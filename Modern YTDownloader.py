import tkinter
from tkinter import filedialog
import customtkinter 
from pytube import YouTube

def download():
    finished_label.configure(text="", text_color = "white")
    progressbar.set(0)
    download_path = filedialog.askdirectory()
    if download_path:
        try:
            link = link_var.get()
            video = YouTube(link, on_progress_callback=on_progress)
            video_stream = video.streams.get_highest_resolution()
            title_label.configure(text=video.title)
            progress_frame.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)
            video_stream.download(download_path)
            finished_label.configure(text="Download Complete!")
            progress_frame.place_forget()
        except:
            finished_label.configure(text="Please select a valid YouTube link", 
                                    text_color ="red")
    else:
        finished_label.configure(text="Please select a valid folder", 
                                    text_color ="red")

def on_progress(stream, chunk, bytes_remaining):
    total_size=stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    percent_str = str(int(percentage_of_completion))
    percentage_label.configure(text=percent_str + "%")
    percentage_label.update()
    progressbar.set(float(percentage_of_completion) / 100)


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

window = customtkinter.CTk()
window.geometry("720x480")
window.title("YT Downloader by cjxs")

main_frame= customtkinter.CTkFrame(window)
main_frame.pack(padx=200, pady=80)

progress_frame=customtkinter.CTkFrame(window)
#progress_frame.pack(pady=10)

title_label=customtkinter.CTkLabel(main_frame, text="Enter your YouTube link")
title_label.pack(padx=10, pady=10)

link_var = tkinter.StringVar()
link_entry = customtkinter.CTkEntry(main_frame, width=350, height=40, textvariable=link_var)
link_entry.pack()

download_btn = customtkinter.CTkButton(main_frame, text="Download", command=download)
download_btn.pack(padx = 10, pady=20)

finished_label = customtkinter.CTkLabel(main_frame, text="")
finished_label.pack()

percentage_label = customtkinter.CTkLabel(progress_frame, text="0%")
percentage_label.pack()

progressbar = customtkinter.CTkProgressBar(progress_frame, width=400)
progressbar.set(0)
progressbar.pack(padx=10, pady = 10)

window.mainloop()