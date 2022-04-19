import os
import cv2


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
    cv2.imwrite("temp_sobel_thre.png", temp_sobel_thre)
    vertical_search_size = 15
    vertical_step = 1
    horizon_search_size = 5
    horizon_step = 1
    min_unlikely_val = float(255.0)
    chosen_targ_region = [0,0,temp_region[2],temp_region[3]]
    for i in range(-vertical_search_size, (vertical_search_size + 1), vertical_step):
        for j in range(-horizon_search_size, (horizon_search_size + 1), horizon_step):
            # print(temp_region)
            x0 = temp_region[0] + j
            y0 = temp_region[1] + i
            x1 = x0 + temp_region[2]
            y1 = y0 + temp_region[3]
            targ_sobel = targ_sobel_whole_size[y0:y1, x0:x1]

            step_1 = abs(temp_sobel_thre - targ_sobel)
            step_2 = sum(map(sum,step_1))
            step_3 = float(temp_region[2]*temp_region[3])
            step_4 = float(step_2/step_3)
            print(step_4)
            # unlikely_val = float(cv2.sum(abs(temp_sobel_thre - targ_sobel))[0] / float(temp_region.area()))
            unlikely_val = step_4

            if min_unlikely_val > unlikely_val:
                min_unlikely_val = unlikely_val
                chosen_targ_region[0] = x0
                chosen_targ_region[1] = y0
    print("chosen_targ_region:%s" % chosen_targ_region)
    return chosen_targ_region


if __name__ == '__main__':
    error_file_name = 'E:/weichai/alignment_test/2021.09.01-13.43.10_40_down.png'
    template_file_name = 'E:/weichai/alignment_test/temp_40_down_21.png'
    error_raw_img = cv2.imread(error_file_name, 0)
    template_image = cv2.imread(template_file_name, 0)
    detect_region = [585,200,1231,1178]
    #442,200,1334,1076
    #585 200 1231 1178
    error_detect_region = alignment(error_raw_img, template_image, detect_region)
    print(error_detect_region)
    error_src_img = error_raw_img[error_detect_region[1]:error_detect_region[1]+error_detect_region[3],error_detect_region[0]:error_detect_region[0]+error_detect_region[2]]
    cv2.imshow("111", error_src_img)
    cv2.waitKey()
    cv2.imwrite("res.png", error_src_img)