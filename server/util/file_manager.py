import json
import pickle
import os
from typing import List
import textract

class FileManager:
    def __init__(self, encoding='utf-8-sig'):
        self.encoding = encoding

    # *** core method ***
    def append_single_line(self, file: str, content: str):
        '''Append content in a new line'''
        with open(file, 'a', encoding=self.encoding) as f:
            f.write(f'{content}\n')

    def write_lines(self, file: str, contents: List[str]):
        """
        WARNING: this function will overwrite content of old file if it exists
        Write each item in contents in newline.
        """
        with open(file, 'w', encoding=self.encoding) as f:
            for line in contents:
                f.write(f'{line}\n')

    def write_whole_file(self, file: str, content: str):
        """
        WARNING: this function will overwrite content of old file if it exists
        Overwrite content into file
        """
        with open(file, 'w', encoding=self.encoding) as f:
            f.write(content)

    def read_line_by_line(self, file: str) -> List[str]:
        r = []
        with open(file, 'r', encoding=self.encoding) as f:
            for line in f.readlines():
                r.append(line.replace('\n', ''))
        return r

    def read_whole_file(self, file: str) -> str:
        with open(file, 'r', encoding=self.encoding) as f:
            text = f.read()
        return text

    
    # *** urls file manipulation ***
    def append_url_list_to_file(self, file: str, urls: List[str]):
        """
        Append a list of urls to file
        """
        with open(file, 'a') as f:
            for u in urls:
                f.write(f'{u}\n')
    
    def append_url_to_file(self, file: str, url: str):
        """
        Append a url to file
        """
        with open(file, 'a') as f:
            f.write(f'{url}\n')

    def read_urls(self, file: str) -> List[str]:
        return self.read_line_by_line(file)

    # *** json file manipulation ***
    def write_json(self, file: str, content: any):
        with open(file, 'w') as f:
            json.dump(content, f)
    
    def read_json(self, file: str) -> any:
        with open(file, 'r') as f:
            return json.load(f)

    # *** pickcle file ***
    def pickle_dump(self, object: any, file: str):
        with open(file, 'wb') as f:
            pickle.dump(object, f)

    def pickle_load(self, file: str) -> any:
        with open(file, 'rb') as f:
            return pickle.load(f)

    # *** listdir ***
    def sort_files(self, files):
        def get_file_number(file): # file = src_1.txt
            return int(file.split('.')[0].split('_')[1])
        return sorted(files, key=lambda file: get_file_number(file))

    def listdir_and_sort(self, dir: str) -> List[str]:
        """List all files in dir and sort them by their name"""
        return self.sort_files(os.listdir(dir))

    def convert_pdf_to_txt(self, pdf_file):
        text = textract.process(pdf_file, language='eng')
        text = text.decode('utf-8')
        return text



file_manager = FileManager()