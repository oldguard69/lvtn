import json


class FileManager:
    def __init__(self, encoding='utf-8-sig'):
        self.encoding = encoding

    # *** core method ***
    def write_line(self, file, content):
        '''Append content in a new line'''
        with open(file, 'a', encoding=self.encoding) as f:
            f.write(f'{content}\n')

    def write_whole_file(self, file, content):
        '''WARNING: this function will overwrite content of old file if it exists'''
        with open(file, 'w', encoding=self.encoding) as f:
            f.write(content)

    def read_line_by_line(self, file):
        r = []
        with open(file, 'r', encoding=self.encoding) as f:
            for line in f.readlines():
                r.append(line.replace('\n', ''))
        return r

    def read_whole_file(self, file):
        with open(file, 'r', encoding=self.encoding) as f:
            text = f.read()
        return text

    
    # *** urls file manipulation ***
    def append_url_list_to_file(self, filepath, urls):
        with open(filepath, 'a') as f:
            for u in urls:
                f.write(f'{u}\n')
    
    def append_url_to_file(self, filepath, url):
        with open(filepath, 'a') as f:
            f.write(f'{url}\n')

    def read_urls(self, filepath):
        return self.read_line_by_line(filepath)

    # *** json file manipulation ***
    def write_json(self, file, content):
        with open(file, 'w') as f:
            json.dump(content, f)
    
    def read_json(self, file):
        with open(file, 'r') as f:
            return json.load(f)

    

file_manager = FileManager()