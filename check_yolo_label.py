import os
import cv2
import glob

root_dir = './yolo_check/'
paths = glob.glob(os.path.join(root_dir, '*.txt'))
for txt_path in paths:
    img_path = txt_path[:-3]+"jpg"
    img = cv2.imread(img_path)
    size = img.shape
    img_width = size[1]
    img_height = size[0]
    with open(txt_path, "r", encoding='utf-8') as t:
        str = t.readline()
        values = str.split()
        x_center = float(values[1])
        y_center = float(values[2])
        width = float(values[3])
        height = float(values[4])

        x_real_center = x_center * img_width
        y_real_center = y_center * img_height
        real_width = width * img_width
        real_height = height * img_height

        x1 = x_real_center - real_width/2.0
        x2 = x_real_center + real_width/2.0
        y1 = y_real_center - real_height/2.0
        y2 = y_real_center + real_height/2.0

        c1 = (int(x1), int(y1))
        c2 = (int(x2), int(y2))
        cv2.circle(img, (int(x_real_center), int(y_real_center)), 1, (255,0,0))
        cv2.rectangle(img, c1, c2, (0, 255, 0), 2)

        # cv2.rectangle(img, c1, c2)
        cv2.imshow("picture", img)
        cv2.waitKey(0)