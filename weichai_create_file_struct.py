import os
import cv2
import glob

import cv2


def check_file_tree(sup_root_dir):
    for side in ['left', 'right']:
        root_dir = os.path.join(os.path.join(sup_root_dir, side), 'labeled_images')
        # for folder in ['labeled_images', 'model_source_images', 'model_images']:
        model_list = os.listdir(root_dir)
        for model in model_list:
            model_dir = os.path.join(root_dir, model)
            sub_model_list = os.listdir(model_dir)
            for sub_model in sub_model_list:
                sub_model_dir = os.path.join(model_dir, sub_model)
                for folder in ['model_source_images', 'model_images']:
                    path = sub_model_dir.replace('labeled_images', folder)
                    # print(path)
                    if not os.path.exists(path):
                        if folder == 'model_images':
                            os.makedirs(path)
                        else:
                            print(path)

    return
if __name__ == '__main__':
    # text = "C:/Users/zhangBY/Desktop/11.01-11.07_train_data/right/model_images/19_down"
    check_file_tree("C:/Users/zhangBY/Desktop/11.01-11.07_train_data")

# print(count_num)

