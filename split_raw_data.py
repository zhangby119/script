import math
import os
import random
import shutil


number_of_workers = 2
dir_list = []
image_dir = './img/'

for i in range(number_of_workers):

    # temp_dir = './' + i + '/'
    temp_dir = './%d/' % i
    dir_list.append(temp_dir)
    os.mkdir(temp_dir)
print(dir_list)

img_list = os.listdir(image_dir)
img_num = len(img_list)
print(img_num)
number_of_pics_per_people = img_num / number_of_workers
number_of_pics_per_people = math.floor(number_of_pics_per_people)

img_list_2 = img_list

for i in range(number_of_workers - 1):
    temp_sample = random.sample(img_list, number_of_pics_per_people)
    img_list = list(set(img_list) - set(temp_sample))
    print(len(temp_sample))
    for img_name in temp_sample:
        image_path = image_dir + '/' + img_name
        img_save_path = dir_list[i] + img_name
        shutil.copy(image_path, img_save_path)

print(len(img_list))
for img_name in img_list:
    image_path = image_dir + '/' + img_name
    img_save_path = dir_list[number_of_workers-1] + img_name
    shutil.copy(image_path, img_save_path)
