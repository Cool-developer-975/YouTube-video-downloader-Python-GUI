import os
import tkinter as tk
from pytube import YouTube
from tkinter import ttk
from pytube.exceptions import VideoUnavailable
import threading
import re
from moviepy.editor import VideoFileClip,AudioFileClip

if not os.path.exists("./downloads"):
    os.makedirs("./downloads")

invalid_chars_pattern = r'[<>:"/\\|?*]'

def make_download_status_visible():
    title1.configure(text="Successfully downloaded",fg="green")
    root.after(3000, reset_download_status)
    return

def reset_download_status():
    title1.configure(text="Enter the url of the YouTube video",fg="white")
    return

def show_popup(err_msg:str):
    popup = tk.Toplevel(root,bg="#2b2a33")
    popup.title("Error")
    popup.geometry("500x500")

    label = tk.Label(popup,text=err_msg,justify="center",bg="#2b2a33",fg="white",font=("system-ui",12))
    label.pack(padx=20,pady=10)
    close_btn = tk.Button(popup,text="Ok",bg="#0ea5e9",fg="white",width=14,height=1,relief="flat",font=("system-ui",10),command=popup.destroy)
    close_btn.pack(padx=20,pady=10)


def combineAudioVideo(audio_path:str,video_path:str,orig_name:str):
    try:
        audio_clip = AudioFileClip(audio_path)
        video_clip = VideoFileClip(video_path)
        video_clip = video_clip.set_audio(audio_clip)
        global invalid_chars_pattern
        orig_name = re.sub(invalid_chars_pattern,'_',orig_name)
        video_clip.write_videofile(f"./downloads/{orig_name}.mp4", codec="h264", audio_codec="aac")
        make_download_status_visible()
        print("Downloaded")
        os.remove(audio_path)
        os.remove(video_path)
    except Exception as e:
        show_popup(f"{e}")
    return

def downloadVideo_task():
    try:
        resolution = selected_option.get()
        vid_format = selected_format.get()
        url = video_link.get()
        yt = YouTube(url)
        streams = yt.streams.filter(adaptive=True)
        print(streams)
        v_streams = streams.filter(file_extension=vid_format,res=resolution)
        audio_streams = streams.filter(only_audio=True)
        print(f"{v_streams} \n {audio_streams}")
        video = v_streams.first()
        audio = audio_streams.first()
        if video and audio:
            audio_path = audio.download(filename="audio.mp4")
            video_path = video.download(output_path="./")
            combineAudioVideo(audio_path,video_path,yt.title)
        else:
            show_popup("Video quality or video extension not found select different quality or extension.")
    except VideoUnavailable as e:
        show_popup("Video is not available!")
    except:
        show_popup("An error occured!")
    

def downloadVideo():
    download_task = threading.Thread(target=downloadVideo_task)
    download_task.start()
    return


# root
root = tk.Tk()
root.geometry("500x500")
root.title("Youtube video Downloader")
root.configure(bg="#2b2a33")

# Variables
video_link = tk.StringVar()


#First heading 
title1 = tk.Label(root,text="Enter the url of the youtube video",font=("system-ui",14),fg="white",bg="#2b2a33")
title1.pack(padx=30,pady=10)



#url input
url_input = tk.Entry(root,width=50,justify="center",font=("system-ui",13),relief="flat",textvariable=video_link)
url_input.pack(padx=50,pady=20)

# download_component
download_component = tk.Frame(root,bg="#2b2a33")
download_component.pack(padx=50,pady=10)

# Download button
download_btn = tk.Button(download_component,text="Download",bg="#0ea5e9",fg="white",width=14,height=1,relief="flat",font=("system-ui",11),command=downloadVideo)
download_btn.pack(padx=10,pady=10,side="left")

# dropdown
options = ["144p","240p","360p","480p", "720p","1080p"]
selected_option = tk.StringVar()
selected_option.set(options[0])
dropdown_menu = ttk.Combobox(download_component, values=options,textvariable=selected_option)
dropdown_menu.pack(padx=5, pady=20,side="right")


# dropdown 2
formats = ["mp4","mkv"]
selected_format = tk.StringVar()
selected_format.set(formats[0])
dropdown_menu2 = ttk.Combobox(download_component,values=formats,textvariable=selected_format)
dropdown_menu2.pack(padx=10, pady=20,side="right")

root.mainloop()