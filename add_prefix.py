import os

date_stamp = '0723_300_4'
this_dir_path = './'
for file in os.listdir(this_dir_path):
    file_path = os.path.join(this_dir_path, file)
    file_name = os.path.splitext(file_path.split('/')[-1])[0]
    new_file_path = this_dir_path + date_stamp + '_' + file_name + os.path.splitext(file_path)[-1]
    print(file_path+'---->'+new_file_path)
    os.rename(file_path, new_file_path)
