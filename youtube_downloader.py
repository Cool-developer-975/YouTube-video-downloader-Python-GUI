from os import mkdir,path
from io import BytesIO
from sys import exit
from re import search
import customtkinter as ctk
from PIL import Image
from urllib import request
from threading import Thread
import yt_dlp

# to keep reference of images
images = []

def reset_error_msg(error_msg):
    error_msg.configure(text="")
    return

def reset_thumbnail_msg(thumbnail_label):
    thumbnail_label.configure(text="",text_color="white")
    return

def reset_progress_label(progress_label):
    progress_label.configure(text="")
    return


def place_thumbnail_image(thumbnail_url,thumbnail_label):
    try:
        with request.urlopen(thumbnail_url) as response:
            image_data = response.read()
        t_image = Image.open(BytesIO(image_data))
        images.append(t_image)
        thumbnail = ctk.CTkImage(dark_image=t_image,size=(400,200))
        thumbnail_label.configure(text="",image=thumbnail)
    except Exception as e:
        print(f"pt-{e}")
        thumbnail_label.configure(text="THUMBNAIL NOT AVAILABLE!")
        thumbnail_label.after(5000,lambda:reset_thumbnail_msg(thumbnail_label))
    return

def on_change_get_size(video_size_label,url,video_quality,vid_format,error_msg):
    try:
        ydl = yt_dlp.YoutubeDL({"format":f"best[height<={video_quality.get()[:-1]}][width<={video_quality.get()[:-1]}][ext={vid_format.get()}]"})
        result = ydl.extract_info(url.get(),download=False)
        if result != None:
            size = result.get("filesize_approx")
            if size:
                size = size / (1024**2)
                video_size_label.configure(text=f"Size : {size:.2f} MB")
            else:
                video_size_label.configure(text="Size : NA, try downloading")
        else:
            video_size_label.configure(text="NA, try downloading")
    except Exception as e:
        video_size_label.configure(text="Size : NA")
        print(f"ch = {e}")
        error_msg.configure(text="Video not available please select other formats or quality.")
        error_msg.after(5000, lambda: reset_error_msg(error_msg))

def on_dropdown_change(video_size_label,url,video_quality,vid_format,error_msg):
    video_size_label.configure(text="Please wait getting size....")
    t3 = Thread(target=on_change_get_size, args=(video_size_label,url,video_quality,vid_format,error_msg))
    t3.start()
    return    

def get_entry_url(url, thumbnail_label, error_msg, video_size_label,vid_format,video_quality):
    ydl = yt_dlp.YoutubeDL({'writethumbnail': True})
    try:
        result = ydl.extract_info(url.get(), download=False)
        if result != None:
            thumbnail_url = result.get('thumbnail', None)

            if thumbnail_url:
                place_thumbnail_image(thumbnail_url, thumbnail_label)
                size = result.get("filesize_approx",0)
                video_size_label.configure(text="Please wait getting size....")
                if size:
                    t4 = Thread(target=on_change_get_size,args=(video_size_label,url,video_quality,vid_format,error_msg))
                    t4.start()
                else:
                    video_size_label.configure(text="NA, try downloading")
            else:
                # raise ValueError("Thumbnail URL not found")
                thumbnail_label.configure(image="",text="Thumbnail not found!",text_color="red")
                thumbnail_label.after(5000,lambda : reset_thumbnail_msg(thumbnail_label))

    except yt_dlp.utils.DownloadError as e:
        print(f"th - {e}")
        error_msg.configure(text="INVALID URL or video format is not available", text_color="red")
        error_msg.after(5000, lambda: reset_error_msg(error_msg))
    return

def get_thumbnail(url,thumbnail_label,error_msg,video_size_label,vid_format,video_quality):
    try:
        if len(url.get()) > 0:
            thumbnail_label.configure(image=None,text="Getting thumbnail...",text_color = "white")
            t1 = Thread(target=get_entry_url,args=(url,thumbnail_label,error_msg,video_size_label,vid_format,video_quality))
            t1.start()
    except Exception as e:
        print(f"{e}")
    return

def on_progress(d,progress_bar,progress_label,error_msg):
    if d['status'] == 'downloading':
        percent = search(r"\d+\.\d",d['_percent_str'])
        if percent:
            percent = float(percent.group())
            progress_bar.set(percent/100)
            progress_label.configure(text=f"{percent}% downloaded")

    elif d['status'] == 'finished':
        progress_label.configure(text="Download complete!")
        progress_bar.grid_forget()
        progress_label.after(5000,lambda:reset_progress_label(progress_label))
    elif d['status'] == 'error':
        error_msg.configure(text=f"{d['error']}")
        error_msg.after(5000,lambda:reset_error_msg(error_msg))

    return

def download(vid_format,video_quality,url,error_msg,progress_bar,progress_label):
    commands = {
        'format':f'best[height<={video_quality[:-1]}][width<={video_quality[:-1]}]',
        'outtmpl':f'./downloads/%(title)s_%(resolution)s.{vid_format}',
        'progress_hooks':[lambda d: on_progress(d,progress_bar,progress_label,error_msg)],
    }
    with yt_dlp.YoutubeDL(commands) as ydl:
        try:
            progress_bar.grid(row=6, column=0, pady=10)
            progress_bar.set(0)
            ydl.download([url])  
        except Exception as e:
            print(f"{e}")
            error_msg.configure(text="Error while downloading video,select another quality or video format", text_color="red")
            progress_bar.grid_forget()
            error_msg.after(5000, lambda: reset_error_msg(error_msg))
        return

def download_video(vid_format,video_quality,url,error_msg,progress_bar,progress_label):
    try:
        t2 = Thread(target=download,args=(vid_format,video_quality,url,error_msg,progress_bar,progress_label))
        t2.start()
    except Exception as e:
        print(f"{e}")
    return

def exitProgram()->None:
    exit()
    return

def app():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    root = ctk.CTk()
    root.title("Youtube video downloader")
    root.geometry("600x600")
    root.protocol("WM_DELETE_WINDOW",exitProgram)
    root.columnconfigure(0,weight=1)
    root.rowconfigure(0,weight=1)

    # font
    f = ("system-ui",17)

    # main frame
    main_frame = ctk.CTkFrame(root)
    main_frame.grid(row=0,column=0,padx=20,pady=20,sticky="nswe")

    # Error msg
    error_msg = ctk.CTkLabel(main_frame,font=f,text="",text_color="Red")
    main_frame.columnconfigure(0,weight=1)
    error_msg.grid(row=0,column=0,pady=10)

    # thumbnail section
    thumbnail_label = ctk.CTkLabel(main_frame,text="",font=f,text_color="Red")
    thumbnail_label.grid(row=1,column=0,pady=10)
    
    # video size
    video_size_label = ctk.CTkLabel(main_frame,text="",font=f,text_color="white")
    video_size_label.grid(row=2,column=0,pady=10)

    # url section
    url_label = ctk.CTkLabel(main_frame,text="Paste the url of video below",font=f)
    url_label.grid(row=3,column=0,pady=10)

    # url input
    url = ctk.StringVar()
    url_entry = ctk.CTkEntry(main_frame,width=400,height=32,font=("system-ui",16),justify="center",textvariable=url,text_color="white")
    url_entry.grid(row=4,column=0,pady=10)
    url.trace_add("write",lambda *args:get_thumbnail(url,thumbnail_label,error_msg,video_size_label,vid_format,video_quality))
    # url_entry.bind("<KeyRelease>",lambda event: get_thumbnail(url,thumbnail_label,error_msg))

    # progress label
    progress_label = ctk.CTkLabel(main_frame,font=f,text="")
    progress_label.grid(row=5,column=0,pady=10)
    # Progress bar
    progress_bar = ctk.CTkProgressBar(main_frame)

    # button frame
    btn_frame = ctk.CTkFrame(main_frame)
    btn_frame.grid(row=7,column=0,padx=20,pady=10,sticky="ew")
    btn_frame.columnconfigure(0,weight=1)
    btn_frame.columnconfigure(1,weight=1)
    btn_frame.columnconfigure(2,weight=1)

    # format combobox
    vid_format = ctk.StringVar() 
    formats = ["mp4","mkv"]
    format_combobox = ctk.CTkComboBox(btn_frame,values=formats,font=("system-ui",14),dropdown_font=("system-ui",14),variable=vid_format,command=lambda e:on_dropdown_change(video_size_label,url,video_quality,vid_format,error_msg))
    vid_format.set(formats[0])
    format_combobox.grid(row=0,column=0,padx=10,pady=10)

    # quality combobox
    video_quality = ctk.StringVar()
    video_qualities = ["144p","240p","360p","480p","720p","1080p"]
    quality_combobox = ctk.CTkComboBox(btn_frame,values=video_qualities,font=("system-ui",14),dropdown_font=("system-ui",14),variable=video_quality,command=lambda e:on_dropdown_change(video_size_label,url,video_quality,vid_format,error_msg))
    video_quality.set(video_qualities[4])
    quality_combobox.grid(row=0,column=1,padx=10,pady=10)
    

    # download button
    download_btn = ctk.CTkButton(btn_frame,text="Download",font=("system-ui",16),border_spacing=7,command=lambda:download_video(vid_format.get(),video_quality.get(),url.get(),error_msg,progress_bar,progress_label))
    download_btn.grid(row=0,column=2,padx=10,pady=10)
    root.mainloop()
    return

if not path.exists("./downloads"):
    mkdir("./downloads")

app()
images.clear()