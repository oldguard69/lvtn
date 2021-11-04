import os
from util.file_manager import file_manager

all_susps = set(file_manager.read_line_by_line(os.path.join('..', '..', 'stats_about_files', 'susp_for_train_model.txt')))

done_susp = file_manager.read_line_by_line('train_classification_model.log')
done_susp = set([i.split(' ')[0] + '.txt' for i in done_susp])

remain = all_susps.difference(done_susp)
file_manager.write_lines('remain.txt', remain)