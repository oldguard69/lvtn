from vncorenlp import VnCoreNLP

class WordSegmenter:
    def __init__(self, vncorenlpModel):
        self.vncorenlp = vncorenlpModel
    
    def tokenize(self, single_sentence: str):
        '''
            * work for single sentence only *
            * return: [[]]
        '''
        return self.vncorenlp.tokenize(single_sentence)

    def segment_word(self, single_sentence):
        '''
            * work for single sentence only *
            * return: string
        '''
        return ' '.join(self.tokenize(single_sentence)[0])


vncorenlp_model =  VnCoreNLP(
    './model/vncorenlp/VnCoreNLP-1.1.1.jar', annotators="wseg", max_heap_size='-Xmx500m'
)

word_segmenter = WordSegmenter(vncorenlp_model)

t = 'Nghe không biết bao nhiêu lần rồi .. giọng của ca sĩ Khánh Hà lại thêm hoà âm của Asia thật sự là một tuyệt phẩm, càng nghe càng thấy da diết đến lạ'
print(word_segmenter.segment_word(t))