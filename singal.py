import os

# this_file_path = __file__
# this_dir_path = os.path.dirname(this_file_path)
this_dir_path = './'
json_index = 1
png_index = 1
for file in os.listdir(this_dir_path):
    file_path = os.path.join(this_dir_path, file)
    if os.path.splitext(file_path)[-1] == '.jpg':
        new_file_path_1 = "../2021_5_28_sideCam%d.jpg" % png_index
        new_file_path = '.'+'/'.join((os.path.splitext(file_path)[0].split('\\'))[:-1]) + '/{:0>4}_Color.png'.format(png_index)
        print(new_file_path_1)
        print(new_file_path)
        png_index += 1
        print(file_path+'---->'+new_file_path)
        os.rename(file_path, new_file_path)