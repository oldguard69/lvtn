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

    def remove_extra_whitespace(self, text: str) -> str:
        t = self.remove_tab_and_new_line_char(text)
        return re.sub(' +', ' ', t)

    def find_invalid_unicode_chars(self, text):
        '''Invalid unicode chars are characters are not alphanumeric, and don't belong to punctuation_set'''
        invalid_chars = set()
        punctuation_set = set("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~\n\t """)
        s = re.sub('\w+', '', text) # replace alphanumeric word character with non-string
        for char in s:
            if char not in punctuation_set:
                invalid_chars.add(char)
        return invalid_chars
    
    def compile_invalid_chars_to_regex(self, invalid_chars):
        if len(invalid_chars):
            return re.compile('[' + ''.join(invalid_chars) + ']')
        return r''

    def remove_invalid_unicode(self, text: str) -> str:
        invalid_chars = self.find_invalid_unicode_chars(text)
        if len(invalid_chars):
            r = self.compile_invalid_chars_to_regex(invalid_chars)
            return re.sub(r, '', text)
        else:
            # there are no invalid chars, return original text
            return text

processor = TextPreprocessor()