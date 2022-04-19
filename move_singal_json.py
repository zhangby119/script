import os
import json
import random
import shutil

import cv2

json_dir = './new/'
new_json_dir = './new_2/'
x_dis = 521
y_dis = 0
#左负右正 x
#上负下正 y

file_name = '20210603_xie51'

json_file_path = json_dir + file_name + '.json'
new_json_file_path = new_json_dir + file_name + '.json'

if json_file_path.endswith('json'):
# 读单个json文件
    with open(json_file_path, 'r', encoding='utf-8') as jf:

        data = json.load(jf)



        for i, points in enumerate(data['shapes']):
            for j in range(len(data['shapes'][i]['points'])):
                data['shapes'][i]['points'][j][0] = data['shapes'][i]['points'][j][0] + x_dis
                data['shapes'][i]['points'][j][1] = data['shapes'][i]['points'][j][1] + y_dis
        json_dict = data

    with open(new_json_file_path, "w") as new_js:
        json.dump(json_dict, new_js)

    shutil.copy('./new/'+file_name+'.jpg','./new_2/'+file_name+'.jpg' )
