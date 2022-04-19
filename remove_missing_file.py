import os
import json


json_dir = './'
json_files = os.listdir(json_dir)
img_save_dir = './segment_img/'

is_dir_exist = os.path.exists(img_save_dir)
if not is_dir_exist:
    os.mkdir(img_save_dir)

for json_file in json_files:

    json_file_path = json_dir + '/' + json_file

    img_file_name = json_file[:-4]+"jpg"
    img_file_path = json_dir + '/' + img_file_name
    img_save_path = img_save_dir + '/' + img_file_name

    if json_file_path.endswith('json'):
    # 读单个json文件
        if not os.path.exists(img_file_path):
            os.remove(json_file_path)