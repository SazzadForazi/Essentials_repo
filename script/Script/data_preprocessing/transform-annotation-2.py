# Image resizing and edit json script (1920x1080)
import os
import argparse
import cv2
import shutil
import json
import base64
from os.path import exists

def edit_json(new_height, new_width, ratio, name,imagedata,flag):
    if flag:
        # print(name)
        shutil.copyfile(os.path.join(args.directory,name+'.json'), os.path.join(args.output,name+'.json'))
        print(os.path.join(args.output, name + '.json'))
        with open(os.path.join(args.output, name + '.json'), 'r+') as f:
            data = json.load(f)
            #print(data['shapes'])
            data["imageHeight"]= new_height
            data["imageWidth"]= new_width
            print(type(imagedata))
            data["imageData"] = imagedata.decode("utf-8")
            print(data["imageData"])
            for i in data['shapes']:
                points_list = i['points']

                points_list[0][0] = points_list[0][0] * ratio
                points_list[0][1] = points_list[0][1] * ratio

                points_list[1][0] = points_list[1][0] * ratio
                points_list[1][1] = points_list[1][1] * ratio

                points_list[2][0] = points_list[2][0] * ratio
                points_list[2][1] = points_list[2][1] * ratio

                points_list[3][0] = points_list[3][0] * ratio
                points_list[3][1] = points_list[3][1] * ratio

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
    if height > target_height or width > target_width:
        if height > target_height and height > width:
            ratio = target_height / height
            new_height = height * ratio
            new_width = width * ratio

        else:
            ratio = target_width / width
            new_height = height * ratio
            new_width = width * ratio

        print('Resizing')
        img = cv2.resize(img,(int(new_width),int(new_height)))
        cv2.imwrite(os.path.join(args.output,name+'.jpg'),img)

        _, im_arr = cv2.imencode('.jpg', img)
        im_bytes = im_arr.tobytes()
        im_b64 = base64.b64encode(im_bytes)
        edit_json(new_height, new_width, ratio, name, im_b64,True)

        return 1
    else:
        print('No need to resize')

        cv2.imwrite(os.path.join(args.output,name+'.jpg'),img)

        _, im_arr = cv2.imencode('.jpg', img)
        im_bytes = im_arr.tobytes()
        im_b64 = base64.b64encode(im_bytes)
        #print(im_b64)

        edit_json(0, 0, 0, name, im_b64,False)
        return 2

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Input')
    parser.add_argument('--directory', type=str, help='Source File', default='/home/kaiser/Downloads/0101/motaleb_bhai/gdrive/from_rangpur_road')
    parser.add_argument('--output', type=str, help='Destination File', default='/home/kaiser/Downloads/0101/motaleb_bhai/gdrive/from_rangpur_road_out')
    args = parser.parse_args()
    # target_height = 540
    # target_width = 960
    # target_height = 208
    # target_width = 208
    target_height = 1080
    target_width = 1920
    ensure_dir(args.output)

    fileNameList , pathList = get_filenames_and_full_paths_for_images(args.directory)
    count = 0
    fileCount = 0
    folderCount = 0
    imageCount = 0
    # mycount = 0
    for i in pathList:
        print(i)
        resize(i)

        # filename = os.path.basename(i)
        # # print(filename)

        # file_name, file_extension = os.path.splitext(filename)
        # # print(file_extension)

        # # /home/kaiserhamidrabbi/Downloads/[4]-tigerit/732022/test/9453.jpg
        # # folder_path = '/home/kaiserhamidrabbi/Downloads/[4]-tigerit/732022/test'
        # folder_path = '/home/kaiserhamidrabbi/Downloads/output/'

        # # print(folder_path + file_name + '.json')

        # file_exists = exists(folder_path + file_name + '.json')
        # # print(file_exists)
        
        # if not file_exists:
        #     # os.remove(folder_path + file_name + file_extension)
        #     # print(folder_path + file_name + file_extension)
        #     mycount = mycount + 1

        if os.path.isfile(i):
            fileCount = fileCount + 1
            if i.endswith(".jpg"):
                imageCount = imageCount +1

        elif os.path.isdir(i):
            folderCount = folderCount +1


    print('Completed files - ',imageCount)
    # print(mycount)