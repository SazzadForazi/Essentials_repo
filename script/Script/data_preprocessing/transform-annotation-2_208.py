# Image resizing and edit json script (208x208)
import os
import argparse
import cv2
import shutil
import json
import base64
from os.path import exists

def edit_json(new_height, new_width, ratio_x, ratio_y, name,imagedata,flag):
    if flag:
        shutil.copyfile(os.path.join(args.directory,name+'.json'), os.path.join(args.output,name+'.json'))
        print(os.path.join(args.output, name + '.json'))
        with open(os.path.join(args.output, name + '.json'), 'r+') as f:
            data = json.load(f)
            data["imageHeight"]= new_height
            data["imageWidth"]= new_width
            print(type(imagedata))
            data["imageData"] = imagedata.decode("utf-8")
            print(data["imageData"])
            for i in data['shapes']:
                points_list = i['points']

                points_list[0][0] = points_list[0][0] * ratio_x
                points_list[0][1] = points_list[0][1] * ratio_y

                points_list[1][0] = points_list[1][0] * ratio_x
                points_list[1][1] = points_list[1][1] * ratio_y

                points_list[2][0] = points_list[2][0] * ratio_x
                points_list[2][1] = points_list[2][1] * ratio_y

                points_list[3][0] = points_list[3][0] * ratio_x
                points_list[3][1] = points_list[3][1] * ratio_y

            f.seek(0)
            f.write(json.dumps(data, indent=4))
            f.truncate()
    else:
        print(name)
        shutil.copyfile(os.path.join(args.directory, name + '.json'), os.path.join(args.output, name + '.json'))

def get_filenames_and_full_paths_for_images(base_dir):
    path_list = []
    fn_list = []
    for path, subdirs, files in os.walk(base_dir):
        for name in files:
            if name.endswith(".jpg") or name.endswith('.png') or name.endswith('.PNG') or name.endswith('.JPG'):
                fn_list.append((name))
                get_path = os.path.join(path, name)
                path_list.append(get_path)

    return fn_list, path_list
def separate_filename_and_extension(path):
    name = os.path.basename(path)
    name = name.split('.')
    nameWithoutExt = name[0]
    extension = '.' + name[1]
    return nameWithoutExt, extension

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(os.path.join(directory)):
        os.makedirs(os.path.join(directory))

def resize(imagePath):
    img = cv2.imread(imagePath)
    name , ext = separate_filename_and_extension(imagePath)
    height = img.shape[0]
    width = img.shape[1]

    ratio_x = 208 / width
    ratio_y = 208 / height

    if height > target_height or width > target_width:
        print('Resizing')
        img = cv2.resize(img, (208, 208))
        cv2.imwrite(os.path.join(args.output,name+'.jpg'),img)
        _, im_arr = cv2.imencode('.jpg', img)
        im_bytes = im_arr.tobytes()
        im_b64 = base64.b64encode(im_bytes)
        edit_json(208, 208, ratio_x, ratio_y, name, im_b64, True)
        return 1
    else:
        print('No need to resize')
        cv2.imwrite(os.path.join(args.output,name+'.jpg'),img)
        _, im_arr = cv2.imencode('.jpg', img)
        im_bytes = im_arr.tobytes()
        im_b64 = base64.b64encode(im_bytes)
        edit_json(0, 0, 0, 0, name, im_b64,False)
        return 2

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Input')
    parser.add_argument('--directory', type=str, help='Destination File', default='/home/kaiser/Documents/filters/0.1-0.19')
    parser.add_argument('--output', type=str, help='Destination File', default='/home/kaiser/Documents/filters/0.1-0.19_out')
    args = parser.parse_args()
    target_height = 208
    target_width = 208
    ensure_dir(args.output)
    fileNameList , pathList = get_filenames_and_full_paths_for_images(args.directory)
    count = 0
    fileCount = 0
    folderCount = 0
    imageCount = 0
    for i in pathList:
        print(i)
        resize(i)
        if os.path.isfile(i):
            fileCount = fileCount + 1
            if i.endswith(".jpg"):
                imageCount = imageCount +1
        elif os.path.isdir(i):
            folderCount = folderCount +1
    print('Completed files - ',imageCount)