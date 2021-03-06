from os.path import join as osjoin

from langdetect import detect
import nltk
# nltk.download('punkt')
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

    vn_sentences_only = [sent for sent in merged_sents if detect(sent) == 'vi']

    file_manager.write_whole_file(f'corpus/raw_text/raw_{unique_name}.txt', raw_text)
    file_manager.write_whole_file(f'corpus/raw_text/clean_{unique_name}.txt', clean_text)
    return vn_sentences_only


def get_vn_only_sentences(txt_file):
    sents = file_manager.read_line_by_line(txt_file)
    vn_sentences_only = [sent for sent in sents if detect(sent) == 'vi']
    return vn_sentences_only
