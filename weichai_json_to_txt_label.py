import os
import json
import glob

def json_to_txt(super_root_dir):
    for side in ['left', 'right']:
        root_dir = os.path.join(os.path.join(super_root_dir, side), 'labeled_images')
        model_list = os.listdir(root_dir)
        for model in model_list:
            model_dir = os.path.join(root_dir, model)
            sub_model_list = os.listdir(model_dir)
            for sub_model in sub_model_list:
                sub_model_dir = os.path.join(model_dir, sub_model)
                json_path_list = glob.glob(os.path.join(sub_model_dir, '*.json'))
                # img_path_list = glob.glob(os.path.join(sub_model_dir, '*.png'))
                # print(txt_path_list)
                # print(img_path_list)
                for json_path in json_path_list:
                    aim_txt_path = json_path[:-4]+'txt'

                    with open(json_path, 'r', encoding='utf-8') as jf:

                        data = json.load(jf)
                        # img = cv2.imread(img_file_path, cv2.IMREAD_COLOR)
                        res_str = ""

                        for shape in data['shapes']:
                            points = shape['points']

                            x0 = points[0][0]
                            y0 = points[0][1]
                            x1 = points[1][0]
                            y1 = points[1][1]
                            label_str = shape['label']
                            label = label_str[-1]
                            if label not in ['0', '1']:
                                print(label)


                            x_center = int((x0 + x1) / 2)
                            y_center = int((y0 + y1) / 2)
                            width = abs(int(x1 - x0))
                            height = abs(int(y1 - y0))

                            str = "%s %s %s %s %s\n" % (x_center, y_center, width, height, label)

                            res_str += str

                        with open(aim_txt_path, "w") as l:
                            l.write(res_str)
                            l.flush()
                            l.close()

                        jf.flush()
                        jf.close()


if __name__ == '__main__':
    json_to_txt('C:/Users/zhangBY/Desktop/11.01-11.07_train_data')
