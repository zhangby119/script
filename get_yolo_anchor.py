import os
import json
import random
import glob
import cv2

label_dir = './raw_labels/'
aim_path = './w_h.txt'
img_width = 1280
img_height = 960
label_list = glob.glob(os.path.join(label_dir, '*.txt'))

for label_path in label_list:
    print("======================================================")
    with open(label_path, "r", encoding='utf-8') as t:
        str = t.readline()
        print(str)
        res_str = ""
        while str != "":
            values = str.split()
            print(values)
            width_norm = int(values[2])
            height_norm = int(values[3])
            width = width_norm * img_width
            height = height_norm * img_height
            res_str += "%s %s\n" % (width, height)
            str = t.readline()
        with open(aim_path, "a+") as l:
            l.write(str)
            l.flush()
            l.close()
    print("======================================================")

