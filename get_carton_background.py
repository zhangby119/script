import os
import json
import random

import cv2

img_dir = './back_ground/'
img_save_dir = './segment_img/'

output_height = 640
output_width = 640

is_img_dir_exist = os.path.exists(img_dir)
if not is_img_dir_exist:
    os.mkdir(img_dir)

img_list = os.listdir(img_dir)
is_dir_exist = os.path.exists(img_save_dir)
if not is_dir_exist:
    os.mkdir(img_save_dir)

for img_name in img_list:
    img_path = os.path.join(img_dir, img_name)
    img = cv2.imread(img_path)
    # cv2.imshow("img",img)
    # cv2.waitKey()
    size = img.shape
    img_width = size[1]
    img_height = size[0]
    print(img_height)
    print(img_width)

    width_range = img_width - output_width
    height_range = img_height - output_height
    print(width_range)
    print(height_range)
    print("------------------------------")
    #sample1 top x,y point
    sample_1_x_seed = random.random()
    sample_1_y_seed = random.random()
    sample_1_x = width_range * sample_1_x_seed
    sample_1_y = height_range * sample_1_y_seed

    sample_1_img = img[int(sample_1_y):(int(sample_1_y) + output_height), int(sample_1_x):(int(sample_1_x) + output_width)]
    sample_1_name = img_name[:-4] + "_background_1.jpg"
    sample_1_path = os.path.join(img_save_dir, sample_1_name)
    cv2.imwrite(sample_1_path, sample_1_img)

    # sample2 top x,y point
    sample_2_x_seed = random.random()
    sample_2_y_seed = random.random()
    sample_2_x = width_range * sample_2_x_seed
    sample_2_y = height_range * sample_2_y_seed

    sample_2_img = img[int(sample_2_y):(int(sample_2_y) + output_height), int(sample_2_x):(int(sample_2_x) + output_width)]
    sample_2_name = img_name[:-4] + "_background_2.jpg"
    sample_2_path = os.path.join(img_save_dir, sample_2_name)
    cv2.imwrite(sample_2_path, sample_2_img)

