# from controllers.check_plagiarism import check_plagiarism, get_number_of_plg_sentences

from util.file_manager import file_manager


# check_plagiarism(1, 'susp_5.txt')
# check_plagiarism(1, 'susp_10.txt')
res = file_manager.read_json('./corpus/production_susp_stats/susp_10.txt_0a2a5960-91bd-4f13-bd0b-59ef70d013f2.json')

def get_number_of_plg_sentences(stats):
    res_set = set()
    for s in stats:
        plg_susp_index = [i for i in range(s['susp_index'], s['susp_index']+s['paragraph_length'])]
        res_set = res_set.union(set(plg_susp_index))
    return len(res_set)
    
print(get_number_of_plg_sentences(res))


