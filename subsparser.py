import os
import pandas as pd

class SUBTITLES_PARSER(object):
    def __init__(self):
        pass

    def setting(self, subtitles_paths:list, lang:tuple):
        n = len(subtitles_paths)
        if n == 2:
            self.path1 = subtitles_paths[0]
            self.path2 = subtitles_paths[1]
            self.sub_type1 = os.path.splitext(self.path1)[1]
            self.sub_type2 = os.path.splitext(self.path2)[1]
            assert self.sub_type1 == self.sub_type2, 'Ext of two subtitles are different.'
            self.sub_type = self.sub_type1
        elif n == 1:
            self.path = subtitles_paths[0]
            self.sub_type = os.path.splitext(self.path)[1]
            assert self.sub_type == '.xlsx', 'Ext is not Netflix xlsx'
        self.lang = lang

    def parser(self) -> dict:
        if self.sub_type == '.smi':
            return {self.lang[0]:self._smi_parser(self.path1), self.lang[1]:self._smi_parser(self.path2)}
        elif self.sub_type == '.srt':
            text1, text2 = self._join_twosrt(self._srt_parser(self.path1), self._srt_parser(self.path2))
            return {self.lang[0]:text1, self.lang[1]:text2}
        elif self.sub_type == '.xlsx':
            text1, text2 = self._xlsx_parser(self.path)
            return {self.lang[0]:text1, self.lang[1]:text2}
        else:
            print("Wrong type subtitle!")
            exit()
    
    def _xlsx_parser(self, path):
        df = pd.read_excel(path)
        return df['Subtitle'].to_list(), df['Translation'].str.replace('\n',' ').str.replace('\u200e','').to_list()

    def _join_twosrt(self, dict1, dict2):
        set1 = set(dict1.keys())
        set2 = set(dict2.keys())
        unionset = set1.intersection(set2)
        text1 = []
        text2 = []
        for key in dict1.keys():
            if key in unionset:
                text1.append(dict1[key])
                text2.append(dict2[key])
        return text1, text2
    
    def _smi_parser(self, path):
        try:
            f = open(path, 'r')
            rawtexts = f.readlines()
        except:
            f = open(path, 'r', encoding='euc-kr')
            rawtexts = f.readlines()
        text = []
        temp_text = ''
        start_flag = False
        for rawtext in rawtexts:
            if 'SYNC' in rawtext:
                start_flag = True
                if temp_text != '':
                    text.append(temp_text)
                temp_text = ''                
                continue
            if '<font' in rawtext:            
                continue
            if start_flag:
                rawtext = rawtext.replace('\n', '')  
                rawtext = rawtext.replace('<br>', ' ')  
                rawtext = rawtext.replace('-', ' ')                  
                rawtext = rawtext.replace("'   ", '')                 
                rawtext = rawtext.replace("'  ", '')            
                rawtext = rawtext.replace("' ", '')          
                rawtext = rawtext.replace("    ", ' ')    
                rawtext = rawtext.replace("   ", ' ')    
                rawtext = rawtext.replace("  ", ' ')  
                temp_text += rawtext.replace('\n', '')            
        f.close()
        return text

    def _srt_parser(self, path):
        f = open(path, 'r')
        rawtexts = f.readlines()
        texts = {}
        temp_text = ''
        start_flag = False
        for rawtext in rawtexts:
            rawtext = rawtext.rstrip()
            if '-->' in rawtext:
                key = rawtext
                start_flag = True
                continue
            if start_flag:      
                if '' == rawtext:
                    texts[key] = temp_text
                    temp_text = ''
                    start_flag = False
                else:
                    temp_text += ' ' + rawtext.replace('<i>', '').replace('</i>', '').replace('\u200e', '')
        return texts