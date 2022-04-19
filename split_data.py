import os
import random
import shutil

train_set_ratio = 0.8
test_set_ratio = 0.1
val_set_ratio = 0.1



image_dir = './data_img/'
label_root = './yolo_label/'

split_store = './split/'
store_dir_exist = os.path.exists(split_store)
if not store_dir_exist:
    os.mkdir(split_store)
train_img_save_path = split_store + 'train_img/'
train_label_save_path = split_store + 'train_label/'
test_img_save_path = split_store + 'test_img/'
test_label_save_path = split_store + 'test_label/'
val_img_save_path = split_store + 'val_img/'
val_label_save_path = split_store + 'val_label/'


is_dir_exist_1 = os.path.exists(train_img_save_path)
if not is_dir_exist_1:
    os.mkdir(train_img_save_path)
is_dir_exist_2 = os.path.exists(test_img_save_path)
if not is_dir_exist_2:
    os.mkdir(test_img_save_path)
is_dir_exist_3 = os.path.exists(val_img_save_path)
if not is_dir_exist_3:
    os.mkdir(val_img_save_path)

is_dir_exist_4 = os.path.exists(train_label_save_path)
if not is_dir_exist_4:
    os.mkdir(train_label_save_path)
is_dir_exist_5 = os.path.exists(test_label_save_path)
if not is_dir_exist_5:
    os.mkdir(test_label_save_path)
is_dir_exist_6 = os.path.exists(val_label_save_path)
if not is_dir_exist_6:
    os.mkdir(val_label_save_path)


imglist = os.listdir(image_dir)
img_num = len(imglist)

test_num = int(img_num*test_set_ratio)
val_num = int(img_num*val_set_ratio)

test_sample = random.sample(imglist, test_num)
train_and_val_sample = list(set(imglist) - set(test_sample))

val_sample = random.sample(train_and_val_sample, val_num)

train_sample = list(set(train_and_val_sample) - set(val_sample))

print(len(val_sample))
print(len(test_sample))
print(len(train_sample))
print(len(imglist))

for val_file_name in val_sample:
    val_label_name = val_file_name[:-3] + 'txt'
    image_path = image_dir + '/' + val_file_name
    label_path = label_root + '/' + val_label_name
    shutil.copy(image_path, val_img_save_path)
    if os.path.exists(label_path):
        shutil.copy(label_path, val_label_save_path)
for test_file_name in test_sample:
    test_label_name = test_file_name[:-3] + 'txt'
    image_path = image_dir + '/' + test_file_name
    label_path = label_root + '/' + test_label_name
    shutil.copy(image_path, test_img_save_path)
    if os.path.exists(label_path):
        shutil.copy(label_path, test_label_save_path)
for train_file_name in train_sample:
    train_label_name = train_file_name[:-3] + 'txt'
    image_path = image_dir + '/' + train_file_name
    label_path = label_root + '/' + train_label_name
    shutil.copy(image_path, train_img_save_path)
    if os.path.exists(label_path):
        shutil.copy(label_path, train_label_save_path)
