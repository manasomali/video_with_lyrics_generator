import gc
import os
import random
from pathlib import Path
import threading

import ffmpeg
from moviepy.editor import (
    AudioFileClip,
    CompositeVideoClip,
    TextClip,
    VideoFileClip,
    concatenate_videoclips,
)


from moviepy.config import change_settings

change_settings(
    {"IMAGEMAGICK_BINARY": r"C:/Program Files/ImageMagick-7.1.1-Q16-HDRI/magick.exe"}
)

import subprocess

def change_pitch_ffmpeg(input_file, output_file, semitone_change):
    pitch_factor = 2 ** (semitone_change / 12.0)
    command = [
        "ffmpeg",
        "-i", input_file,
        "-filter:a", f"asetrate=44100*{pitch_factor},atempo=1/{pitch_factor}"
        "-c:v", "copy",
        output_file
    ]
    subprocess.run(command)

def get_full_file_paths(directory):
    list_files = os.listdir(directory)
    return [os.path.join(directory, item) for item in list_files]

def create_video_from_videos_audio_and_title(background_videos, audio_file, output_file, title):
    audio = AudioFileClip(audio_file)
    audio_duration = audio.duration
    random.shuffle(background_videos)

    clips = []
    total_video_duration = 0

    for video_file in background_videos:
        video_clip = VideoFileClip(video_file)
        text = TextClip(title, fontsize=40, color="white", font="Comic-Sans-MS")
        text = text.set_position(("center", 160)).set_duration(video_clip.duration)
        video_with_text = CompositeVideoClip([video_clip, text])

        if (total_video_duration + video_with_text.duration) > audio_duration:
            remaining_duration = audio_duration - total_video_duration
            video_with_text = video_with_text.subclip(0, remaining_duration)
            clips.append(video_with_text)
            break
        else:
            clips.append(video_with_text)
            total_video_duration += video_with_text.duration

    final_video = concatenate_videoclips(clips, method="compose")
    final_video = final_video.set_audio(audio)
    final_video.write_videofile(output_file, threads = len(threading.enumerate()))


def add_caption_to_video(
    caption: str,
    video: str,
    output: str,
    alignment: str = "10", # Default ASS line alignment (10=Center Center, 6=Top Center, 2=Bottom Center) https://stackoverflow.com/questions/57869367/ffmpeg-subtitles-alignment-and-position
    margin_v: str = "0",
):
    style = f"Alignment={alignment},MarginL=50,MarginR=50,MarginV={margin_v}"
    ffmpeg_input = ffmpeg.input(video)
    video_stream = ffmpeg_input.video
    audio_stream = ffmpeg_input.audio
    try:
        (
            ffmpeg.concat(
                video_stream.filter("subtitles", filename=caption, force_style=style),
                audio_stream,
                v=1,
                a=1,
            )
            .output(output)
            .overwrite_output()
            .run()
        )
    except Exception as e:
        print("Fmmpeg error: ", e)

if __name__ == "__main__":
    gc.collect()

    title = "@manasoma.music"
    current_dir = Path.cwd()
    
    audios_dir = f"{current_dir}/audios"
    subtitles_pt_dir = f"{current_dir}/subtitles/pt"
    subtitles_en_dir = f"{current_dir}/subtitles/en"
    background_videos = get_full_file_paths(f"{current_dir}/backgrounds")
    
    for filename in os.listdir(audios_dir):
        filename_without_ext = filename[:-4]

        audio_file =  f"{audios_dir}/{filename_without_ext}.mp3"
        
        output_file_not_sub = f"videos/not_sub/{filename_without_ext}.mp4"
        output_file_pt_sub = f"videos/pt_sub/{filename_without_ext}.mp4"
        output_file_pt_en_sub = f"videos/pt_en_sub/{filename_without_ext}.mp4"
        output_file_pt_en_sub_pitch = f"videos/pt_en_sub_pitch/{filename_without_ext}.mp4"

        ass_pt_file = f"{subtitles_pt_dir}/{filename_without_ext}.ass"
        ass_en_file = f"{subtitles_en_dir}/{filename_without_ext}.ass"

        if not Path(output_file_not_sub).exists():
            create_video_from_videos_audio_and_title(background_videos, audio_file, output_file_not_sub, title)
        
        if not Path(output_file_pt_sub).exists():
            add_caption_to_video(ass_pt_file, output_file_not_sub, output_file_pt_sub, alignment="6", margin_v="100")
        
        if not Path(output_file_pt_en_sub).exists():
            add_caption_to_video(ass_en_file, output_file_pt_sub, output_file_pt_en_sub, alignment="6", margin_v="170")

        if not Path(output_file_pt_en_sub_pitch).exists():
            change_pitch_ffmpeg(output_file_pt_en_sub, output_file_pt_en_sub_pitch, -1)

        gc.collect()
