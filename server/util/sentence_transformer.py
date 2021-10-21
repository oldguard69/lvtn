import torch
import os
import numpy as np
from transformers import AutoModel, AutoTokenizer

from util.file_manager import file_manager
from util.text_cleaner import text_cleaner
from util.word_segmenter import word_segmenter


class SentenceTransformer:
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

    def encode(self, word_segmented_sentences, batch_size=128, seq_len=256):
        # compute sentence embedding for each batch_size sentences at a time
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

        # convert from tensor to numpy array
        all_embeddings = np.asarray([emb.numpy() for emb in all_embeddings])
        return all_embeddings
    
    def encode_whole_doc(self, word_segmented_sentences, seq_len=256):
        # encode the whole document
        tokens = self.tokenize_sentences(word_segmented_sentences, seq_len)
        token_embeddings = self.compute_embedding_tokens(tokens)
        embeddings = self.mean_pooling(token_embeddings, tokens['attention_mask'])
        embeddings = embeddings.cpu().numpy()
        return embeddings

    def compute_embedding_of_a_doc(self, corpus_dir, file, batch_size=None):
        # read doc line by line, remove punctuation and lower character, segment word and then compute embedding
        sentences = file_manager.read_line_by_line(os.path.join(corpus_dir, file))
        sentences = [text_cleaner.remove_punctuation(text_cleaner.lowercase(sent)) for sent in sentences]
        word_segmented_sentences = [word_segmenter.segment_word(sent) for sent in sentences]
        if batch_size:
            embeddings = self.encode(word_segmented_sentences, batch_size)
        else:
            embeddings = self.encode_whole_doc(word_segmented_sentences)
        del sentences, word_segmented_sentences
        
        result = []
        for index, embedding in enumerate(embeddings):
            result.append({
                'filename': file,
                'index': index,
                'embedding': embedding
            })
        return result


# Set device for using gpu
cuda = True
device = torch.device("cuda" if (
    torch.cuda.is_available() and cuda) else "cpu")
torch.set_default_tensor_type("torch.FloatTensor")
if device.type == "cuda":
    torch.set_default_tensor_type("torch.cuda.FloatTensor")
print(device)


local_model_directory = 'C:/Users/jeanLannes/workstation/lvtn/server/util/model/phobert_using_transformer'
tokenizer = AutoTokenizer.from_pretrained(local_model_directory)
phobert = AutoModel.from_pretrained(local_model_directory)

phobert.eval()

sentence_transfomer = SentenceTransformer(phobert, tokenizer)