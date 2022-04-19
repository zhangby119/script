import os
import re
import shutil
import cv2

root_dir = 'C:/Users/zhangBY/Desktop/test'
img_list = os.listdir(root_dir)

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

models_split_raw_list = os.listdir(root_dir)

for model in models_split_raw_list:
    img_dir = os.path.join(root_dir, model)
    img_list = os.listdir(img_dir)
    for img_name in img_list:
        img_path = os.path.join(img_dir, img_name)
        img = cv2.imread(img_path)
        # print('img_path:%s' % img_path)
        dim = (1225, 1024)
        output_resize = cv2.resize(img, dim, cv2.INTER_NEAREST)
        cv2.imshow(model, output_resize)
        # cv2.imshow('img', img)
        key = str(cv2.waitKey())
        # print(key)
        model_num = int(key) - ord('0')
        if 10 > model_num > -1:
            model_secondary_num = model + '_' + str(model_num)
            # print(model_num)
            # print(model)
            print(model_secondary_num)

            new_img_dir = os.path.join(img_dir, model_secondary_num)
            if not os.path.exists(new_img_dir):
                os.mkdir(new_img_dir)

            new_img_path = os.path.join(new_img_dir, img_name)
            shutil.move(img_path, new_img_path)
        else:
            continue
    cv2.destroyAllWindows()
