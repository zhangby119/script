import os

name_prefix = '0915_second_factory_'
this_dir_path = './'
i = 0
for file in os.listdir(this_dir_path):
    if file.endswith("jpg"):
        file_path = os.path.join(this_dir_path, file)
        file_name = os.path.splitext(file_path.split('/')[-1])[0]
        new_file_name = name_prefix + "%s" % i + ".jpg"
        new_file_path = this_dir_path + new_file_name
        print(file_path+'---->'+new_file_path)
        os.rename(file_path, new_file_path)
        i = i + 1
