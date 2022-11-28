import os

class SUBTITLES_READER(object):
    def __init__(self, subtitles_path1:str, subtitles_path2:str, lang:tuple):
        self.path1 = subtitles_path1
        self.path2 = subtitles_path2
        self.sub_type1 = os.path.splitext(self.path1)[1]
        self.sub_type2 = os.path.splitext(self.path2)[1]
        assert self.sub_type1 == self.sub_type2, 'Ext of two subtitles are different.'
        self.sub_type = self.sub_type1
        self.lang = lang
        
    def decode(self) -> dict:
        if self.sub_type == '.smi':
            return {self.lang[0]:self._smi_decode(self.path1), self.lang[1]:self._smi_decode(self.path2)}
        elif self.sub_type == '.srt':
            text1, text2 = self._join_twosrt(self._srt_decode(self.path1), self._srt_decode(self.path2))
            return {self.lang[0]:text1, self.lang[1]:text2}
        else:
            print("Wrong type subtitle!")
            exit()
    
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
    
    def _smi_decode(self, path):
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

    def _srt_decode(self, path):
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