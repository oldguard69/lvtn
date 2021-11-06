from os.path import join as osjoin

import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
import tika
tika.initVM()
from tika import parser

from util.file_manager import file_manager
from util.text_cleaner import text_cleaner
from util.merge_short_sentences import merge_short_sentence


def convert_pdf_to_txt(pdf_file, unique_name):
    parsed = parser.from_file(pdf_file)
    raw_text = parsed['content']
    clean_text = text_cleaner.remove_invalid_unicode(raw_text)
    
    remove_dup_whitespace_text = text_cleaner.remove_duplicate_whitespace(
        text_cleaner.remove_tab_and_new_line_char(clean_text)
    )
    sents = sent_tokenize(remove_dup_whitespace_text)
    merged_sents = merge_short_sentence(sents, 100)

    file_manager.write_whole_file(f'util/fil/raw_{unique_name}.txt', raw_text)
    file_manager.write_whole_file(f'util/fil/clean_{unique_name}.txt', clean_text)
    # file_manager.write_lines(f'utl/fil/final_{pdf_file[:-4]}.txt', merged_sents)
    return merged_sents


# pdf_file = osjoin('paper_5.pdf')
# convert_pdf_to_txt(pdf_file)
# print('done')