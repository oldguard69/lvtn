def get_all_src_files(stats):
    return list(set([s['src_file'] for s in stats]))

def get_index_range(begin_index, length):
    return set([i for i in range(begin_index, begin_index + length)])

def is_overlap(potential_stats, current_stats):
    prev_src_index = get_index_range(
        potential_stats['src_start_index'], potential_stats['src_paragraph_length']
        )
    prev_susp_index = get_index_range(
        potential_stats['susp_insert_index'], potential_stats['susp_paragraph_length']
        )
    current_src_index = get_index_range(
        current_stats['src_start_index'], current_stats['paragraph_length']
        )
    current_susp_index = get_index_range(
        current_stats['susp_insert_index'], current_stats['paragraph_length']
        )
    # Nếu chỉ số trong hai đoạn nguồn giao nhau
    # và chỉ số trong hai đoạn nghi ngờ giao nhau
    if len(prev_src_index.intersection(current_src_index)) and \
       len(prev_susp_index.intersection(current_susp_index)):
       return True
    return False

def initialize_potential_stats(current_stats):
    return  {
        'src_file': current_stats['src_file'],
        'src_start_index': current_stats['src_start_index'],
        'src_paragraph_length': current_stats['paragraph_length'],
        'susp_insert_index': current_stats['susp_insert_index'],
        'susp_paragraph_length': current_stats['paragraph_length']
    }

def merge_overlapping_paragraph_of_sub_stats(sub_stats):
    potential_stats = initialize_potential_stats(sub_stats[0])
    # print(potential_stats)
    res = []
    for current_stats in sub_stats:
        if is_overlap(potential_stats, current_stats):
            # Nếu hai đoạn giao nhau thì gộp lại thành đoạn dài nhất
            # Chỉ số bắt đầu của src và susp thì lấy chỉ số nhỏ nhất
            # Độ dài của đoạn thì chọn đoạn dài nhất
            # Đoạn nguồn
            potential_stats['src_start_index'] = min(
                potential_stats['src_start_index'], current_stats['src_start_index']
            )
            potential_stats['src_paragraph_length'] = max( # max: chọn đoạn dài nhất
                potential_stats['src_start_index'] + potential_stats['src_paragraph_length'],
                current_stats['src_start_index'] + current_stats['paragraph_length']
            ) - potential_stats['src_start_index'] # trừ chỉ số của câu bắt đầu đoạn

            # Đoạn nghi ngờ
            potential_stats['susp_insert_index'] = min(
                potential_stats['susp_insert_index'], current_stats['susp_insert_index']
            )
            potential_stats['susp_paragraph_length'] = max(
                potential_stats['susp_insert_index'] + potential_stats['susp_paragraph_length'],
                current_stats['susp_insert_index'] + current_stats['paragraph_length']
            ) - potential_stats['susp_insert_index']
        else:
            res.append(potential_stats)
            potential_stats = initialize_potential_stats(current_stats)
    
    res.append(potential_stats)
    # print(res)
    return list(res)

def merge_overlapping_paragraph(stats):
    result = []
    for src_file in get_all_src_files(stats):
        sub_stats = [s for s in stats if s['src_file'] == src_file]
        result.extend(merge_overlapping_paragraph_of_sub_stats(sub_stats))
    print(f'Before: {len(stats)} --- after: {len(result)}')
    return sorted(result, key=lambda x: x['susp_insert_index'])