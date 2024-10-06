# Video With Lyrics Generator

## Description
This project is a comprehensive tool designed to automate the process of generating music videos with synchronized lyrics. It combines audio tracks, background videos, and multilingual subtitles to create engaging visual content. Key features include:

1. Automatic download of audio, video, and subtitle files from YouTube using [YouTube-DL](https://github.com/yt-dlp/yt-dlp)
2. Conversion of subtitle formats (VTT to SRT)
3. Translation of subtitles between languages (e.g., English to Portuguese)
4. Custom video generation with background clips and audio
5. Addition of stylized subtitles in multiple languages

## Installation

Install ImageMagick and FFmpeg:

 - [YouTube-DL](https://github.com/yt-dlp/yt-dlp)
 - [imagemagick](https://imagemagick.org/index.php)
 - [FFmpeg](https://ffmpeg.org/)

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Before running the project, cun the `create_videos.py` file to create the necessary folders and subfolders.

```bash
python create_dirs.py
```

To download the videos, audio and subtitles, run the following command:

```bash
python download.py
```

Edit the `download.py` file to change the `video_urls` variable adding the URLs of the songs you want to download.

To generate the videos, run the following command:

```bash
python generate_videos.py
```

Edit the `generate_videos.py` file to change the `title` variable and add the videos inside the `videos/backgrounds` folder to be used as background.
The final videos will be saved in the `videos/pt_en_sub` folder, with the audio and subtitles in English and Portuguese

## Sample Result

You can see some results in this TikTok profile [@mansoma.music](https://www.tiktok.com/@manasoma.music)