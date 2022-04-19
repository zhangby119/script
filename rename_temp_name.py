import os

name_prefix = '0925_second_factory_'
this_dir_path = './'
i = 0
for file in os.listdir(this_dir_path):
    if file.endswith("jpg"):
        img_path = os.path.join(this_dir_path, file)
        file_name = os.path.splitext(img_path.split('/')[-1])[0]

        json_name = file_name + ".json"
        json_path = os.path.join(this_dir_path, json_name)

        new_file_name = name_prefix + "%s" % i
        new_img_name = new_file_name + ".jpg"
        new_img_path = this_dir_path + new_img_name

        if os.path.exists(json_path):
            new_json_name = new_file_name + ".json"
            new_json_path = this_dir_path + new_json_name
            print(json_path + '---->' + new_json_path)
            os.rename(json_path, new_json_path)

        print(img_path+'---->'+new_img_path)
        os.rename(img_path, new_img_path)
        i = i + 1
