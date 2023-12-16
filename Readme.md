# YouTube Video Downloader

This is a simple Python GUI application built with Tkinter and Pytube to download YouTube videos. The application allows users to input a YouTube video URL, select video quality, and choose the desired video format for download.

## Prerequisites

- Python 3.x
- Required Python packages: `os`, `tkinter`, `pytube`, `threading`, `pathlib`, `moviepy`

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/your-repo.git
    ```

2. Install the required packages:

    ```bash
    pip install pytube moviepy
    ```

3. Run the application:

    ```bash
    python youtube_downloader.py
    ```

## Usage

1. Launch the application.
2. Enter the URL of the YouTube video in the provided input field.
3. Choose the desired video quality and format from the dropdown menus.
4. Click the "Download" button to start the download process.

## Features

- Video quality selection (144p, 240p, 360p, 480p, 720p, 1080p)
- Video format selection (mp4, mkv)
- Download status display
- Error handling for unavailable videos or download issues

## Folder Structure

- The downloaded videos are saved in the "downloads" folder.

## Screenshots

[Include screenshots if possible]

## Acknowledgments

- This project uses the Pytube library for YouTube video downloading.
- The GUI is built with Tkinter.

## License

This project is licensed under the [MIT License](LICENSE).