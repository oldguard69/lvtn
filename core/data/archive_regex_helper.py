import re
from typing import Set

intab_l = "ạảãàáâậầấẩẫăắằặẳẵóòọõỏôộổỗồốơờớợởỡéèẻẹẽêếềệểễúùụủũưựữửừứíìịỉĩýỳỷỵỹđ"
ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'
digits = '0123456789'
punctuation = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
whitespace = ' '
accept_strings =  intab_l + ascii_lowercase + digits + punctuation + whitespace
invalid_vietnamese_chars = re.compile('^[^' + accept_strings + ']+$')


# find special character
def find_invalid_unicode_character(text: str) -> Set:
    '''Return a set of non-word characters get from text'''
    invalid_char = set()
    punctuation_set = set("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~\n\t""")
    s = re.sub('\w+', '', text) # replace alphanumeric word character with non-string
    for char in s:
        if char not in punctuation_set:
            invalid_char.add(char)
    return invalid_char



# invalid_char = ''
# with open('/content/drive/MyDrive/data/invalid_chars.txt', 'r', encoding='utf-8') as f:
#     for char in f.readlines():
#         invalid_char += char.replace('\n', '')
# r2 = re.compile('[' + invalid_char + ']')


