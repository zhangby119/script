import os
import shutil

prefix = '0915_second_factory_temp_'
this_dir_path = './'
aim_dir = './raw_data/'
i = 0
for file in os.listdir(this_dir_path):
    file_path = os.path.join(this_dir_path, file)
    file_name = os.path.splitext(file_path.split('/')[-1])[0]
    # new_file_path = this_dir_path + date_stamp + '_' + file_name + os.path.splitext(file_path)[-1]
    # print(file_name)
    if file_name.startswith("Images_"):
        img_dir = file_path + "/"
        # print(img_dir)
        img_list = os.listdir(img_dir)
        # print(img_list)
        for img in img_list:
            new_img = prefix + "%s" % i + ".jpg"
            i = i + 1
            img_path = os.path.join(img_dir, img)
            new_img_path = os.path.join(aim_dir, new_img)
            shutil.copy(img_path, new_img_path)
            # print(new_img)
            # print(img_path)
    # os.rename(file_path, new_file_path)
