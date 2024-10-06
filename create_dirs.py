import os

dirs = [
    "videos/not_sub", 
    "videos/original",
    "videos/pt_sub",
    "videos/pt_en_sub",
    "subtitles/pt",
    "subtitles/en",
    "backgrounds",
    "audios"
]

for directory in dirs:
    os.makedirs(directory, exist_ok=True)