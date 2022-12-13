from dataclasses import dataclass
import os

sep = os.path.sep

@dataclass
class convertConfig:

    # You have to modify these settings.
    fonts_dir     = './fonts'
    output_dir    = './results'
    subtitles_dir = './subtitles'

    subtitle01    = '.srt'
    subtitle02    = '.srt'
    output_file   = '.pdf'
    font_file     = 'Arial-Unicode-Regular.ttf'
    add_line      = False
    target_lang   = ['en', 'ko'] 

    # You don't need to modify these settings, but if you want to convert .xlsx or .smi format, then modify these settings.
    target_path   = [subtitles_dir+sep+subtitle01, subtitles_dir+sep+subtitle02]
    output_path   = output_dir+sep+output_file
    font_path     = fonts_dir+sep+font_file
