def merge_short_sentence(sent_tokenized_doc: List[str], minimum_len: int) -> List[str]:
    '''Merge sentence with less than minimum_len to the following sentence.
       Merge the last sentence to it's previous sentence if it shorter than minimum_len
    '''
    i = 1 # index of the following sentence
    result = []
    doc_len = len(sent_tokenized_doc)
    current_sent = sent_tokenized_doc[0]
    while True:
        if len(current_sent) < minimum_len:
            if i == doc_len:
                # in case we reach last sentence, keep add current_sent
                # to previous sentence until it's len satisfy condition
                while len(current_sent) < minimum_len:
                    current_sent = result[len(result) - 1] + ' ' + current_sent
                    result[len(result) - 1] = current_sent
            else:
                current_sent += ' ' + sent_tokenized_doc[i]
        else:
            result.append(current_sent)
            if i < doc_len: # move current_sent to the next sentence
                current_sent = sent_tokenized_doc[i]
        if i >= doc_len:
            break
        i += 1

    return result