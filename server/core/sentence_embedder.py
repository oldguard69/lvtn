import torch



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


class SentenceEmbedder:
    def __init__(self, phobert, tokenizer):
        self.phobert = phobert
        self.tokenizer = tokenizer

    def tokenize_sentences(self, word_segmented_sentences, max_seq_len=256):
        '''
            n = len(word_segmented_sentences)
            * return: dict{
                'input_ids': (n, max_seq_len), 
                'token_type_ids': (n, max_seq_len), 
                'attention_mask': (n, max_seq_len)}
        '''
        token = self.tokenizer(
                    word_segmented_sentences, max_length=max_seq_len, truncation=True, 
                    padding='max_length', return_tensors='pt'
                )
        return token

    def compute_embedding_tokens(self, token):
        ''' 
            * token: return value from get_encode_token()
            * return {'last_hidden_state': (num_of_sentences, seq_len, 768), 'pooling': ()}
        '''
        with torch.no_grad():
            return self.phobert(**token)['last_hidden_state']

    def mean_pooling(self, token_embeddings, attention_mask):
        '''
            Using this function in order to get embedding vector for one sentence.
            * embedding: last_hidden_state, shape=(num_of_sentences, seq_len, 768)
            * attention_mask: attention_mask return from tokenizer.encode_plus
            * return: tensor of size (num_of_sentences, 768)
        '''
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)

        sum_mask = input_mask_expanded.sum(1)

        sum_mask = torch.clamp(sum_mask, min=1e-9)

        mean_pooled = sum_embeddings / sum_mask
        return mean_pooled

    # NOTE Depend on the computational power of the GPU, compute the embeddings in batch or whole document
    def encode(self, word_segmented_sentences, batch_size=32, seq_len=256):
        all_embeddings = []
        for start_index in range(0, len(word_segmented_sentences), batch_size):
            # tokenize and compute sentence embedding
            tokens = self.tokenize_sentences(
                word_segmented_sentences[start_index:start_index+batch_size], seq_len
            )
            token_embeddings = self.compute_embedding_tokens(tokens)
            embeddings = self.mean_pooling(token_embeddings, tokens['attention_mask'])

            # convert from cuda tensor to cpu tensor
            embeddings = embeddings.cpu()
            all_embeddings.extend(embeddings)
        return all_embeddings

    
    def encode_whole_doc(self, word_segmented_sentences, seq_len=256):
        tokens = self.tokenize_sentences(word_segmented_sentences, seq_len)
        token_embeddings = self.compute_embedding_tokens(tokens)
        mean_pool = self.mean_pooling(token_embeddings, tokens['attention_mask'])
        return mean_pool