import textract
import re
import os
import requests
from bs4 import BeautifulSoup
import time
import random


# ===================================== get paper url =====================================
urls = [
    'https://sj.ctu.edu.vn/ql/docgia/nam-2015/loaichuyensan-2/xuatban-782.html',
    'https://sj.ctu.edu.vn/ql/docgia/nam-2017/loaichuyensan-2/xuatban-1222/chuyensan-250.html',
    'https://sj.ctu.edu.vn/ql/docgia/nam-2011/loaichuyensan-2/xuatban-182.html',
    'https://sj.ctu.edu.vn/ql/docgia/nam-2013/loaichuyensan-2/xuatban-442/chuyensan-250.html',
    'https://sj.ctu.edu.vn/ql/docgia/nam-2020/loaichuyensan-2/xuatban-2002.html'
    'https://sj.ctu.edu.vn/ql/docgia/nam-2018/loaichuyensan-2/xuatban-1402.html',
    'https://sj.ctu.edu.vn/ql/docgia/nam-2018/loaichuyensan-2/xuatban-1522.html'
]
paper_url = []
for url in urls:
    page = requests.get(url)
    data = BeautifulSoup(page.content, 'html.parser')
    elements = data.select('.div-left.chitiet.grid_05')
    for e in elements:
        paper_url.append(str(e.parent.get("href")))


# ===================================== download pdf file =====================================
def download_file(writefile, url):
    r = requests.get(url, allow_redirects=True)
    with open(writefile, 'wb') as f:
        f.write(r.content)

pdf_folder = '/content/drive/MyDrive/data/dhct'
raw_text_folder = '/content/drive/MyDrive/data/dhct_raw_txt'
clean_text_folder = '/content/drive/MyDrive/data/dhct_clean'

for i, url in enumerate(paper_url):
    sleep_time = random.randint(1, 5)
    print(f'file {i} -- sleep in {sleep_time}s')
    file = os.path.join(pdf_folder, f'paper_{i}.pdf')
    download_file(file, url)
    time.sleep(sleep_time)



# ===================================== convert pdf to raw txt =====================================
def convert_pdf_to_raw_txt(pdf_file, txt_file):
    text = textract.process(pdf_file, language='eng')
    text = text.decode('utf-8')
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write(text)


# convert pdf to raw txt file. Raw mean there are still invalid characters
for file in os.listdir(pdf_folder):
    file_name = file.split('.')[0] + '.txt'
    pdf_file = os.path.join(pdf_folder, file)
    txt_file = os.path.join(raw_text_folder, file_name)
    convert_pdf_to_raw_txt(pdf_file, txt_file)




# ===================================== clean raw data =====================================
from  util.shared import read_file, write_to_file
from .text_preprocessor import TextPreprocessor

processor = TextPreprocessor()

# clean raw text
for file in os.listdir(raw_text_folder):
    text = read_file(os.path.join(raw_text_folder, file))
    text = processor.remove_invalid_unicode(text)
    text = re.sub('Tap chi Khoa hoc Trương Đai hoc Cân Thơ', 'Tạp chí Khoa học Trường Đại học Cần Thơ', text)
    text = re.sub('Trương Đai hoc Cân Thơ', 'Trường Đại học Cần Thơ', text)
    text = re.sub('Trương Đai hoc', 'Trường Đại học', text)
    text = re.sub('Tap chı Khoa hoc Trươ ng Đai hoc Cân Thơ', 'Tạp chí Khoa học Trường Đại học Cần Thơ', text)
    write_to_file(os.path.join(clean_text_folder, file), text)
    print(file)




