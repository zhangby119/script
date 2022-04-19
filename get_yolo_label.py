import os
import json
import cv2

json_dir = './data/'
json_files = os.listdir(json_dir)
label_save_dir = './yolo_label/'

# 创立文件夹
is_dir_exist = os.path.exists(label_save_dir)
if not is_dir_exist:
    os.mkdir(label_save_dir)


for json_file in json_files:

    json_file_path = json_dir + '/' + json_file
    img_file_name = json_file[:-4]+"jpg"
    img_file_path = json_dir + '/' + img_file_name

    label_file_name = json_file[:-4]+"txt"
    label_save_path = label_save_dir + '/' + label_file_name

    if json_file_path.endswith('json'):
    # 读单个json文件
        with open(json_file_path, 'r', encoding='utf-8') as jf:

            data = json.load(jf)
            img = cv2.imread(img_file_path, cv2.IMREAD_COLOR)
            # print(type(info))
            # 找到位置进行修改
            x1 = float("inf")
            y1 = float("inf")
            x2 = 0
            y2 = 0
            size = img.shape
            img_width = size[1]
            img_height = size[0]

            for shape in data['shapes']:
                points = shape['points']
                for point in points:
                    x_temp = point[0]
                    y_temp = point[1]
                    x1 = min(x1, x_temp)
                    x2 = max(x2, x_temp)
                    y1 = min(y1, y_temp)
                    y2 = max(y2, y_temp)



            x_center = (x1+x2)/2.0
            y_center = (y1+y2)/2.0
            width = x2-x1
            height = y2-y1



            x_normalize = x_center / img_width
            y_normalize = y_center / img_height


            width_normalize = width / img_width
            height_normalize = height / img_height

            # # test
            # x_test = x_normalize * img_width
            # y_test = y_normalize * img_height
            # width_test = width_normalize * img_width
            # height_test = height_normalize * img_height
            # cv2.circle(img, (int(x_test), int(y_test)), 2, (0, 255, 255))
            # c1 = (int(x_test-(width_test/2)), int(y_test-(height_test/2)))
            # c2 = (int(x_test+(width_test/2)), int(y_test+(height_test/2)))
            # cv2.rectangle(img, c1, c2, (0, 255, 233), 2)
            # cv2.imshow("test", img)
            # cv2.waitKey(0)



            res_str = "0 %f %f %f %f"%(x_normalize, y_normalize, width_normalize, height_normalize)
            with open(label_save_path,"w") as l:
                l.write(res_str)
