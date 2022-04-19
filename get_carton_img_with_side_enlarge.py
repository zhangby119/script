import os
import json
import random

import cv2

json_dir = './data/'
json_files = os.listdir(json_dir)
img_save_dir = './segment_img/'

json_dict = {}
json_save_dir_path = './new_label/'

enlarge_side_pro = 0.15
enlarge_side_min = 0.2
enlarge_side_max = 0.3


is_dir_exist = os.path.exists(img_save_dir)
if not is_dir_exist:
    os.mkdir(img_save_dir)
is_dir_exist = os.path.exists(json_save_dir_path)
if not is_dir_exist:
    os.mkdir(json_save_dir_path)

for json_file_name in json_files:
    file_name = json_file_name[:-5]
    json_file_path = json_dir + '/' + json_file_name

    img_file_name = file_name + ".jpg"
    img_save_file_name = file_name + "_enlarge_side.jpg"
    json_save_file_name = file_name + "_enlarge_side.json"
    img_file_path = json_dir + '/' + img_file_name
    img_save_path = img_save_dir + '/' + img_save_file_name

    json_save_path = json_save_dir_path + '/' + json_save_file_name

    if json_file_path.endswith('json'):
    # 读单个json文件
        temp_pro = random.random()
        if temp_pro < enlarge_side_pro:
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
                    # shape_type = shape['shape_type']  # 类型，如polygon或者linestrip
                    # label_name = shape['label']  # 标签名，如heng,zong等等
                    points = shape['points']
                    for point in points:
                        x_temp = point[0]
                        y_temp = point[1]
                        x1 = min(x1, x_temp)
                        x2 = max(x2, x_temp)
                        y1 = min(y1, y_temp)
                        y2 = max(y2, y_temp)

                enlarge_seed = random.uniform(enlarge_side_min, enlarge_side_max)
                box_width = (x2 - x1)
                box_height = (y2 - y1)
                edge = min(box_width, box_height) * enlarge_seed

                #进行上下左右的扩大
                if_enlarge_left = random.randint(0, 1)
                if_enlarge_right = random.randint(0, 1)
                if_enlarge_top = random.randint(0, 1)
                if_enlarge_bottom = random.randint(0, 1)
                x1_res = x1
                x2_res = x2
                y1_res = y1
                y2_res = y2
                if if_enlarge_left:
                    x1_res = max(x1 - edge, 0)
                if if_enlarge_right:
                    x2_res = min(x2 + edge, img_width)
                if if_enlarge_top:
                    y1_res = max(y1 - edge, 0)
                if if_enlarge_bottom:
                    y2_res = min(y2 + edge, img_height)



                for i, points in enumerate(data['shapes']):
                    for j in range(len(data['shapes'][i]['points'])):
                        data['shapes'][i]['points'][j][0] = data['shapes'][i]['points'][j][0] - x1_res
                        data['shapes'][i]['points'][j][1] = data['shapes'][i]['points'][j][1] - y1_res
                json_dict = data


                print("文件%s：左上角：(%f,%f)   右下角：(%f,%f)" %(json_file_path, x1, y1, x2, y2))
                res_img = img[int(y1_res):int(y2_res), int(x1_res):int(x2_res)]
                cv2.imwrite(img_save_path, res_img)
            with open(json_save_path, "w") as new_js:
                json.dump(json_dict, new_js)
