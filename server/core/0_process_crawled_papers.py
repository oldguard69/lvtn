# NOTE: this file is for showing how crawl paper process look like
# The webpage may change and break the code

import os

from langdetect import detect

from util.web_crawler import web_crawler
from util.file_manager import file_manager
from util.text_cleaner import text_cleaner
from .directory import stdj_dir

pdf_folder = os.path.join(stdj_dir, 'pdf')
clean_txt_folder = os.path.join(stdj_dir, 'clean_txt')
raw_txt_folder = os.path.join(stdj_dir, 'raw_txt')


def get_issue_detail_urls():
    urls = []
    root_url = 'http://stdj.scienceandtechnology.com.vn/index.php/stdj/issue/archive?issuesPage={page}#issues'
    for i in range(1, 8):
        root_page = web_crawler.fecth_and_parse_page_content(root_url.format(page=i))
        issue_summary = root_page.select('.issue-summary.media')
        for issue in issue_summary:
            link = issue.select_one('.title').get('href')
            urls.append(link)
        web_crawler.sleep(f'issue page {i}')
    return urls

def get_paper_urls_of_an_issue(issue_url):
    result = []
    issue_detail = web_crawler.fecth_and_parse_page_content(issue_url)
    link_elements = issue_detail.select('.obj_galley_link.pdf')
    for e in link_elements:
        result.append(e.get('href'))
    return result


issue_urls = get_issue_detail_urls()
print(f'Total issue detail page: {len(issue_urls)}')

paper_urls_file = os.path.join(stdj_dir, 'paper_urls.txt')
fetched_paper_urls_file = os.path.join(stdj_dir, 'fetched_paper_urls.txt')

"""Duyệt qua mỗi issue_url trong issue_urls
trong mỗi issue_url, lấy hết paper_urls
"""
paper_urls = []
for i, issue_url in enumerate(issue_urls):
    urls = get_paper_urls_of_an_issue(issue_url)
    paper_urls.extend(urls)
    web_crawler.sleep(f'issue detail {i}, total paper_urls: {len(paper_urls)}', 1, 3)

    file_manager.append_url_list_to_file(paper_urls_file, urls)


# download paper in pdf format
i = 0
for url in paper_urls:
    page = web_crawler.fecth_and_parse_page_content(url)
    download_link = page.select_one('.download').get('href')
    web_crawler.download_pdf_file(os.path.join(pdf_folder, f'{i}.pdf'), download_link)
    file_manager.append_url_to_file(fetched_paper_urls_file, url)
    web_crawler.sleep(f'{i}.pdf', 1, 3)
    i += 1




def is_non_vn(text):
    return detect(text) != 'vi'


done_files = os.path.join(stdj_dir, 'done_files.txt')
error_files = os.path.join(stdj_dir, 'error_files.txt')

# convert pdf to raw_txt and clean_txt
for file in os.listdir(pdf_folder):
    text_file_name = 'file_{}.txt'.format(file[:-4])
    pdf_file = os.path.join(pdf_folder, file)
    try:
        raw_text = web_crawler.convert_pdf_to_raw_txt(pdf_file)
        raw_text_file = os.path.join(raw_txt_folder, text_file_name)
        file_manager.write_whole_file(raw_text_file, raw_text)

        clean_text = text_cleaner.remove_invalid_unicode(raw_text)
        clean_text_file = os.path.join(clean_txt_folder, text_file_name)
        file_manager.write_whole_file(clean_text_file, clean_text)

        if clean_text == '':
            raise ValueError()
        else:
            if is_non_vn(clean_text):
                raise ValueError()
            else:
                file_manager.write_lines(done_files, file)
                print(f'File {file} is ok')
    except:
        # os.remove(os.path.join(pdf_folder, file))
        file_manager.write_lines(error_files, file)
        print(f'File {file} is error')