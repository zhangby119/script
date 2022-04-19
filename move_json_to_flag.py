import os
import json
import random

import cv2

json_dir = './2/'
json_files = os.listdir(json_dir)
new_json_dir = './new/'



for json_file in json_files:

    json_file_path = json_dir + '/' + json_file
    new_json_file_path = new_json_dir + '/' + json_file

    if json_file_path.endswith('json'):
    # 读单个json文件
        with open(json_file_path, 'r', encoding='utf-8') as jf:

            data = json.load(jf)
            # # 找到位置进行修改
            x_min = float("inf")
            y_min = float("inf")

            flag_x = 0
            flag_y = 0

            for i, points in enumerate(data['shapes']):

                if data['shapes'][i]['label'] == 'flag':
                    # print(data['shapes'][i]['points'][0])
                    flag_x = data['shapes'][i]['points'][0][0]
                    flag_y = data['shapes'][i]['points'][0][1]
            print(flag_x)
            print(flag_y)

            for shape in data['shapes']:
                # shape_type = shape['shape_type']  # 类型，如polygon或者linestrip
                # label_name = shape['label']  # 标签名，如heng,zong等等
                points = shape['points']
                print(points)
                for point in points:
                    if y_min > point[1]:
                        x_min = point[0]
                        y_min = point[1]

            x_dis = x_min - flag_x
            y_dis = y_min - flag_y
            print(x_dis)
            print(y_dis)



            for i, points in enumerate(data['shapes']):
                for j in range(len(data['shapes'][i]['points'])):
                    data['shapes'][i]['points'][j][0] = data['shapes'][i]['points'][j][0] - x_dis
                    data['shapes'][i]['points'][j][1] = data['shapes'][i]['points'][j][1] - y_dis
            json_dict = data

        with open(new_json_file_path, "w") as new_js:
            json.dump(json_dict, new_js)
