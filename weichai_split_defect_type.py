import os
import cv2
import glob

import cv2

root_dir = "D:/huifu/WeiChaiDataset_arranged/right/labeled_images"
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
            print(img_name)
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
                print(label.split(" "))

                x_center = int(points[0])
                y_center = int(points[1])
                width = int(points[2])
                height = int(points[3])

                x1 = int(x_center - (width / 2))
                x2 = int(x_center + (width / 2))
                y1 = int(y_center - (height / 2))
                y2 = int(y_center + (height / 2))

                c1 = (x1, y1)
                c2 = (x2, y2)

                tmp = img.copy()
                defect_img = img[y1:y2, x1:x2]

                cv2.circle(tmp, (x_center, y_center), 1, (255, 0, 0))
                cv2.rectangle(tmp, c1, c2, (0, 255, 0), 2)

                dim = (int(img_width/2.5), int(img_height/2.5))
                temp_resize = cv2.resize(tmp, dim, cv2.INTER_NEAREST)

                defect_dim = (200, 150)
                defect_resize = cv2.resize(defect_img, defect_dim, cv2.INTER_NEAREST)
                cv2.imshow("defect image", defect_resize)
                cv2.imshow("src image", temp_resize)
                key = cv2.waitKey()
                type = chr(key)
                print(chr(key))

                new_label = "%s %s %s %s %s\n" % (x_center, y_center, width, height, type)
                new_label_str += new_label

                defect_dir = os.path.join(sub_model_dir, type)
                defect_name = "%s_%s.png" % (img_name, index)
                if not os.path.exists(defect_dir):
                    os.mkdir(defect_dir)
                defect_path = os.path.join(defect_dir, defect_name)
                cv2.imwrite(defect_path, defect_img)
                index = index + 1
            with open(txt_path, "w") as l:
                l.write(new_label_str)
                l.flush()
                l.close()

