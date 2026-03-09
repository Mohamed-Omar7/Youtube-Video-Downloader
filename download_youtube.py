from pytubefix import YouTube
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar

# progress function
def progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = int(bytes_downloaded / total_size * 100)

    progress_bar['value'] = percentage
    root.update_idletasks()


def choose_folder():
    folder = filedialog.askdirectory()
    path_label.config(text=folder)


def download_video():
    try:
        link = entry.get()

        if link == "":
            messagebox.showwarning("Warning", "Enter YouTube link")
            return

        folder = path_label.cget("text")

        yt = YouTube(link, on_progress_callback=progress)

        title_label.config(text=yt.title)

        if type_var.get() == "video":
            stream = yt.streams.get_highest_resolution()
        else:
            stream = yt.streams.filter(only_audio=True).first()

        stream.download(folder)

        messagebox.showinfo("Success", "Download completed!")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# GUI
root = Tk()
root.title("YouTube Downloader")
root.geometry("500x400")
root.resizable(False, False)

Label(root,
      text="YouTube Downloader",
      font=("calibri", 22, "bold"),
      fg="purple").pack(pady=10)

entry = Entry(root, width=50, font=("calibri", 12))
entry.pack(pady=10)

title_label = Label(root, text="", font=("calibri", 10))
title_label.pack()

Button(root,
       text="Choose Folder",
       command=choose_folder).pack(pady=5)

path_label = Label(root, text="No folder selected", fg="gray")
path_label.pack()

# download type
type_var = StringVar(value="video")

Radiobutton(root, text="Video", variable=type_var, value="video").pack()
Radiobutton(root, text="Audio (MP3)", variable=type_var, value="audio").pack()

# progress bar
progress_bar = Progressbar(root, length=300)
progress_bar.pack(pady=20)

Button(root,
       text="Download",
       font=("calibri", 12),
       bg="purple",
       fg="white",
       command=download_video).pack()

root.mainloop()