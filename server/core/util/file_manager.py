import json
import pickle
import os
import h5py


class FileManager:
    def __init__(self, encoding='utf-8-sig'):
        self.encoding = encoding

    # *** core method ***
    def append_single_line(self, file, content):
        '''Append content in a new line'''
        with open(file, 'a', encoding=self.encoding) as f:
            f.write(f'{content}\n')

    def write_lines(self, file, lines):
        with open(file, 'w', encoding=self.encoding) as f:
            for line in lines:
                f.write(f'{line}\n')

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

    # *** pickcle file ***
    def pickle_dump(self, object, file):
        with open(file, 'wb') as f:
            pickle.dump(object, f)

    def pickle_load(self, file):
        with open(file, 'rb') as f:
            return pickle.load(f)

    # *** listdir ***
    def sort_files(self, files):
        def get_file_number(file): # file = src_1.txt
            return int(file.split('.')[0].split('_')[1])
        return sorted(files, key=lambda file: get_file_number(file))

    def listdir_and_sort(self, dir):
        return self.sort_files(os.listdir(dir))

    # *** hdf5 ***
    def hdf5_write(self, file, key, data):
        with h5py.File(file, 'a') as f:
            f.create_dataset(key, data=data)

    def hdf5_read(self, file, key):
        with h5py.File(file, 'r') as f:
            return f[key]
    
    def hdf5_get_keys(self, file):
        with h5py.File(file, 'r') as f:
            return list(f.keys())



file_manager = FileManager()