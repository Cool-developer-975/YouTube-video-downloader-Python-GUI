# YouTube Downloader using Python GUI

This repository contains a simple YouTube video downloader with a graphical user interface (GUI) built using Python. The application allows you to download YouTube videos by providing the video URL, selecting the desired video format, and quality. It utilizes the `yt_dlp` library for downloading YouTube videos.

## Prerequisites
1. **Python**: Make sure you have Python installed on your system.
2. **Libraries**: Install the required libraries using the following command:
    ```bash
    pip install Pillow customtkinter yt-dlp
    ```

## How to Use
1. **Run the Script**: Execute the script in your preferred Python environment.
2. **Enter URL**: Enter the YouTube video URL in the provided input field.
3. **Thumbnail Display**: The thumbnail of the video will be displayed.
4. **Format and Quality Selection**: Choose the video format (mp4 or mkv) and quality (144p, 240p, 360p, 480p, 720p, 1080p).
5. **Start Download**: Click the "Download" button to initiate the download process.

## Code Explanation

### Libraries Used
- `os`: Provides a way of using operating system-dependent functionality.
- `io`: Provides the Python interfaces to stream handling.
- `re`: Regular expression operations.
- `customtkinter`: A custom tkinter library.
- `PIL`: Python Imaging Library for working with images.
- `urllib.request`: Library for opening URLs.
- `threading`: Provides thread-based parallelism.
- `yt_dlp`: YouTube video downloader library.

### Functions
1. **`reset_error_msg`**: Resets the error message on the GUI.
2. **`reset_thumbnail_msg`**: Resets the thumbnail message on the GUI.
3. **`reset_progress_label`**: Resets the progress label on the GUI.
4. **`place_thumbnail_image`**: Downloads and displays the thumbnail image on the GUI.
5. **`get_entry_url`**: Extracts video information without downloading and displays the thumbnail.
6. **`get_thumbnail`**: Initiates the process of getting the thumbnail in a separate thread.
7. **`on_progress`**: Updates the progress bar and label during the download process.
8. **`download`**: Downloads the YouTube video based on the specified format and quality.
9. **`download_video`**: Initiates the video download process in a separate thread.
10. **`app`**: Sets up the GUI using custom tkinter elements and runs the main application.

## Note
- The downloaded videos will be saved in the "downloads" folder within the script directory.
- Ensure that the required libraries are installed before running the script.
- The GUI is designed using a custom dark theme for a better user experience.
