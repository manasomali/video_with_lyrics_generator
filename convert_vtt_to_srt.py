import os
import re
from tqdm import tqdm

def vtt_to_srt(vtt_file, srt_file) -> bool:
    try:
        with open(vtt_file, "r", encoding="utf-8") as vtt:
            lines = vtt.readlines()

        with open(srt_file, "w", encoding="utf-8") as srt:
            counter = 1
            for line in lines:
                if line.strip().startswith("WEBVTT"):
                    continue
                if line.strip().startswith("Kind:"):
                    continue
                if line.strip().startswith("Language:"):
                    continue

                timestamp_line = re.sub(r"(\d{2}:\d{2}:\d{2})\.(\d{3})", r"\1,\2", line)
                if re.match(r"\d{2}:\d{2}:\d{2},\d{3}", timestamp_line):
                    srt.write(f"{counter}\n")
                    counter += 1
                
                srt.write(timestamp_line)

        return True
    except Exception as e:
        print("Fail to convert vtt to srt", e)
        return False