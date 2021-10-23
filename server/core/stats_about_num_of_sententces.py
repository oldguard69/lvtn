from collections import defaultdict
from os.path import join as osjoin

from util.file_manager import file_manager
from util.word_segmenter import word_segmenter
from util.text_cleaner import text_cleaner

src_dir = osjoin('..', 'corpus', 'src')
susp_dir = osjoin('..', 'corpus', 'susp')

# num_word_per_sent = defaultdict(int)

# num_sents_per_doc = defaultdict(int)
# for file in file_manager.listdir_and_sort(src_dir):
#     sentences = file_manager.read_line_by_line(osjoin(src_dir, file))
#     num_sents_per_doc[len(sentences)] += 1

#     for sent in sentences:
#         sent = text_cleaner.remove_punctuation(sent)
#         word_segmented_sent = word_segmenter.segment_word(sent)
#         num_word_per_sent[len(word_segmented_sent.split(' '))] += 1

#     print(file)
# file_manager.pickle_dump(num_sents_per_doc, 'src_sent_per_doc.pk')


# num_sents_per_doc = defaultdict(int)
# for file in file_manager.listdir_and_sort(susp_dir):
#     sentences = file_manager.read_line_by_line(osjoin(susp_dir, file))
#     num_sents_per_doc[len(sentences)] += 1

#     for sent in sentences:
#         sent = text_cleaner.remove_punctuation(sent)
#         word_segmented_sent = word_segmenter.segment_word(sent)
#         num_word_per_sent[len(word_segmented_sent.split(' '))] += 1

#     print(file)
# file_manager.pickle_dump(num_sents_per_doc, 'susp_sent_per_doc.pk')

# file_manager.pickle_dump(num_word_per_sent, 'word_per_sent.pk')


result = set()
for dir in [src_dir, susp_dir]:
    for file in file_manager.listdir_and_sort(dir):
        sentences = file_manager.read_line_by_line(osjoin(dir, file))

        for sent in sentences:
            sent = text_cleaner.remove_punctuation(sent)
            word_segmented_sent = word_segmenter.segment_word(sent)
            length = len(word_segmented_sent.split(' '))
            if  length > 500:
                result.add(file)
        print(file)

file_manager.write_lines('extreme_sent_files.txt', list(result))