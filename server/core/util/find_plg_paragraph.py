from pandas import DataFrame

from cosine_similarity import cosine_sim

class PlagiarisedParagraphFinder:
    def __init__(self) -> None:
        pass
    
    def sort(df: DataFrame) -> DataFrame:
        '''Sort dataframe based on susp_index, src_file src_index'''
        df = df.sort_values(by=['susp_index', 'src_file', 'src_index'])
        return df.reset_index(drop=True)

    def match_susp_embeddings_with_src_embeddings(susp_embs, src_embs) -> DataFrame:
        result = []
        for susp_row in susp_embs:
            for src_row in src_embs:
                cosine = cosine_sim(susp_row['embedding'], src_row['embedding'])
                result.append({
                    'src_file': src_row['filename'],
                    'src_index': src_row['index'],
                    'susp_index': susp_row['index'],
                    'cosine_sim': cosine
                })
        return DataFrame(result)

    def get_plagiriarised_sentences(df: DataFrame) -> DataFrame:
        '''Using classifier to get df with plagiarised sentences'''
        pass

    def find_plagirised_paragraph(df: DataFrame):
        pass

    