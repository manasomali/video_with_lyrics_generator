import os
import subprocess
from pathlib import Path

from helpers import vtt_to_srt, translate_srt_file, post_process_srt, srt_to_ass, remove_lang_sufix


def download_video(url: str, mp4_destiny: str) -> None:
    subprocess.run([
        "yt-dlp",
        "-f", "bestvideo+bestaudio",
        "--merge-output-format", "mp4",
        "--output", f"{mp4_destiny}/%(title)s.%(ext)s",
        url
    ])

def convert_mp4_to_mp3(mp4_file, mp3_file):
    command = [
        'ffmpeg',
        '-i', mp4_file,
        '-q:a', '0',
        '-map', 'a',
        mp3_file
    ]
    subprocess.run(command)

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
        "https://www.youtube.com/watch?v=PVjiKRfKpPI"
    ]
    sub_langs=["en", "pt"]
    current_dir = Path.cwd()
    for url in video_urls:
        download_video(url, f"{current_dir}/videos/original")
        download_subs(url, f"{current_dir}/subtitles", sub_langs)
    
    for filename in os.listdir(f"{current_dir}/videos/original"): 
        mp3_filename = filename.replace("mp4", "mp3")
        mp3_path = f"{current_dir}/audios/{mp3_filename}"
        if not os.path.exists(mp3_path):
            convert_mp4_to_mp3(f"{current_dir}/videos/original/{filename}", mp3_path)

    for lang in sub_langs:
        for filename in os.listdir(f"{current_dir}/subtitles/{lang}"):
            if filename.endswith(".vtt"):
                vtt_path = f"{current_dir}/subtitles/{lang}/{filename}"
                srt_path = remove_lang_sufix(vtt_path).replace(".vtt", ".srt")
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

    for filename in os.listdir(f"{current_dir}/subtitles/pt"):
        if filename.endswith(".srt"):
            if Path(f"{current_dir}/subtitles/en/{filename}").exists():
                print(f"Already exists: {current_dir}/subtitles/en/{filename}")
                continue
            
            translate_srt_file(
                f"{current_dir}/subtitles/pt/{filename}",
                src_lang="pt",
                dest_lang="en",
                out_file=f"{current_dir}/subtitles/en/{filename}"
            )
    
    for lang in sub_langs:
        for filename in os.listdir(f"{current_dir}/subtitles/{lang}"):
            if filename.endswith(".srt"):
                post_process_srt(f"{current_dir}/subtitles/{lang}/{filename}")

    for lang in sub_langs:
        for filename in os.listdir(f"{current_dir}/subtitles/{lang}"):
            if filename.endswith(".srt"):
                if lang=="pt":
                    if Path(f"{current_dir}/subtitles/pt/{filename.replace(".srt", ".ass")}").exists():
                        print(f"Already exists: {current_dir}/subtitles/pt/{filename.replace(".srt", ".ass")}")
                        continue
                    srt_to_ass(f"{current_dir}/subtitles/{lang}/{filename}", fade_in_ms=400, fade_out_ms=400, font="Raleway Heavy", color="&Hffffff", font_size="12", karaoke=True)
                if lang=="en":
                    if Path(f"{current_dir}/subtitles/{lang}/{filename.replace(".srt", ".ass")}").exists():
                        print(f"Already exists: {current_dir}/subtitles/en/{filename.replace(".srt", ".ass")}")
                        continue
                    srt_to_ass(f"{current_dir}/subtitles/{lang}/{filename}", fade_in_ms=400, fade_out_ms=400, font="relationship of mélodrame", color="&H03fcff", font_size="12", karaoke=False)