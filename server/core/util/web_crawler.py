import os
import requests
import bs4 as BeautifulSoup
import random
import time
import textract

from util.file_manager import file_manager
from util.text_cleaner import processor


class WebCrawler:
    def __init__(self): pass

    # *** crawl web ***
    def download_pdf_file(self, file, url, verify=True):
        r = requests.get(url, allow_redirects=True, verify=verify)
        with open(file, 'wb') as f:
            f.write(r.content)

    def fecth_and_parse_page_content(self, url, verify=True):
        s = requests.Session()
        page_content = s.get(url, verify=verify).content
        return BeautifulSoup(page_content, 'html.parser')
    
    def sleep(self, file, lower_bound, upper_bound):
        sleep_time = random.randint(lower_bound, upper_bound)
        print(f'{file} -- sleep in {sleep_time}s')
        time.sleep(sleep_time)


    # *** convert pdf to text ***
    def convert_pdf_to_raw_txt(self, pdf_file):
        text = textract.process(pdf_file, language='eng')
        text = text.decode('utf-8')
        return text

    def convert_all_pdf_to_txt(self, pdf_folder, clean_text_folder, raw_text_foler, save_raw_text=False):
        for file in os.listdir(pdf_folder):
            print(file) # file is similar to 'paper_01.pdf'
            text_file_name = file.split('.')[0] + '.txt'
            pdf_file = os.path.join(pdf_folder, file)
            raw_text = self.convert_pdf_to_raw_txt(pdf_file)

            if save_raw_text:
                raw_text_file = os.path.join(raw_text_foler, text_file_name)
                file_manager.write_whole_file(raw_text_file, raw_text)

            clean_text = processor.remove_invalid_unicode(raw_text)
            clean_text_file = os.path.join(clean_text_folder, text_file_name)
            file_manager.write_whole_file(clean_text_file, clean_text)

    def check_invalid_chars_in_text_folder(self, folder):
        all_file = os.listdir(folder)
        contain_invalid_chars_file = 0
        for file in all_file:
            text = file_manager.read_whole_file(os.path.join(folder, file))
            invalid_chars = processor.find_invalid_unicode_chars(text)
            if len(invalid_chars):
                print(f"file {file} -- {''.join(invalid_chars)}")
                contain_invalid_chars_file += 1
            else:
                print(f'file {file} does not contain invalid chars')
        print(f'total file: {len(all_file)}, file contain invalid char: {contain_invalid_chars_file}')

web_crawler = WebCrawler()