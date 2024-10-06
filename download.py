import os
import subprocess
from pathlib import Path
import re

from helpers import vtt_to_srt, translate_srt_file, post_process_srt


def download_video(url: str, mp4_destiny: str) -> None:
    subprocess.run([
        "yt-dlp",
        "-f", "bestvideo+bestaudio",
        "--merge-output-format", "mp4",
        "--output", f"{mp4_destiny}/%(title)s.%(ext)s",
        url
    ])

def download_audio(url: str, mp3_destiny: str) -> None:
    subprocess.run([
        "yt-dlp",
        "-x",
        "--audio-format", "mp3",
        "--output", f"{mp3_destiny}/%(title)s.%(ext)s",
        url
    ])

def download_subs(url: str, srt_destiny: str, sub_langs: list[str]) -> None:
    for lang in sub_langs:
        subprocess.run([
            "yt-dlp",
            "--write-subs",
            "--sub-langs", f"{lang}.*",
            "--skip-download",
            "--output", f"{srt_destiny}/{lang}/%(title)s.%(ext)s",
            url
        ])

if __name__ == "__main__":
    video_urls = [
        "https://www.youtube.com/watch?v=k4V3Mo61fJM",
        "https://www.youtube.com/watch?v=KtlgYxa6BMU",
        "https://www.youtube.com/watch?v=XFkzRNyygfk",
        "https://www.youtube.com/watch?v=RBumgq5yVrA",
        "https://www.youtube.com/watch?v=wVyggTKDcOE",
        "https://www.youtube.com/watch?v=YaEG2aWJnZ8"
    ]
    sub_langs=["en", "pt"]
    current_dir = Path.cwd()
    for url in video_urls:
        download_video(url, f"{current_dir}/videos/original")
        download_audio(url, f"{current_dir}/audios")
        download_subs(url, f"{current_dir}/subtitles", sub_langs)
    
    for lang in sub_langs:
        for filename in os.listdir(f"{current_dir}/subtitles/{lang}"):
            if filename.endswith(".vtt"):
                vtt_path = f"{current_dir}/subtitles/{lang}/{filename}"
                srt_path = re.sub(r'\..*?\.', '.', vtt_path).replace(".vtt", ".srt")
                success = vtt_to_srt(
                    vtt_path,
                    srt_path
                )
                if success:
                    os.remove(vtt_path)
    
    for filename in os.listdir(f"{current_dir}/subtitles/en"):
        if filename.endswith(".srt"):
            if Path(f"{current_dir}/subtitles/pt/{filename}").exists():
                print(f"Already exists: {current_dir}/subtitles/pt/{filename}")
                continue
            
            translate_srt_file(
                f"{current_dir}/subtitles/en/{filename}",
                src_lang="en",
                dest_lang="pt",
                out_file=f"{current_dir}/subtitles/pt/{filename}"
            )
    
    for lang in sub_langs:
        for filename in os.listdir(f"{current_dir}/subtitles/{lang}"):
            if filename.endswith(".srt"):
                post_process_srt(f"{current_dir}/subtitles/{lang}/{filename}")
