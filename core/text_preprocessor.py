import re

class TextPreprocessor:
    def __init__(self):
        pass

    def lowercase(self, text: str) -> str:
        return text.lower()
    
    def remove_punctuation(self, text: str) -> str:
        '''Because of using sentence tokenize, we dont remove dot'''
        punctuation = r"""[!"#$%&'()*+,-/:;<=>?@[\]^_`{|}~]"""
        return re.sub(punctuation, '', text)
    
    def remove_tab_and_new_line_char(self, text: str) -> str:
        return re.sub('[\n\t]', '', text)

