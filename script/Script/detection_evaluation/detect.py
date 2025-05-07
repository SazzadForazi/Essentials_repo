# -*- coding: utf-8 -*-
import argparse
import os
import time
import requests
from PIL import Image, ImageDraw, ImageFont

cwd = os.getcwd()
rs = requests.session()

# unicode_font = ImageFont.truetype("Siyamrupali.ttf", size=18, layout_engine=ImageFont.LAYOUT_RAQM)

def draw(filepath, plates):
    im = Image.open(filepath)
    bg_width = im.width
    bg_height = im.height

    for plate in plates:
        xmin = max(plate['bbox']['start_x'] * bg_width, 0)
        ymin = max(plate['bbox']['start_y'] * bg_height, 0)
        xmax = min(plate['bbox']['end_x'] * bg_width, bg_width)
        ymax = min(plate['bbox']['end_y'] * bg_height, bg_height)

        # text = "{} ({:.2f})".format(plate['name'], plate['score'])
        text = 'Dhaka Metro - Ga'

        # portion of image width you want text width to be
        img_fraction = 0.20
        fontsize = 1
        font = ImageFont.truetype("Siyamrupali.ttf", size=fontsize, layout_engine=ImageFont.LAYOUT_RAQM)
        while font.getsize(text)[0] < img_fraction * im.size[0]:
            fontsize += 1
            font = ImageFont.truetype("Siyamrupali.ttf", size=fontsize, layout_engine=ImageFont.LAYOUT_RAQM)

        box_width = img_fraction * im.size[0] + 20
        box_height = box_width / 6
        distance = 10

        mid = xmin + int((xmax - xmin) / 2)
        box_xmin = max(mid - box_width / 2, 0)
        box_xmax = min(box_xmin + box_width, bg_width)

        if box_xmax >= bg_width:
            box_xmin = box_xmax - box_width

        box_ymin = ymax + distance
        box_ymax = box_ymin + box_height

        if box_ymax > bg_height:
            box_ymin = ymin - distance - box_height
            box_ymax = box_ymin + box_height

        draw = ImageDraw.Draw(im)
        draw.rectangle([box_xmin, box_ymin, box_xmax, box_ymax], fill='yellow')
        draw.rectangle([xmin, ymin, xmax, ymax], outline='yellow', width=3)

        try:
            draw.text([box_xmin + 10, box_ymin, box_xmax, box_ymax], text, font=font, fill='black')
        except Exception as e:
            print(filepath)
            print(plates)
            raise

        output_filename = os.path.basename(filepath)
        im.save(os.path.join(args.outputdir, output_filename))

def call_detect_api(image_data):
    resp = rs.post(url='http://{}:{}/detect'.format(args.ip, args.port), data=image_data)
    resp.raise_for_status()
    return resp.json()

def get_files():
    exts = ['.jpg', '.JPG', 'jpeg', '.png']
    video_exts = ['.mp4']
    input = args.input

    if os.path.isdir(input):
        for filename in sorted(os.listdir(input)):
            ext = os.path.splitext(filename)[1]
            if ext in exts:
                with open(os.path.join(input, filename), "rb") as f:
                    image_data = f.read()
                yield os.path.join(input, filename), image_data

    elif os.path.isfile(input):
        ext = os.path.splitext(input)[1]
        if ext in exts:
            with open(input, "rb") as f:
                image_data = f.read()
            yield input, image_data

def detect():
    for n, file in enumerate(get_files()):
        filepath = file[0]
        filename = os.path.splitext(os.path.basename(filepath))[0]
        image_data = file[1]

        t0 = time.time()
        detected_plates = call_detect_api(image_data)
        t1 = time.time()

        # plates = []
        # for plate in detected_plates:
        #     plates.append(plate)

        # Print in console
        # print(detected_plates)
        if n == 0:
            print("{:<50} {:<10} {:13}".format('FILENAME', '# PLATES', 'TIME TOOK(ms)'))
            print("{:<50} {:<10} {:13}".format('-' * 50, '-' * 10, '-' * 13))
        print("{:<50} {:<10} {:>13.2f}".format(filename, len(detected_plates), (t1 - t0) * 1000))

        # print(plates)
        # result = sorted(plates, key=lambda k: k['score'], reverse=True)
        # output = ', '.join(["{}({:.2f})".format(x['name'], x['score']) for x in plates])

        # Output to file
        draw(filepath, detected_plates)

def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Recognize number plate from a directory of images of vehicle')
    parser.add_argument('--input', type=dir_path, default='/home/kaiser/Documents/projects/detection_evaluation/input')
    parser.add_argument('--outputdir', type=dir_path, default='/home/kaiser/Documents/projects/detection_evaluation/detection_output')
    parser.add_argument('--ip', type=str, default='192.168.1.219', help='Number plate detection server IP address')
    parser.add_argument('--port', type=str, default='5008', help='Number plate detection server port')
    args = parser.parse_args()
    detect()