from pytube import YouTube
import tkinter as tk
from tkinter import ttk, filedialog
import time

def download_video():
    global start_time
    global stream
    link = url_entry.get()
    video = YouTube(link)
    stream = video.streams.get_highest_resolution()
    print(f"File Size: {stream.filesize_mb:.2f} MegaBytes")
    download_path = filedialog.askdirectory()
    with stream.download(download_path) as file:
        pass
    start_time = time.time()
    timer = root.after(1000, update_time)
    root.after_cancel(timer)

def show_progress(stream, chunk, bytes_remaining):
    size = stream.filesize
    progress = (size - bytes_remaining) / size
    progress_percent = round(progress * 100, 2)
    speed = round((size - bytes_remaining) / (time.time() - start_time), 2)
    progress_label.config(text=f"{size - bytes_remaining} / {size} bytes")
    speed_label.config(text=f"{speed} bytes/s")
    progress_bar["value"] = progress_percent
    time_label.config(text="time_elapsed"(start_time))

def update_time():
    global start_time
    global timer
    current_time = time.time()
    elapsed_time = current_time - start_time
    hours, remainder = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    time_label.config(text=f"{int(hours)}:{int(minutes)}:{int(seconds)}")
    speed = (stream.filesize - stream.bytes_remaining) / elapsed_time
    speed_label.config(text=f"{speed:.2f} bytes/s")
    timer = root.after(1000, update_time)

def show_title(event=None):
    link = url_entry.get()
    try:
        video = YouTube(link)
        title_label.config(text=video.title)
    except:
        title_label.config(text="Invalid URL")

root = tk.Tk()
root.title("YouTube Video Downloader")
root.geometry("500x300")

ttk.Style().configure('TButton', padding=10, relief="flat", background="#ccc")
ttk.Style().configure('TLabel', padding=5, background="#fff")

title_label = ttk.Label(root)
title_label.place(x=50, y=30)

url_label = ttk.Label(root, text="Enter URL:")
url_label.place(x=50, y=80)

url_entry = ttk.Entry(root)
url_entry.place(x=130, y=85, width=320)
url_entry.bind("<KeyRelease>", show_title)

download_button = ttk.Button(root, text="Download", style="TButton", command=download_video)
download_button.place(x=50, y=120)

choose_button = ttk.Button(root, text="Choose Location", style="TButton", command=lambda: filedialog.askdirectory())
choose_button.place(x=170, y=120)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.place(x=50, y=170)

progress_label = ttk.Label(root, text="0 / 0 bytes")
progress_label.place(x=50, y=210)

speed_label = ttk.Label(root, text="0.00 bytes/s")
speed_label.place(x=350, y=210)

time_label = ttk.Label(root, text="0:0:0")
time_label.place(x=200, y=260)

root.mainloop()
