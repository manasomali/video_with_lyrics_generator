import os

DIRS = [
    "videos/not_sub", 
    "videos/original",
    "videos/pt_sub",
    "videos/pt_en_sub",
    "subtitles/pt",
    "subtitles/en",
    "backgrounds",
    "audios"
]

if __name__ == "__main__":
    for directory in DIRS:
        os.makedirs(directory, exist_ok=True)