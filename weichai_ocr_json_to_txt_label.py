import os
import json
import cv2
import glob
import shutil
import random

root_dir = 'C:/Users/zhangBY/Desktop/20211219'
aim_dir = 'C:/Users/zhangBY/Desktop/20211219_augmented'
produce_num_per_img = 10
seed_ratio = 0.5

json_path_list = glob.glob(os.path.join(root_dir, '*.json'))

aim_label_path = os.path.join(aim_dir, 'labels.txt')

if os.path.exists(aim_label_path):
    shutil.remove(aim_label_path)
for json_path in json_path_list:
    img_path = json_path[:-4]+'png'
    img_name = img_path.split('\\')[-1]
    print(img_name)
    img = cv2.imread(img_path)
    img_height, img_width, _img_channel = img.shape
    # 读单个json文件
    with open(json_path, 'r', encoding='utf-8') as jf:
        data = json.load(jf)
        i = 0
        for shape in data['shapes']:
            points = shape['points']
            x0 = int(min(points[0][0], points[1][0]))
            y0 = int(min(points[0][1], points[1][1]))
            x1 = int(max(points[0][0], points[1][0]))
            y1 = int(max(points[0][1], points[1][1]))

            characters_width = x1 - x0
            characters_height = y1 - y0
            enlarge_range = seed_ratio * min(characters_width, characters_height)
            characters_letter = shape['label']

            for index in range(produce_num_per_img):
                new_x0 = None
                new_y0 = None
                new_x1 = None
                new_y1 = None
                if index == 0:
                    new_x0 = x0
                    new_y0 = y0
                    new_x1 = x1
                    new_y1 = y1
                elif index == 1:
                    new_x0 = 0 if (x0 - enlarge_range) < 0 else int(x0 - enlarge_range)
                    new_y0 = 0 if (y0 - enlarge_range) < 0 else int(y0 - enlarge_range)
                    new_x1 = img_width if (x1 + enlarge_range) >= img_width else int(x1 + enlarge_range)
                    new_y1 = img_height if (y1 + enlarge_range) >= img_height else int(y1 + enlarge_range)
                else:
                    while True:
                        up_lengthen = int(random.random() * enlarge_range)
                        bottom_lengthen = int(random.random() * enlarge_range)
                        left_lengthen = int(random.random() * enlarge_range)
                        right_lengthen = int(random.random() * enlarge_range)
                        new_x0 = x0 if x0 == 0 else x0 - left_lengthen
                        new_y0 = y0 if y0 == 0 else y0 - up_lengthen
                        new_x1 = x1 if x1 == img_width else x1 + right_lengthen
                        new_y1 = y1 if y1 == img_height else y1 + bottom_lengthen
                        if new_x0 >= 0 and new_y0 >= 0 or new_x1 <= img_width or new_y1 <= img_height:
                            break
                print("%s,%s,%s,%s" % (new_x0, new_y0 ,new_x1, new_y1))
                characters_img = img[new_y0:new_y1, new_x0:new_x1]
                characters_img_name = "%s_%s_%s.png" % (img_name[:-4], i, index)
                characters_img_path = os.path.join(aim_dir, characters_img_name)

                print(characters_img_path)
                str = "%s %s\n" % (characters_img_name, characters_letter)
                print(str)
                cv2.imwrite(characters_img_path, characters_img)
                with open(aim_label_path, "a", encoding='utf-8') as l:
                    l.write(str)
                    l.flush()
                    l.close()

            i = i + 1


