import os
LINE_BREAK = "=" * 50

train_path = './train-1500'
test_path = './test-500'

def file_stats(path):
    total = 0
    for folder in os.listdir(path):
        num_of_file = len(os.listdir(os.path.join(path, folder)))
        total += num_of_file
        print(f'{folder}: {num_of_file} files')
    print(f'Total file in {path}: {total}')

# file_stats(train_path)
# print(LINE_BREAK)
# file_stats(test_path)

print(len(os.listdir('../../corpus/dhct_clean')))