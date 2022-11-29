# This script converts .smi or .srt into pdf for English study

from fpdf import FPDF as PDF
from reader import SUBTITLES_READER
OUTPUT_DIR    = './results'
SUBTITLES_DIR = './subtitles'

#f'{SUBTITLES_DIR}/Wednesday.S01E01.1080p.NF.WEB-DL.DDP5.1.Atmos.H.264-SMURF_en.srt'
#f'{SUBTITLES_DIR}/Wednesday.S01E01.Wednesdays.Child.is.Full.of.Woe.1080p.NF.WEB-DL.DDP5.1.Atmos.H.264-SMURF_ko.srt'
#f'{SUBTITLES_DIR}/Desperate.Housewives-S01E02.HDTV.XviD_en.smi'
#f'{SUBTITLES_DIR}/Desperate.Housewives-S01E02.HDTV.XviD_ko.smi'

# target1 = f'{SUBTITLES_DIR}/Wednesday.S01E01.1080p.NF.WEB-DL.DDP5.1.Atmos.H.264-SMURF_en.srt'
# target2 = f'{SUBTITLES_DIR}/Wednesday.S01E01.Wednesdays.Child.is.Full.of.Woe.1080p.NF.WEB-DL.DDP5.1.Atmos.H.264-SMURF_ko.srt'
# reader = SUBTITLES_READER()
# reader.setting([target1, target2], ('en', 'ko'))

target = f'{SUBTITLES_DIR}/연희공략01.xlsx'
reader = SUBTITLES_READER()
reader.setting([target], ('cn', 'ko'))

texts = reader.decode()
target1, target2 = texts.keys()

pdf = PDF(format='A4') 
pdf = PDF(orientation='P', unit='mm', format='A4')
pdf.add_page()
pdf.add_font('ArialUnicode', fname='Arial-Unicode-Regular.ttf', uni=True)
pdf.set_font('ArialUnicode', '', 11)
for idx in range(len(texts[target1])):    
    pdf.cell(200, 11, txt=texts[target1][idx], ln=1)#, align='C')
    pdf.cell(200, 11, txt=texts[target2][idx], ln=1)#, align='C')
    #pdf.cell(200, 10, txt='', ln=1, align='C')
pdf.output(f'{OUTPUT_DIR}/연희공략01.pdf', 'F')