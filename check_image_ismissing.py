import os
import shutil
img_dir = './data/'

back_ground_dir = './back_ground/'
img_files = os.listdir(img_dir)


for img_file in img_files:

    img_file_path = img_dir + img_file

    # img_file_name = json_file[:-4]+"jpg"
    # img_file_path = json_dir + img_file_name

    if img_file_path.endswith('jpg'):
    # 读单个json文件
        json_file_path = img_file_path[:-3] + "json"
        if not os.path.exists(json_file_path):
            img_new_path = back_ground_dir + img_file
            shutil.copy(img_file_path, img_new_path)


