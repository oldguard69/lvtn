import os
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
        return ' '.join([' '.join(i) for i in word_segmenter.tokenize(single_sentence)])


model_dir = os.path.abspath('C:/Users/jeanLannes/workstation/lvtn/server/util/model/vncorenlp/VnCoreNLP-1.1.1.jar')
vncorenlp_model =  VnCoreNLP(
    model_dir, annotators="wseg", max_heap_size='-Xmx500m'
)

word_segmenter = WordSegmenter(vncorenlp_model)