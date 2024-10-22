import re

import pysrt
from googletranslatepy import Translator
from tqdm import tqdm
import pysubs2

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


def srt_to_ass(input_srt, fade_in_ms: int, fade_out_ms: int, font: str, color: str, font_size: str, karaoke: bool):
    subs = pysubs2.load(input_srt, encoding="utf-8")
    
    for style in subs.styles.values():
        style.fontname = font
        style.fontsize = float(font_size)
        style.primarycolor = color

    for event in subs:
        event.text = str(event.text)

    subs.save(input_srt.replace(".srt", ".ass"))
    
    disable_scalal_border_and_shadow(input_srt.replace(".srt", ".ass"))
    if karaoke:
        add_karaoke_effect_evenly(input_srt.replace(".srt", ".ass"))
    add_fade_in_and_fade_out(input_srt.replace(".srt", ".ass"), fade_in_ms, fade_out_ms)

def add_fade_in_and_fade_out(ass_file_path, fade_in_ms, fade_out_ms):
    subs = pysubs2.load(ass_file_path, encoding="utf-8")
    for event in subs:
        event.text = f"{{\\fad({fade_in_ms},{fade_out_ms})}}{event.text}"

    subs.save(ass_file_path.replace(".srt", ".ass"))


def disable_scalal_border_and_shadow(ass_file_path):
    with open(ass_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    lines = [line.replace("ScaledBorderAndShadow: yes", "ScaledBorderAndShadow: no") for line in lines]

    with open(ass_file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)

def add_karaoke_effect_evenly(ass_file_path):
    subs = pysubs2.load(ass_file_path)

    for line in subs:
        if not line.is_comment:
            total_duration = (line.end - line.start) // 10
            
            words = line.text.split()
            num_words = len(words)
            
            if num_words == 0:
                continue

            word_duration = total_duration // num_words
            
            new_text = ""
            for word in words:
                new_text += f"{{\\k{word_duration}}}{word} "

            line.text = new_text.strip()

    subs.save(ass_file_path)

def post_process_srt(file_path: str) -> None:
    print("Processing:", file_path)

    subs = pysrt.open(file_path, encoding="utf-8")

    for subtitle in tqdm(subs, desc="Processing subtitle"):
        original_text: str = subtitle.text
        cleaned_text = re.sub(r'\[.*?\]|\(.*?\)', '', original_text)
        processed_text = ' '.join(cleaned_text.split())
        new_text: str = processed_text.replace("&nbsp","").replace("&NBSP","").replace(";","").replace("♪","").replace("  ","").strip()
        if "/pt/" in file_path:
            new_text = new_text.upper()
        if "/en/" in file_path:
            new_text = new_text.lower()
        
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

def remove_lang_sufix(filename):
    text_list = filename.split('.')
    if len(text_list)==2:
        extension = text_list[-1]
        text_list = text_list[:-1]
    else:
        extension = text_list[-1]
        text_list = text_list[:-2]

    return f"{".".join(text_list)}.{extension}"