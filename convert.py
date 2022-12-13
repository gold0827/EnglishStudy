# This script converts two srt file into a pdf for language study
import warnings
warnings.filterwarnings('ignore')

from fpdf import FPDF as PDF
from subsparser import SUBTITLES_PARSER
from config import convertConfig

config = convertConfig()
reader = SUBTITLES_PARSER()
reader.setting(config.target_path, config.target_lang)
texts = reader.parser()
target1, target2 = texts.keys()

pdf = PDF(orientation='P', unit='mm', format='A4')
pdf.add_page()
pdf.add_font('ArialUnicode', fname=config.font_path, uni=True)
pdf.set_font('ArialUnicode', '', 11)

print("Processing start!")
for idx in range(len(texts[target1])):    
    pdf.cell(200, 11, txt=texts[target1][idx], ln=1)
    pdf.cell(200, 11, txt=texts[target2][idx], ln=1)
    if config.add_line:
        pdf.cell(200, 10, txt='', ln=1, align='C') 
pdf.output(config.output_path, 'F')
print("Done!")