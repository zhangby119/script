import os
import glob

import cv2

pre_root_dir = "D:/huifu/11.01-11.07_train_data/left"
enlarge_ratio = 4

root_dir = os.path.join(pre_root_dir, 'labeled_images')
save_dir = os.path.join(pre_root_dir, 'defect_images')
if not os.path.exists(save_dir):
    os.mkdir(save_dir)
model_list = os.listdir(root_dir)
for model in model_list:
    model_dir = os.path.join(root_dir, model)
    sub_model_list = os.listdir(model_dir)
    for sub_model in sub_model_list:
        sub_model_dir = os.path.join(model_dir, sub_model)
        txt_path_list = glob.glob(os.path.join(sub_model_dir, '*.txt'))
        # img_path_list = glob.glob(os.path.join(sub_model_dir, '*.png'))
        # print(txt_path_list)
        # print(img_path_list)
        for txt_path in txt_path_list:
            img_path = txt_path[:-3]+'png'
            # if not os.path.exists(img_path):
            #     print(img_path)
            img_name = img_path.split('\\')[-1][:-4]
            # print(img_name)
            img = cv2.imread(img_path)
            img_height, img_width, channel = img.shape
            label_list = []
            with open(txt_path, 'r', encoding='utf-8') as f:
                label_list = f.readlines()
                f.flush()
                f.close()
            # print(labels)
            new_label_str = ""
            index = 0
            for label in label_list:
                # if label.endswith("\n"):
                #     label = label[:-2]
                points = label.split(" ")
                # print(label.split(" "))

                x_center = int(points[0])
                y_center = int(points[1])
                width = int(points[2])
                if width<0:
                    print(img_path)
                    print(points)
                    width = abs(width)
                height = int(points[3])
                if height<0:
                    print(img_path)
                    print(points)
                    height = abs(height) * enlarge_ratio
                width = width * enlarge_ratio
                height = height * enlarge_ratio

                x1 = int(x_center - (width / 2))
                x2 = int(x_center + (width / 2))
                y1 = int(y_center - (height / 2))
                y2 = int(y_center + (height / 2))
                x1 = max(0, x1)
                y1 = max(0, y1)
                x2 = min(img_width, x2)
                y2 = min(img_height, y2)
                c1 = (x1, y1)
                c2 = (x2, y2)

                defect_img = img[y1:y2, x1:x2]

                defect_name = "%s_%s.png" % (img_name, index)
                defect_path = os.path.join(save_dir, defect_name)
                cv2.imwrite(defect_path, defect_img)
                index = index + 1

