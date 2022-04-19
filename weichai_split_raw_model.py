import os
import json
import re
import shutil

import cv2

root_dir = 'C:/Users/zhangBY/Desktop/新建文件夹'
img_list = os.listdir(root_dir)

exist_models = []
for img_name in img_list:
    img_path = os.path.join(root_dir, img_name)
    temp = re.split('[._]', img_name)
    model_name = temp[-3] + '_' + temp[-2]
    model_path = os.path.join(root_dir, model_name)
    if not os.path.exists(model_path):
        os.mkdir(model_path)
    new_img_path = os.path.join(model_path, img_name)
    shutil.move(img_path, new_img_path)
    # print(model_path)
    # print(temp)
