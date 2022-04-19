import os
import numpy as np
import re
import cv2
import glob
import random
import threading
import time
from threading import RLock

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

def mergeStone2Img(stone_img, stone_mask, tar_img, tar_cor):
    tar_img = cv2.cvtColor(tar_img, cv2.COLOR_GRAY2BGR)

    # cv2.imshow('stone_img',stone_img)
    # cv2.waitKey()
    # cv2.imshow('stone_mask',stone_mask)
    # cv2.waitKey()

    rows, cols, channels = stone_img.shape
    roi = tar_img[tar_cor[0]:tar_cor[0]+rows, tar_cor[1]:tar_cor[1]+cols]
    # cv2.imshow('roi',roi)
    # cv2.waitKey()

    mask_inv = cv2.bitwise_not(stone_mask)
    # cv2.imshow('mask_inv',mask_inv)
    # cv2.waitKey()
    img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)  # 将石块区域和mask取与使值为0
    # cv2.imshow('img1_bg',img1_bg)
    # cv2.waitKey()
    # 取 roi 中与 mask_inv 中不为零的值对应的像素的值，其他值为 0 。
    # 把logo放到图片当中
    img2_fg = cv2.bitwise_and(stone_img, stone_img, mask=stone_mask)  # 获取石块的像素信息

    # cv2.imshow('img2_fg',img2_fg)
    # cv2.waitKey()
    dst = cv2.add(img1_bg, img2_fg)  # 相加即可
    # cv2.imshow('dst',dst)
    # cv2.waitKey()
    tar_img[tar_cor[0]:tar_cor[0]+rows, tar_cor[1]:tar_cor[1]+cols] = dst
    # cv2.imshow('tar_img',tar_img)
    # cv2.waitKey()

    tar_img = cv2.cvtColor(tar_img, cv2.COLOR_BGR2GRAY)
    return tar_img

def produce_data(pre_root_dir, left_or_right, model_list, stone_img_dir):
    # print(stone_img_dir)
    stone_img_list = glob.glob(os.path.join(stone_img_dir, '*_mask.png'))

    print(len(stone_img_list))

    root_dir = os.path.join(pre_root_dir, left_or_right)
    side_type = left_or_right
    aim_negative_dir = os.path.join(root_dir, 'fake_stone_training_data')

    negative_label_dir = os.path.join(aim_negative_dir, 'labels')
    # if not os.path.exists(positive_label_dir):
    #     os.mkdir(positive_label_dir)
    # if not os.path.exists(negative_label_dir):
    #     os.mkdir(negative_label_dir)
    correct_dir = os.path.join(root_dir, 'model_source_images')
    model_dir = os.path.join(root_dir, 'model_images')
    model_list = os.listdir(model_dir)
    # print(model_list)
    for aim_model in model_list:
        print('开始处理模板%s...' % aim_model)
        sub_models_list = os.listdir(os.path.join(model_dir, aim_model))
        negative_label_txt = os.path.join(negative_label_dir, '%s_negative_label.txt' % aim_model)
        # print(positive_label_txt)
        # print(negative_label_txt)
        # print(sub_models_list)
        #
        # print(sub_models_list)
        for sub_model in sub_models_list:
            print('开始处理模板%s--子型板%s...' % (aim_model, sub_model))
            correct_img_dir = os.path.join(os.path.join(correct_dir, aim_model), sub_model)
            model_img_dir = os.path.join(os.path.join(model_dir, aim_model), sub_model)

            correct_img_path_list = glob.glob(os.path.join(correct_img_dir, '*.png'))
            model_img_path_list = glob.glob(os.path.join(model_img_dir, '*.png'))
            model_region_path_list = glob.glob(os.path.join(model_img_dir, '*.txt'))

            correct_img_num = len(correct_img_path_list)
            model_img_num = len(model_img_path_list)
            stone_img_num = len(stone_img_list)

            for error_index in range(10):
                stone_img_index = random.randint(1, stone_img_num) - 1
                stone_mask_path = stone_img_list[stone_img_index]
                stone_img_path = stone_mask_path[:-9] + '.png'
                print('fake stone file:%s' % stone_img_path)
                # print(stone_mask_path)
                lock.acquire()
                stone_img = cv2.imread(stone_img_path)
                stone_mask = cv2.imread(stone_mask_path, 0)
                lock.release()

                stone_height, stone_width, _ = stone_img.shape
                # print(stone_width)
                # print(stone_height)


                correct_img_index = random.randint(1, correct_img_num) - 1
                # print(correct_img_path_list[correct_img_index])
                src_img_path = correct_img_path_list[correct_img_index]
                correct_img_path_list.remove(src_img_path)
                correct_img_num = correct_img_num -1

                img_name = 'fake_stone_' + src_img_path.split('\\')[-1][:-4]
                print(img_name)

                model_img_index = random.randint(1, model_img_num) - 1
                model_img_path = model_img_path_list[model_img_index]

                model_region_path = model_img_path[:-3] + 'txt'
                with open(model_region_path, "r", encoding='utf-8') as model_label:
                    model_region_str = model_label.readline()[:-1]
                    model_label.close()
                model_region_temp = model_region_str.split(' ')
                model_region = list(map(int, model_region_temp))
                print('模板范围：%s' % model_region)
                correct_img = cv2.imread(src_img_path, 0)
                model_img = cv2.imread(model_img_path, 0)

                # print('对齐正确图像中')
                correct_img_region = alignment(correct_img, model_img, model_region)
                # print('正确图像对齐后区域：%s' % correct_img_region)

                # 测试跳过对齐
                # correct_img_region = model_region


                correct_img_after_alig = correct_img[correct_img_region[1]:correct_img_region[1] + correct_img_region[3],
                                       correct_img_region[0]:correct_img_region[0] + correct_img_region[2]]
                correct_height, correct_width = correct_img_after_alig.shape
                model_height, model_width = model_img.shape
                min_width = min(correct_width, model_width)
                min_height = min(correct_height, model_height)

                stone_x = random.randint(151, min_width-stone_width-150) - 1
                stone_y = random.randint(101, min_height-stone_height - 100) - 1
                stone_tar_cor = [int(stone_y), int(stone_x)]

                # cv2.imshow('123', stone_img)
                # cv2.waitKey()

                error_img_with_stone = mergeStone2Img(stone_img, stone_mask, correct_img_after_alig, stone_tar_cor)

                # dim = (1000, 800)
                # temp_resize = cv2.resize(error_img_with_stone, dim, cv2.INTER_NEAREST)
                # cv2.imshow("temp_img", temp_resize)
                # cv2.waitKey()

                stone_x_center = stone_width/2 + stone_x
                stone_y_center = stone_height / 2 + stone_y

                stone_width = 40 if stone_width < 40 else stone_width
                stone_height = 40 if stone_height < 40 else stone_height
                stone_rect = [int(stone_x_center), int(stone_y_center), stone_width, stone_height]
                print(stone_rect)


                print('开始生成数据...')
                x_center = stone_rect[0]
                y_center = stone_rect[1]
                width = stone_rect[2]
                height = stone_rect[3]
                if width < 40 or height < 40:
                    continue

                side_indicator = 0 if side_type == 'left' else 1

                for sample_index in range(11):
                    sample_x0 = 0
                    sample_y0 = 0
                    sample_x1 = 0
                    sample_y1 = 0
                    if sample_index==0:
                        sample_x0 = int(x_center - width/2)
                        sample_y0 = int(y_center - height/2)
                        sample_x1 = int(x_center + width/2)
                        sample_y1 = int(y_center + height/2)
                    else:
                        while True:
                            height_up = random.randint(0, height)
                            height_below = random.randint(0, height)
                            width_left = random.randint(0, width)
                            width_right = random.randint(0, width)
                            sample_x0 = x_center - width_left
                            sample_y0 = y_center - height_up
                            sample_x1 = x_center + width_right
                            sample_y1 = y_center + height_below
                            if height_below + height_up >= 40 and width_left + width_right >= 40 and sample_x0 >= 0 and sample_y0 >= 0 and sample_x1 <= min_width and sample_y1 <= min_height:
                                break


                    error_sample_img = error_img_with_stone[sample_y0:sample_y1, sample_x0:sample_x1]
                    model_sample_img = model_img[sample_y0:sample_y1, sample_x0:sample_x1]

                    negative_sample_error_name = '%s_%s_0_0_%s_0.png' % (img_name, side_indicator, sample_index)
                    negative_sample_model_name = '%s_%s_0_0_%s_1.png' % (img_name, side_indicator, sample_index)

                    negative_label = '%s,%s,2\n' % (negative_sample_error_name, negative_sample_model_name)
                    with open(negative_label_txt, "a", encoding='utf-8') as n_label_file:
                        n_label_file.write(negative_label)
                        n_label_file.close()

                    negative_sample_error_path = os.path.join(aim_negative_dir, negative_sample_error_name)
                    negative_sample_model_path = os.path.join(aim_negative_dir, negative_sample_model_name)

                    cv2.imwrite(negative_sample_error_path, error_sample_img)
                    cv2.imwrite(negative_sample_model_path, model_sample_img)

                print('------------------------------------------------------')
            print('\n')

class myThread (threading.Thread):
    def __init__(self, threadID, root_dir, side_type, model_list, stone_dir):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.root_dir = root_dir
        self.side_type = side_type
        self.model_list = model_list
        self.stone_dir = stone_dir
    def run(self):
        print ("开始线程：%s" % self.model_list)
        produce_data(self.root_dir, self.side_type, self.model_list, self.stone_dir)
        print ("退出线程：%s" % self.model_list)



if __name__ == '__main__':
    lock = RLock()
    # root_dir = 'D:/huifu/10.23-10.28'
    root_dir = '/home/research/Py_Project/weichai_dataset/WeiChaiDataset_arranged'
    stone_dir = '/home/research/Py_Project/weichai_dataset/stoneImg'
    left_model_list = os.listdir(os.path.join(os.path.join(root_dir, 'left'), 'labeled_images'))
    left_model_num_half = int(len(left_model_list)/2)
    # print(left_model_num_half)
    print(left_model_list)
    left_model_list_1 = left_model_list[0:left_model_num_half]
    left_model_list_2 = left_model_list[left_model_num_half:]

    print(left_model_list_1)
    print(left_model_list_2)

    right_model_list = os.listdir(os.path.join(os.path.join(root_dir, 'right'), 'labeled_images'))
    right_model_num_half = int(len(right_model_list) / 2)
    # print(right_model_num_half)
    print(right_model_list)
    right_model_list_1 = right_model_list[0:right_model_num_half]
    right_model_list_2 = right_model_list[right_model_num_half:]

    print(right_model_list_1)
    print(right_model_list_2)

    for side in ['left', 'right']:
        aim_negative_dir = os.path.join(os.path.join(root_dir, side), 'fake_stone_training_data')
        if not os.path.exists(aim_negative_dir):
            os.mkdir(aim_negative_dir)

        negative_label_dir = os.path.join(aim_negative_dir, 'labels')
        if not os.path.exists(negative_label_dir):
            os.mkdir(negative_label_dir)


    # 创建新线程
    thread1 = myThread(1, root_dir, 'left', left_model_list_1, stone_dir)
    thread2 = myThread(2, root_dir, 'left', left_model_list_2, stone_dir)
    thread3 = myThread(3, root_dir, 'right', right_model_list_1, stone_dir)
    thread4 = myThread(4, root_dir, 'right', right_model_list_2, stone_dir)

    # 开启新线程
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
    print("退出主线程")
    #
    time.sleep(10)

    for side in ['left', 'right']:
        negative_label_dir = os.path.join(os.path.join(os.path.join(root_dir, side), 'fake_stone_training_data'), 'labels')
        negative_label_list = os.listdir(negative_label_dir)

        final_negative_label_path = os.path.join(negative_label_dir, 'labels.txt')

        for negative_label_name in negative_label_list:
            negative_label_path = os.path.join(negative_label_dir, negative_label_name)
            print(negative_label_path)
            str_negative = ''
            with open(negative_label_path, "r", encoding='utf-8') as negative_label:
                str_negative_line = negative_label.readline()
                while str_negative_line != '':
                    str_negative += str_negative_line
                    str_negative_line = negative_label.readline()
                negative_label.close()
            with open(final_negative_label_path, "a", encoding='utf-8') as final_negative_label:
                final_negative_label.write(str_negative)
                final_negative_label.close()

