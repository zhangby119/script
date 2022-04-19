import os
import numpy as np
import re
import cv2
import glob
import random

import cv2
'''
命名信息：   以'_'分割，
        0. 采集时间
        1. 型板号
        2. 上下型
        ======
        3. 左右相机 （0为左相机，1为右相机）
        4. 正样本是否是随机取样（0为对应，1为随机取样）
        5. 正负样本（0为负样本，1为正样本）
        6. 第几个标注区域
        7. 该标注区域生成出的第几个数据（共21个）
        8. 属于模板数据还是型板数据（0为从单图型板上取出的数据，1为从模板上取出的数据）
        
'''
def get_sobel(__img, kernel_size, direction):
    if __img is None:
        return __img
    img = __img.copy()

    scale = 1
    delta = 0
    ddepth = cv2.CV_16S
    img_guaussian = cv2.GaussianBlur(img, (kernel_size, kernel_size), 0, 0, cv2.BORDER_DEFAULT)
    # grad_x = cv2.Sobel(img_guaussian, ddepth, 1, 0, 3, scale, delta, cv2.BORDER_DEFAULT)
    grad_x = cv2.Sobel(img_guaussian, ddepth, 1, 0)
    abs_grad_x = cv2.convertScaleAbs(grad_x)
    grad_y = cv2.Sobel(img_guaussian, ddepth, 0, 1)
    abs_grad_y = cv2.convertScaleAbs(grad_y)
    if direction == "vertical":
        return abs_grad_x
    elif direction == "horizon":
        return abs_grad_y
    else:
        grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)

        return grad


def alignment(targ_img, temp_img, temp_region):
    # if targ_img is None or temp_img is None or temp_region.area() == 0 or temp_img.rows != temp_region.height or temp_img.cols != temp_region.width:
    #     return temp_region
    temp_sobel = get_sobel(temp_img, 9, "both")
    targ_sobel_whole_size = get_sobel(targ_img, 9, "both")

    temp_sobel_list = cv2.threshold(temp_sobel, 20, 255, cv2.THRESH_TOZERO)
    temp_sobel_thre = temp_sobel_list[1]
    targ_sobel_whole_size_list = cv2.threshold(targ_sobel_whole_size, 20, 255, cv2.THRESH_TOZERO)
    targ_sobel_whole_size = targ_sobel_whole_size_list[1]
    # cv2.imwrite("temp_sobel_thre.png", temp_sobel_thre)

    vertical_search_size = 15
    vertical_step = 1
    horizon_search_size = 10
    horizon_step = 1
    print('垂直范围：-+%s, 垂直步幅：%s, 水平范围：-+%s, 水平步幅：%s,' % (vertical_search_size, vertical_step, horizon_search_size, horizon_step))
    min_unlikely_val = float(255.0)
    chosen_targ_region = [0,0,temp_region[2],temp_region[3]]
    for i in range(-vertical_search_size, (vertical_search_size + 1), vertical_step):
        for j in range(-horizon_search_size, (horizon_search_size + 1), horizon_step):
            x0 = temp_region[0] + j
            y0 = temp_region[1] + i
            x1 = x0 + temp_region[2]
            y1 = y0 + temp_region[3]
            targ_sobel = targ_sobel_whole_size[y0:y1, x0:x1]

            step_1 = abs(temp_sobel_thre - targ_sobel)
            step_2 = sum(map(sum,step_1))
            step_3 = float(temp_region[2]*temp_region[3])
            step_4 = float(step_2/step_3)
            # unlikely_val = float(cv2.sum(abs(temp_sobel_thre - targ_sobel))[0] / float(temp_region.area()))
            unlikely_val = step_4

            if min_unlikely_val > unlikely_val:
                min_unlikely_val = unlikely_val
                chosen_targ_region[0] = x0
                chosen_targ_region[1] = y0
    # print("对齐后:%s" % chosen_targ_region)
    return chosen_targ_region

def produce_data(pre_root_dir, left_or_right):
    root_dir = os.path.join(pre_root_dir, left_or_right)
    side_type = left_or_right
    aim_negative_dir = os.path.join(root_dir, 'negative_training_data')
    negative_label_txt = os.path.join(aim_negative_dir, 'negative_label.txt')
    aim_positive_dir = os.path.join(root_dir, 'positive_training_data')
    positive_label_txt = os.path.join(aim_positive_dir, 'positive_label.txt')
    if not os.path.exists(aim_negative_dir):
        os.mkdir(aim_negative_dir)
    if not os.path.exists(aim_positive_dir):
        os.mkdir(aim_positive_dir)

    labeled_dir = os.path.join(root_dir, 'labeled_images')
    correct_dir = os.path.join(root_dir, 'model_source_images')
    model_dir = os.path.join(root_dir, 'model_images')
    model_list = os.listdir(labeled_dir)
    print(model_list)
    for aim_model in model_list:
        print('开始处理模板%s...' % aim_model)
        sub_models_list = os.listdir(os.path.join(labeled_dir, aim_model))
        # print(sub_models_list)
        for sub_model in sub_models_list:
            print('开始处理模板%s--子型板%s...' % (aim_model, sub_model))
            labeled_img_dir = os.path.join(os.path.join(labeled_dir, aim_model), sub_model)
            correct_img_dir = os.path.join(os.path.join(correct_dir, aim_model), sub_model)
            model_img_dir = os.path.join(os.path.join(model_dir, aim_model), sub_model)
            label_path_list = glob.glob(os.path.join(labeled_img_dir, '*.txt'))
            error_img_path_list = glob.glob(os.path.join(labeled_img_dir, '*.png'))
            correct_img_path_list = glob.glob(os.path.join(correct_img_dir, '*.png'))
            model_img_path_list = glob.glob(os.path.join(model_img_dir, '*.png'))
            model_region_path_list = glob.glob(os.path.join(model_img_dir, '*.txt'))

            correct_img_num = len(correct_img_path_list)
            model_img_num = len(model_img_path_list)

            for error_img_path in error_img_path_list:
                img_name = error_img_path.split('\\')[-1][:-4]
                print('处理缺陷记录%s...' % img_name)
                label_path = error_img_path[:-3] + 'txt'
                error_img = cv2.imread(error_img_path, 0)
                correct_img_index = random.randint(1, correct_img_num) - 1

                model_img_index = random.randint(1, model_img_num) - 1
                model_img_path = model_img_path_list[model_img_index]
                model_img = cv2.imread(model_img_path, 0)
                model_region_path = model_img_path[:-3] + 'txt'
                model_region_str = ''
                # if model_region_path not in model_region_path_list:
                #     cv2.imshow('%s not find model label' % model_img_path, model_img)
                #     cv2.waitKey()
                with open(model_region_path, "r", encoding='utf-8') as model_label:
                    model_region_str = model_label.readline()[:-1]
                    model_label.close()
                model_region_temp = model_region_str.split(' ')
                model_region = list(map(int, model_region_temp))
                print('模板范围：%s' % model_region)
                correct_img = cv2.imread(correct_img_path_list[correct_img_index], 0)

                # print('对齐错误图像中')
                # error_img_region = alignment(error_img, model_img, model_region)
                # print('错误图像对齐后区域：%s' % error_img_region)
                # print('对齐正确图像中')
                # correct_img_region = alignment(correct_img, model_img, model_region)
                # print('正确图像对齐后区域：%s' % correct_img_region)

                # 测试跳过对齐
                error_img_region = model_region
                correct_img_region = model_region

                error_img_after_alig = error_img[error_img_region[1]:error_img_region[1] + error_img_region[3],
                                       error_img_region[0]:error_img_region[0] + error_img_region[2]]
                correct_img_after_alig = correct_img[correct_img_region[1]:correct_img_region[1] + correct_img_region[3],
                                       correct_img_region[0]:correct_img_region[0] + correct_img_region[2]]

                error_shape = error_img_after_alig.shape
                correct_shape = correct_img_after_alig.shape
                model_shape = model_img.shape
                min_width = min(error_shape[1], correct_shape[1], model_shape[1])
                min_height = min(error_shape[0], correct_shape[0], model_shape[0])

                # if label_path not in label_path_list:
                #     cv2.imshow('not find error label', error_img)
                #     cv2.waitKey()

                error_rect_list = []
                with open(label_path, "r", encoding='utf-8') as label_file:
                    print('读取标注数据……')
                    label_line_str = label_file.readline()
                    while label_line_str != '':
                        label_line_list = label_line_str.split()
                        print('标注文件中标注信息：%s' % label_line_list)
                        txt_x_center = int(label_line_list[0]) - error_img_region[0]
                        txt_y_center = int(label_line_list[1]) - error_img_region[1]
                        txt_width = int(label_line_list[2])
                        txt_height = int(label_line_list[3])

                        single_error_rect = [txt_x_center, txt_y_center, txt_width, txt_height]
                        error_rect_list.append(single_error_rect)
                        label_line_str = label_file.readline()
                    label_file.close()
                print('标注数据根据对齐结果变化后：%s' % error_rect_list)

                print('开始生成数据...')
                rect_index = 0
                for error_rect in error_rect_list:
                    same_pos_positive_sample_posibility = random.random()
                    is_same_pos_positive_sample = True if same_pos_positive_sample_posibility < 0.6 else False
                    print(same_pos_positive_sample_posibility)
                    random_positive_sample_indicator = 0 if is_same_pos_positive_sample else 1
                    if is_same_pos_positive_sample:
                        print('正样本在负样本相同位置采样')
                    else:
                        print('正样本在全图随机采样')
                    x_center = error_rect[0]
                    y_center = error_rect[1]
                    width = error_rect[2]
                    height = error_rect[3]
                    if width < 40 or height < 40:
                        continue

                    x0 = int(x_center - width/2)
                    x1 = int(x_center + width/2)
                    y0 = int(y_center - height/2)
                    y1 = int(y_center + height/2)

                    side_indicator = 0 if side_type == 'left' else 1
                    # print(side_indicator)
                    src_negative_sample_error_name = '%s_%s_%s_0_%s_0_0.png' % (img_name, side_indicator, random_positive_sample_indicator, rect_index)
                    src_negative_sample_model_name = '%s_%s_%s_0_%s_0_1.png' % (img_name, side_indicator, random_positive_sample_indicator, rect_index)

                    src_positive_sample_correct_name = '%s_%s_%s_1_%s_0_0.png' % (img_name, side_indicator, random_positive_sample_indicator, rect_index)
                    src_positive_sample_model_name = '%s_%s_%s_1_%s_0_1.png' % (img_name, side_indicator, random_positive_sample_indicator, rect_index)

                    src_negative_sample_error = error_img_after_alig[y0: y1, x0: x1]
                    src_negative_sample_model = model_img[y0: y1, x0: x1]
                    src_positive_sample_correct = correct_img_after_alig[y0: y1, x0: x1]

                    negative_label = '%s,%s,0\n' % (src_negative_sample_error_name, src_negative_sample_model_name)
                    with open(negative_label_txt, "a", encoding='utf-8') as n_label_file:
                        n_label_file.write(negative_label)
                        n_label_file.close()
                    positive_label = '%s,%s,1\n' % (src_positive_sample_correct_name, src_positive_sample_model_name)
                    with open(positive_label_txt, "a", encoding='utf-8') as p_label_file:
                        p_label_file.write(positive_label)
                        p_label_file.close()

                    src_negative_sample_error_path = os.path.join(aim_negative_dir, src_negative_sample_error_name)
                    src_negative_sample_model_path = os.path.join(aim_negative_dir, src_negative_sample_model_name)
                    src_positive_sample_correct_path = os.path.join(aim_positive_dir, src_positive_sample_correct_name)
                    src_positive_sample_model_path = os.path.join(aim_positive_dir, src_positive_sample_model_name)

                    cv2.imwrite(src_negative_sample_error_path, src_negative_sample_error)
                    cv2.imwrite(src_negative_sample_model_path, src_negative_sample_model)
                    cv2.imwrite(src_positive_sample_correct_path, src_positive_sample_correct)
                    cv2.imwrite(src_positive_sample_model_path, src_negative_sample_model)

                    sample_index = 1
                    for sample_index in range(1, 21):
                        height_up = random.randint(0, height)
                        height_below = random.randint(0, height)
                        width_left = random.randint(0, width)
                        width_right = random.randint(0, width)
                        sample_x0 = x_center - width_left
                        sample_y0 = y_center - height_up
                        sample_x1 = x_center + width_right
                        sample_y1 = y_center + height_below
                        while height_below + height_up < 40 or width_left + width_right < 40 or sample_x0 < 0 or sample_y0 < 0 or sample_x1 > min_width or sample_y1 > min_height:
                            height_up = random.randint(0, height)
                            height_below = random.randint(0, height)
                            width_left = random.randint(0, width)
                            width_right = random.randint(0, width)
                            sample_x0 = x_center - width_left
                            sample_y0 = y_center - height_up
                            sample_x1 = x_center + width_right
                            sample_y1 = y_center + height_below

                        error_sample_img = error_img_after_alig[sample_y0:sample_y1, sample_x0:sample_x1]
                        model_sample_img = model_img[sample_y0:sample_y1, sample_x0:sample_x1]

                        negative_sample_error_name = '%s_%s_%s_0_%s_%s_0.png' % (img_name, side_indicator, random_positive_sample_indicator, rect_index, sample_index)
                        negative_sample_model_name = '%s_%s_%s_0_%s_%s_1.png' % (img_name, side_indicator, random_positive_sample_indicator, rect_index, sample_index)

                        negative_label = '%s,%s,0\n' % (negative_sample_error_name, negative_sample_model_name)
                        with open(negative_label_txt, "a", encoding='utf-8') as n_label_file:
                            n_label_file.write(negative_label)
                            n_label_file.close()

                        negative_sample_error_path = os.path.join(aim_negative_dir, negative_sample_error_name)
                        negative_sample_model_path = os.path.join(aim_negative_dir, negative_sample_model_name)

                        cv2.imwrite(negative_sample_error_path, error_sample_img)
                        cv2.imwrite(negative_sample_model_path, model_sample_img)

                        positive_sample_correct_name = ''
                        positive_sample_model_name = ''
                        if is_same_pos_positive_sample:
                            correct_sample_img = correct_img_after_alig[sample_y0:sample_y1, sample_x0:sample_x1]

                            positive_sample_correct_name = '%s_%s_0_1_%s_%s_0.png' % (img_name, side_indicator, rect_index, sample_index)
                            positive_sample_model_name = '%s_%s_0_1_%s_%s_1.png' % (img_name, side_indicator, rect_index, sample_index)

                        else:
                            positive_sample_width_range = min_width - sample_x1 + sample_x0
                            positive_sample_height_range = min_height - sample_y1 + sample_y0
                            new_x0 = random.randint(0, positive_sample_width_range)
                            new_y0 = random.randint(0, positive_sample_height_range)
                            new_x1 = new_x0 + sample_x1 - sample_x0
                            new_y1 = new_y0 + sample_y1 - sample_y0
                            correct_sample_img = correct_img_after_alig[new_y0:new_y1, new_x0:new_x1]
                            model_sample_img = model_img[new_y0:new_y1, new_x0:new_x1]

                            positive_sample_correct_name = '%s_%s_1_1_%s_%s_0.png' % (img_name, side_indicator, rect_index, sample_index)
                            positive_sample_model_name = '%s_%s_1_1_%s_%s_1.png' % (img_name, side_indicator, rect_index, sample_index)

                        positive_label = '%s,%s,1\n' % (positive_sample_correct_name, positive_sample_model_name)
                        with open(positive_label_txt, "a", encoding='utf-8') as p_label_file:
                            p_label_file.write(positive_label)
                            p_label_file.close()

                        positive_sample_correct_path = os.path.join(aim_positive_dir, positive_sample_correct_name)
                        positive_sample_model_path = os.path.join(aim_positive_dir, positive_sample_model_name)

                        cv2.imwrite(positive_sample_correct_path, correct_sample_img)
                        cv2.imwrite(positive_sample_model_path, model_sample_img)

                    rect_index = rect_index + 1
                print('------------------------------------------------------')
            print('\n')




if __name__ == '__main__':
    produce_data('D:/huifu/WeiChaiDataset_arranged', 'left')
    produce_data('D:/huifu/WeiChaiDataset_arranged', 'right')