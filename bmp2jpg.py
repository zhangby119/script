import os

# this_file_path = __file__
# this_dir_path = os.path.dirname(this_file_path)
this_dir_path = './'
file_list = os.listdir(this_dir_path)

for files in file_list:
    file_path = this_dir_path + '/' + files
    if file_path.endswith('json'):
        new_json_name = files[:-5] + '_gray.json'
        new_json_path = this_dir_path + '/' + new_json_name
        os.rename(file_path, new_json_path)
    if file_path.endswith('bmp'):
        new_img_name = files[:-4] + '_gray.jpg'
        new_img_path = this_dir_path + '/' + new_img_name
        os.rename(file_path, new_img_path)
