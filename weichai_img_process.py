import os


import cv2

raw_img_dir = './raw_data/'
img_list = os.listdir(raw_img_dir)

res_img_dir = './res_img/'
res_label_dir = './labels/'

is_res_img_dir_exist = os.path.exists(res_img_dir)
if not is_res_img_dir_exist:
    os.mkdir(res_img_dir)
is_res_label_dir_exist = os.path.exists(res_label_dir)
if not is_res_label_dir_exist:
    os.mkdir(res_label_dir)

for img_file in img_list:
    label_name = img_file[:-3]+'txt'
    img_file_path = os.path.join(raw_img_dir, img_file)
    res_img_path = os.path.join(res_img_dir, img_file)
    res_label_path = os.path.join(res_img_dir, label_name)

    img = cv2.imread(img_file_path)

    cv2.imshow("111", img)
    cv2.waitKey(0)

    print(img[0][0])


