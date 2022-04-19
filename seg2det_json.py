import os
import json
import random
import shutil

import cv2

json_dir = './src/'
new_json_dir = './dst/'
x_dis = 521
y_dis = 0
#左负右正 x
#上负下正 y

file_name = '0723_300_5_left_18'

json_file_path = json_dir + file_name + '.json'
new_json_file_path = new_json_dir + file_name + '.json'

if json_file_path.endswith('json'):
# 读单个json文件
    with open(json_file_path, 'r', encoding='utf-8') as jf:

        data = json.load(jf)
        x_min = float("inf")
        y_min = float("inf")
        x_max = 0
        y_max = 0

        for shape in data['shapes']:
            points = shape['points']
            for point in points:
                x_temp = point[0]
                y_temp = point[1]
                x_min = min(x_min, x_temp)
                x_max = max(x_max, x_temp)
                y_min = min(y_min, y_temp)
                y_max = max(y_max, y_temp)

        data['shapes'] = [{'label': 'carton', 'points': [[x_min, y_min],
                                                        [x_min, y_max],
                                                        [x_max, y_max],
                                                        [x_max, y_min]
                                                        ],
                          "shape_type": "polygon",
                          "flags": {}
                          }]


        # for i, points in enumerate(data['shapes']):
        #     for j in range(len(data['shapes'][i]['points'])):
        #         data['shapes'][i]['points'][j][0] = data['shapes'][i]['points'][j][0] + x_dis
        #         data['shapes'][i]['points'][j][1] = data['shapes'][i]['points'][j][1] + y_dis
        json_dict = data

    with open(new_json_file_path, "w") as new_js:
        json.dump(json_dict, new_js)

    # shutil.copy('./new/'+file_name+'.jpg','./new_2/'+file_name+'.jpg' )
