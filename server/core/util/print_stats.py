def print_stats(stats, column_size=25):
    def padding_space(string,  column_size=25):
        string = str(string)
        t = column_size - len(string)
        r = int(t // 2)
        if t % 2:
            s = ' '*r + string + ' '*(r+1)
        else:
            s = ' '*r + string + ' '*r   
        return s

    width = column_size * 4 + 5
    print('='*width)
    for i in ['src_file', 'start_index', 'insert_index', 'paragraph_len']:
        print('|' + padding_space(i, column_size), end='')
    print('|')
    print('='*width)

    for item in stats:
        for key in ['src_file', 'start_index', 'insert_index', 'paragraph_len']:
            print("|" + padding_space(item[key], column_size), end='')
        print('|')
        print('='*width)


# stats = [{'insert_index': 28,
#   'paragraph_len': 48,
#   'src_file': 'src_1.txt',
#   'start_index': 23},
#  {'insert_index': 126,
#   'paragraph_len': 17,
#   'src_file': 'src_4.txt',
#   'start_index': 135},
#  {'insert_index': 173,
#   'paragraph_len': 8,
#   'src_file': 'src_0.txt',
#   'start_index': 77}]
# print_stats(stats)