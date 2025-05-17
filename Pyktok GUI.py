import os
import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from tqdm import tqdm


def download_video():
    url = url_entry.get().strip()
    if not url:
        messagebox.showerror("Ошибка", "Введите ссылку на видео TikTok!")
        return

    download_folder = "TikTok Downloads"
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    try:
        service_url = f"https://tikdown.org/get?url={url}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(service_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        video_url = None
        for a in soup.find_all('a', href=True):
            if 'video' in a['href'] and 'tikdown' not in a['href']:
                video_url = a['href']
                break

        if not video_url:
            messagebox.showerror("Ошибка", "Не удалось извлечь ссылку на видео!")
            return
            
        video_response = requests.get(video_url, headers=headers, stream=True)
        video_response.raise_for_status()

        parsed_url = urlparse(url)
        video_id = parsed_url.path.split('/')[-1] if parsed_url.path else 'tiktok_video'
        filename = os.path.join(download_folder, f"{video_id}.mp4")

        total_size = int(video_response.headers.get('content-length', 0))
        with open(filename, 'wb') as file, tqdm(
                desc="Скачивание",
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
        ) as bar:
            for chunk in video_response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
                    bar.update(len(chunk))

        messagebox.showinfo("Успех!", f"Видео сохранено в:\n{filename}")

    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка:\n{str(e)}")


root = tk.Tk()
root.title("TikTok Video Downloader")
root.geometry("500x150")

tk.Label(root, text="Введите ссылку на видео TikTok:", font=('Arial', 12)).pack(pady=5)

url_entry = tk.Entry(root, width=50, font=('Arial', 10))
url_entry.pack(pady=5)

download_btn = tk.Button(
    root,
    text="Скачать видео",
    command=download_video,
    bg='#FF0050',  # Цвет как в TikTok
    fg='white',
    font=('Arial', 12)
)
download_btn.pack(pady=10)

root.mainloop()
