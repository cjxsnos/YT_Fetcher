from pytube import YouTube
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import time



def download_video():
    global start_time,stream, video, video_size, video_size_mb
    download_path = filedialog.askdirectory()
    if not video:
        messagebox.showwarning("Warning", "Please enter a valid URL.")
        return
    
    def update_progress(current, total):
        progress = int(current / total * 100)
        progress_bar['value'] = progress
        progress_label.config(text=f"{current / (1024 * 1024):.2f} / {total / (1024 * 1024):.2f} MB")
        speed_label.config(text=f"{stream.download_speed / (1024 * 1024):.2f} MB/s")
        elapsed_time = time.time() - start_time
        elapsed_time_str = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
        remaining_time = (total - current) / stream.download_speed
        remaining_time_str = time.strftime("%H:%M:%S", time.gmtime(remaining_time))
        time_label.config(text=f"{elapsed_time_str} / {remaining_time_str}")
        root.after(100, update_progress, current, total)

    progress_bar['value'] = 0
    progress_bar['maximum'] = video_size
    progress_label.config(text="0.00 / {:.2f} MB".format(video_size_mb))
    speed_label.config(text="0.00 MB/s")
    time_label.config(text="00:00:00 / 00:00:00")
    start_time = time.time()
    try:
        stream.download(download_path)
        messagebox.showinfo("Success", "Video downloaded successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download video.\nError message: {str(e)}")

def show_progress(stream, chunk, bytes_remaining):
    global video_size
    progress = (video_size - bytes_remaining) / video_size
    progress_percent = round(progress * 100, 2)
    speed = round((video_size - bytes_remaining) / (time.time() - start_time), 2)
    progress_label.config(text=f"{video_size - bytes_remaining} / {video_size} bytes")
    speed_label.config(text=f"{speed} bytes/s")
    progress_bar["value"] = progress_percent
    time_label.config(text=f"time_elapsed{start_time}")

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

def get_video_info(event=None):
    global video, video_size, stream, video_size_mb
    link = video_link_var.get()
    try:
        video = YouTube(link)
        video_tile_var.set(video.title)
        stream = video.streams.get_highest_resolution()
        video_size = stream.filesize
        video_size_mb = video_size / (1024 * 1024)
        progress_label.config(text=f"{video_size_mb:.2f} mbytes")
    except:
        video_tile_var.set("Invalid URL")

root = tk.Tk()
root.title("YouTube Video Downloader")
root.geometry("500x300")

video_tile_var = tk.StringVar()
#video_size_var = tk.DoubleVar()
video_link_var = tk.StringVar()

ttk.Style().configure('TButton', padding=10, relief="flat", background="#ccc")
ttk.Style().configure('TLabel', padding=5, background="#fff")

title_label = ttk.Label(root, textvariable = video_tile_var)
title_label.place(x=50, y=30)

url_label = ttk.Label(root, text="Enter URL:")
url_label.place(x=50, y=80)

url_entry = tk.Entry(root, textvariable = video_link_var)
url_entry.place(x=130, y=85, width=320)
url_entry.bind("<KeyRelease>", get_video_info)

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
