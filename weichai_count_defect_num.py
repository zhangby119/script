import os
import cv2
import glob

import cv2


def count_side_num(root_dir):
    count_num = 0
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
                # print(label_list)
                # print(len(label_list))
                count_num = count_num + len(label_list)
    return count_num
if __name__ == '__main__':
    left_root_dir = "D:/huifu/WeiChaiDataset_arranged_with_type/left/labeled_images"
    right_root_dir = "D:/huifu/WeiChaiDataset_arranged_with_type/right/labeled_images"
    left_num = count_side_num(left_root_dir)
    print(left_num)
    right_num = count_side_num(right_root_dir)
    print(right_num)
    res = left_num+ right_num
    print(res)
# print(count_num)

