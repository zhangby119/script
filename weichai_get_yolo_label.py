import os
import json
import cv2

json_dir = 'C:/Users/zhangBY/Desktop/新建文件夹'
json_files = os.listdir(json_dir)



for json_file in json_files:

    json_file_path = json_dir + '/' + json_file
    img_file_name = json_file[:-4]+"jpg"
    img_file_path = json_dir + '/' + img_file_name

    label_file_name = json_file[:-4]+"txt"
    label_save_path = json_dir + '/' + label_file_name

    if json_file_path.endswith('json'):
    # 读单个json文件
        with open(json_file_path, 'r', encoding='utf-8') as jf:

            data = json.load(jf)
            # img = cv2.imread(img_file_path, cv2.IMREAD_COLOR)
            res_str = ""

            for shape in data['shapes']:
                points = shape['points']

                x0 = points[0][0]
                y0 = points[0][1]
                x1 = points[1][0]
                y1 = points[1][1]

                x_center = int((x0 + x1) / 2)
                y_center = int((y0 + y1) / 2)
                width = int(x1 - x0)
                height = int(y1 - y0)

                str = "%s %s %s %s\n" % (x_center, y_center, width, height)

                res_str += str



            with open(label_save_path,"w") as l:
                l.write(res_str)
