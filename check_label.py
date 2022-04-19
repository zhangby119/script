import os
import json

json_dir = './data/'
json_files = os.listdir(json_dir)
flag = True
for json_file in json_files:

    json_file_path = json_dir + '/' + json_file
    if json_file_path.endswith('json'):
    # 读单个json文件
        with open(json_file_path, 'r', encoding='utf-8') as jf:

            data = json.load(jf)
            # print(type(info))
            # 找到位置进行修改
            for shape in data['shapes']:
                shape_type = shape['shape_type']  # 类型，如polygon或者linestrip
                label_name = shape['label']  # 标签名，如heng,zong等等
                # points = shape['points']
                if shape_type == 'polygon':
                    if label_name == 'ce' or label_name == 'ping':
                        continue
                    else:
                        flag = False
                        print(json_file_path + "wrong polygon")
                elif shape_type == 'linestrip':
                    if label_name != 'edge':
                        flag = False
                        print(json_file_path + "wrong edge")
if flag:
    print("未找到违法标记")
