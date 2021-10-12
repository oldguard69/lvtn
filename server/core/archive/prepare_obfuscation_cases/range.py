# import os
# from util.file_manager import file_manager

# while True:
#     s = input('Nhap so: ')
#     if s == 'q':
#         break
#     json_file = 'susp_{}.json'.format(s)
#     txt_file = 'susp_{}.txt'.format(s)
#     stats = file_manager.read_json(
#         os.path.join('..', 'corpus', 'susp_stats', json_file)
#     )['file_stats']
#     sents = file_manager.read_line_by_line(
#         os.path.join('..', 'corpus', 'susp', txt_file)
#     )
#     contents = []
#     for item in stats:
#         start = item["susp_index"]
#         end = start + item['paragraph_length']
#         print(f'{start} -> {end}')
#         for i in range(start, end):
#             content = f'{i + 1}: {sents[i]}\n->\n'
#             # print(content)
#             contents.append(content)
#     print('='*100)
#     file_manager.write_lines('t.txt', contents)



import os
from util.file_manager import file_manager

ss = file_manager.read_line_by_line('ob_susp.txt')
ss = [s.split('.')[0].split('_')[1] for s in ss]

contents = []
for s in ss:
    json_file = 'susp_{}.json'.format(s)
    txt_file = 'susp_{}.txt'.format(s)
    stats = file_manager.read_json(
        os.path.join('..', 'corpus', 'susp_stats', json_file)
    )['file_stats']
    sents = file_manager.read_line_by_line(
        os.path.join('..', 'corpus', 'susp', txt_file)
    )
    contents.append(f'{txt_file}\n')
    print(f'{txt_file}')
    
    for item in stats:
        start = item["susp_index"]
        end = start + item['paragraph_length']
        print(f'{start+1} -> {end}')
        contents.append(f'{start+1} -> {end}')

        for i in range(start, end):
            line = f'{i + 1}: {sents[i]}\n->\n'
            contents.append(line)
    print('='*100)
file_manager.write_lines('t.txt', contents)
