import os
from moviepy.editor import VideoFileClip
from tqdm import tqdm

def extract_audio(mp4_file, output_audio_file):
    video = VideoFileClip(mp4_file)
    audio = video.audio
    audio.write_audiofile(output_audio_file)
    video.close()

if __name__ == "__main__":
    input_dir = os.getcwd()
    filenames = [f for f in os.listdir(input_dir) if f.endswith(".mp4")]

    for filename in tqdm(filenames, desc="Extracting audio"):
        mp4_file = os.path.join(input_dir, filename)
        output_audio_file = os.path.join(input_dir, filename.replace(".mp4", ".mp3"))
        extract_audio(mp4_file, output_audio_file)
