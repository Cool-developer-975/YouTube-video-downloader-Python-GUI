import io
import customtkinter as ctk
from PIL import Image,ImageTk
import subprocess
import urllib.request

def place_thumbnail_image(thumbnail_url,thumbnail_label):
    try:
        with urllib.request.urlopen(thumbnail_url) as response:
            image_data = response.read()
        image = Image.open(io.BytesIO(image_data))
        thumbnail = ctk.CTkImage(light_image=image,dark_image=image,size=(400,200))
        thumbnail_label.configure(image=thumbnail)
    except Exception as e:
        print(f"{e}")




def get_entry_url(url,thumbnail_label):
    commands = ['yt-dlp','--get-thumbnail',url.get()]
    try:
        result = subprocess.run(commands,capture_output=True,text=True,check=True)
        thumbnail_url = result.stdout.strip()
        place_thumbnail_image(thumbnail_url,thumbnail_label)
    except subprocess.CalledProcessError as e:
        print(f"error:{e}")
    

def app():
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.title("Youtube video downloader")
    root.geometry("600x600")
    root.columnconfigure(0,weight=1)
    root.rowconfigure(0,weight=1)

    # font
    f = ("system-ui",17)

    # main frame
    main_frame = ctk.CTkFrame(root)
    main_frame.grid(row=0,column=0,padx=20,pady=20,sticky="nswe")

    # Error msg
    error_msg = ctk.CTkLabel(main_frame,font=f,text="Error")
    main_frame.columnconfigure(0,weight=1)
    error_msg.grid(row=0,column=0,pady=10)

    # thumbnail section
    thumbnail_label = ctk.CTkLabel(main_frame,text="",font=f)
    thumbnail_label.grid(row=1,column=0,pady=10)

    # url section

    # url input
    url = ctk.StringVar()
    url_entry = ctk.CTkEntry(main_frame,width=400,height=32,placeholder_text="Enter the url of the video",font=("system-ui",16),justify="center",textvariable=url)
    url_entry.grid(row=2,column=0,pady=10)
    url_entry.bind("<KeyRelease>",lambda event: get_entry_url(url,thumbnail_label))

    # button frame
    btn_frame = ctk.CTkFrame(main_frame)
    btn_frame.grid(row=3,column=0,padx=20,pady=10,sticky="ew")
    btn_frame.columnconfigure(0,weight=1)
    btn_frame.columnconfigure(1,weight=1)
    btn_frame.columnconfigure(2,weight=1)

    # format combobox
    formats = ["mp4","mkv"]
    format_combobox = ctk.CTkComboBox(btn_frame,values=formats)
    format_combobox.set(formats[0])
    format_combobox.grid(row=0,column=0,padx=10,pady=10)

    # quality combobox
    video_quality = ["144p","240p","360p","480p","720p","1080p"]
    quality_combobox = ctk.CTkComboBox(btn_frame,values=video_quality)
    quality_combobox.set(video_quality[0])
    quality_combobox.grid(row=0,column=1,padx=10,pady=10)


    # download button
    download_btn = ctk.CTkButton(btn_frame,text="Download",font=("system-ui",16),border_spacing=7,hover=True,hover_color="#019bfd")
    download_btn.grid(row=0,column=2,padx=10,pady=10)
    root.mainloop()
    return

app()