import os

import pysrt
from googletranslatepy import Translator
from tqdm import tqdm

def translate_srt_file(file_path, src_lang, dest_lang, out_file):
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
