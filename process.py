import pysrt
from tqdm import tqdm


def post_process_srt(file_path):
    print("Processing:", file_path)

    subs = pysrt.open(file_path, encoding="utf-8")

    for subtitle in tqdm(subs, desc="Translating subtitle"):
        original_text = subtitle.text
        new_text = original_text.replace("&nbsp","").replace("&NBSP","").replace(";","").replace("♪","").replace("  ","").strip()
        if "/pt/" in file_path:
            new_text = new_text.upper()
        
        subtitle.text = new_text

    subs.save(file_path, encoding="utf-8")
    


    
