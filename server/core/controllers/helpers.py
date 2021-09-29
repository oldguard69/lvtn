import os
from flask import jsonify
from core.util.file_manager import file_manager


def get_response_for_request_file_sentences(corpus_dir, filename):
    sentences = file_manager.read_line_by_line(
        os.path.join(corpus_dir, filename)
        )
    response = jsonify(sentences=sentences)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


from core.util.word_segmenter import word_segmenter

t = 'Nghe không biết bao nhiêu lần rồi .. giọng của ca sĩ Khánh Hà lại thêm hoà âm của Asia thật sự là một tuyệt phẩm, càng nghe càng thấy da diết đến lạ'
print(word_segmenter.segment_word(t))