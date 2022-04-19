import os
import shutil

import cv2
import glob

import cv2


def generate_src_defect_img(sup_root_dir):
    for side in ['left', 'right']:
        root_dir = os.path.join(sup_root_dir, side)
        model_dir = os.path.join(root_dir, 'labeled_images')
        aim_negative_dir = os.path.join(root_dir, 'src_negative_data')


        if os.path.exists(aim_negative_dir):
            shutil.rmtree(aim_negative_dir)
        os.mkdir(aim_negative_dir)

        model_list = os.listdir(model_dir)

        for model in model_list:
            model_path = os.path.join(model_dir, model)
            sub_model_list = os.listdir(model_path)
            for sub_model in sub_model_list:
                sub_model_path = os.path.join(model_path, sub_model)
                txt_path_list = glob.glob(os.path.join(sub_model_path, '*.txt'))
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
                    img_height, img_width, _ = img.shape
                    error_rect_list = []
                    with open(txt_path, 'r', encoding='utf-8') as f:
                        print('读取标注数据……')
                        label_line_str = f.readline()
                        while label_line_str != '':
                            label_line_list = label_line_str.split()
                            print('标注文件中标注信息：%s' % label_line_list)
                            txt_x_center = int(label_line_list[0])
                            txt_y_center = int(label_line_list[1])
                            txt_width = int(label_line_list[2])
                            txt_height = int(label_line_list[3])
                            txt_label = int(label_line_list[4])

                            single_error_rect = [txt_x_center, txt_y_center, txt_width, txt_height, txt_label]
                            error_rect_list.append(single_error_rect)
                            label_line_str = f.readline()
                        f.close()
                    print('开始生成数据...')
                    rect_index = 0
                    for error_rect in error_rect_list:
                        x_center = error_rect[0]
                        y_center = error_rect[1]
                        width = error_rect[2]
                        height = error_rect[3]
                        label = error_rect[4]
                        if label == 'n':
                            continue
                        label = int(label)
                        if width < 40:
                            width = 40
                        if height < 40:
                            height = 40

                        width = width*2
                        height = height*2

                        sample_x0 = int(x_center - width / 2)
                        sample_x1 = int(x_center + width / 2)
                        sample_y0 = int(y_center - height / 2)
                        sample_y1 = int(y_center + height / 2)

                        sample_x0 = sample_x0 if sample_x0 >= 0 else 0
                        sample_y0 = sample_y0 if sample_y0 >= 0 else 0
                        sample_x1 = sample_x1 if sample_x1 < img_width else img_width-1
                        sample_y1 = sample_y1 if sample_y1 < img_height else img_height-1

                        error_sample_img = img[sample_y0:sample_y1, sample_x0:sample_x1]

                        negative_sample_error_name = '%s_%s_%s.png' % (img_name, rect_index, label)

                        negative_sample_error_path = os.path.join(aim_negative_dir, negative_sample_error_name)

                        cv2.imwrite(negative_sample_error_path, error_sample_img)

                        rect_index = rect_index + 1
if __name__ == '__main__':
    root_dir = "D:/huifu/11.01-11.07_train_data"
    generate_src_defect_img(root_dir)
# print(count_num)

