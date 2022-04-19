import os
import random
import shutil




image_dir = './data/'
background_dir = './back_ground/'

background_dir_exist = os.path.exists(background_dir)
if not background_dir_exist:
    os.mkdir(background_dir)


file_list = os.listdir(image_dir)


for file_name in file_list:
    if file_name.endswith("jpg"):
        name = file_name[:-3]
        json_name = name + "json"
        if json_name not in file_list:
            aim_img_path = os.path.join(background_dir, file_name)
            resource_path = os.path.join(image_dir, file_name)
            shutil.move(resource_path, aim_img_path)
            print(file_name)

