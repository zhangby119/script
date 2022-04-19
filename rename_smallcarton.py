import os


source_dir = 'C:/Users/zhangBY/Desktop/small_carton/test/'
aim_dir = 'E:/yolo/yolo_carton_dataset_2cls/test/'




aim_img_dir = aim_dir + 'images/'
aim_label_dir = aim_dir + 'labels/'

source_list = os.listdir(source_dir)
aim_img_list = os.listdir(aim_img_dir)
print(source_list)

for img_filename in source_list:
    # print(img_filename)
    label_filename = img_filename.split('.')[0] + '.txt'
    # print(label_filename)
    aim_img_path = aim_img_dir + img_filename
    aim_img_new_path = aim_img_dir + "small_carton_" + img_filename
    aim_label_path = aim_label_dir + label_filename
    aim_label_new_path = aim_label_dir + "small_carton_" + label_filename
    os.rename(aim_img_path, aim_img_new_path)
    os.rename(aim_label_path, aim_label_new_path)
    temp = ""
    with open(aim_label_new_path, 'r', encoding='utf-8') as old_version_label:
        src = old_version_label.readline()
        temp = "1" + src[1:]
        print(temp)
        old_version_label.close()
    with open(aim_label_new_path, 'w', encoding='utf-8') as new_version_label:
        new_version_label.write(temp)
        new_version_label.close()
