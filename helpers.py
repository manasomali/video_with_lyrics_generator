import re

import pysrt
from googletranslatepy import Translator
from tqdm import tqdm

def translate_srt_file(file_path: str, src_lang: str, dest_lang: str, out_file: str) -> None:
    print("Translating:", file_path)
    translator = Translator(source=src_lang, target=dest_lang)

    subs = pysrt.open(file_path, encoding="utf-8")

    for subtitle in tqdm(subs, desc="Translating subtitle"):
        original_text = subtitle.text
        translated_text = translator.translate(original_text)
        if translated_text:
            translated_text_upper = translated_text.upper()
            subtitle.text = translated_text_upper

    subs.save(out_file, encoding="utf-8")


def post_process_srt(file_path: str) -> None:
    print("Processing:", file_path)

    subs = pysrt.open(file_path, encoding="utf-8")

    for subtitle in tqdm(subs, desc="Processing subtitle"):
        original_text: str = subtitle.text
        new_text: str = original_text.replace("&nbsp","").replace("&NBSP","").replace(";","").replace("♪","").replace("  ","").strip()
        if "/pt/" in file_path:
            new_text = new_text.upper()
        
        subtitle.text = new_text

    subs.save(file_path, encoding="utf-8")

def vtt_to_srt(vtt_file: str, srt_file: str) -> bool:
    try:
        with open(vtt_file, "r", encoding="utf-8") as vtt:
            lines: list[str] = vtt.readlines()

        with open(srt_file, "w", encoding="utf-8") as srt:
            counter: int = 1
            for line in lines:
                if line.strip().startswith("WEBVTT"):
                    continue
                if line.strip().startswith("Kind:"):
                    continue
                if line.strip().startswith("Language:"):
                    continue

                timestamp_line: str = re.sub(r"(\d{2}:\d{2}:\d{2})\.(\d{3})", r"\1,\2", line)
                if re.match(r"\d{2}:\d{2}:\d{2},\d{3}", timestamp_line):
                    srt.write(f"{counter}\n")
                    counter += 1
                
                srt.write(timestamp_line)

        return True
    except Exception as e:
        print("Fail to convert vtt to srt", e)
        return False