# -*- coding: utf-8 -*-
import argparse
import base64
import os
import time
import json
import math

import cv2
import numpy as np
import requests
import skvideo.io
from PIL import Image, ImageDraw, ImageFont


# =============================================================================
# Globals
DETECTOR_IP = '192.168.1.219'
DETECTOR_PORT = '5008'
RECOGNIZER_IP = '192.168.1.219'
RECOGNIZER_PORT = '5009'


cwd = os.getcwd()
rs = requests.session()


def truncate(f, n):
    return math.floor(f * 10 ** n) / 10 ** n


def is_video_file(path):
    allowed_extensions = ['.3gp', '.avi', '.flv', '.m4v', '.mkv', '.mov', '.mp4', '.mpg', '.mpeg', '.mts', '.webm',
                          '.wmv']
    ext = os.path.splitext(path)[1]
    return True if ext in allowed_extensions else False


def convert_base64(encoded_data):
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img


def calculate_fps(vid_path):
    data = skvideo.io.ffprobe(vid_path)['video']
    rate = data['@r_frame_rate']
    return rate


def extract_frame(vid_path, out_frames_dir):
    videogen = skvideo.io.vreader(vid_path)
    videometadata = skvideo.io.ffprobe(vid_path)
    # frame_rate = videometadata['video']['@avg_frame_rate']
    # print("fps for input vid : ", frame_rate)
    count = 0
    t1 = time.time()
    for frame in videogen:
        outputdata = frame
        # print(type(outputdata))
        im = Image.fromarray(outputdata)
        im.save(os.path.join(out_frames_dir, '{}{}.jpg'.format("frame", count)))
        # plt.imsave(os.path.join(out_frames_dir, '{}{}.jpg'.format("frame", count)), outputdata)
        # print(type(cv2.imread(os.path.join(out_frames_dir, '{}{}.jpg'.format("frame", count)))))
        count = count + 1
    t2 = time.time()
    print("time taken : ", t2 - t1)


def write_video(output_vid, out_frames_dir, rate):
    vid_out = skvideo.io.FFmpegWriter(output_vid, inputdict={'-r': rate, }, outputdict={
        '-r': rate, })
    # writer = skvideo.io.FFmpegWriter(output_vid)
    t1 = time.time()
    files = os.listdir(out_frames_dir)
    # for sorting the file names properly
    files.sort(key=lambda x: int(x[5:-4]))

    for i in range(0, len(files)):
        path = os.path.join(out_frames_dir, files[i])
        im = np.array(Image.open(path))
        # np_im = np.array(im)
        im_data = im.astype(np.uint8)
        # writer.writeFrame(im_data)
        vid_out.writeFrame(im_data)
        # skvideo.io.vwrite(output_vid, outputdata)
    # writer.close()
    vid_out.close()
    videometadata = skvideo.io.ffprobe(output_vid)
    # frame_rate = videometadata['video']['@avg_frame_rate']
    # print("fp for output vid : ", frame_rate)
    t2 = time.time()
    print("time taken : ", t2 - t1)


def read_image(input):
    exts = ['.jpg', '.JPG', 'jpeg', '.png']

    if os.path.isdir(input):
        for filename in sorted(os.listdir(input)):
            # if int(os.path.splitext(filename)[0]) <= 506:
            #     continue
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


def detect_plate(image_data):
    resp = rs.post(url='http://{}:{}/detect'.format(DETECTOR_IP, DETECTOR_PORT), data=image_data)
    resp.raise_for_status()
    return resp.json()


def call_recognizer(image_data):
    url = 'http://{}:{}/recognize'.format(RECOGNIZER_IP, RECOGNIZER_PORT)
    resp = rs.post(
        url=url,
        json=json.dumps(image_data))
    resp.raise_for_status()
    return resp.json()


def split_plate(img):
    height, width, d = img.shape
    height_half = int(height / 2)
    text_part = img[0:height_half, 0:width]
    number_part = img[height_half: height, 0: width]
    return text_part, number_part


def recognize_city(image_data):
    resp = rs.post(url='http://{}:5009/recognize/city'.format(args.ip), data=image_data)
    resp.raise_for_status()
    return resp.json()


def recognize_number(image_data):
    resp = rs.post(url='http://{}:5009/recognize/number'.format(args.ip), data=image_data)
    resp.raise_for_status()
    return resp.json()


def draw(filepath, plates):
    im = Image.open(filepath)
    bg_width = im.width
    bg_height = im.height

    for plate in plates:
        xmin = max(plate['bbox']['start_x'] * bg_width, 0)
        ymin = max(plate['bbox']['start_y'] * bg_height, 0)
        xmax = min(plate['bbox']['end_x'] * bg_width, bg_width)
        ymax = min(plate['bbox']['end_y'] * bg_height, bg_height)

        if 'text' in plate and 'number' in plate:
            text = "{}\n{}".format(plate['text'], plate['number'])
        else:
            text = f'{plate["probability"]:.6f}'

        # portion of image width you want text width to be
        if args.recognize:
            img_fraction = 0.20
        else:
            img_fraction = 0.10
        fontsize = 1
        font = ImageFont.truetype("Siyamrupali.ttf", size=fontsize, layout_engine=ImageFont.Layout.RAQM)

        while font.getlength(text) < img_fraction * im.size[0]:
            fontsize += 2
            font = ImageFont.truetype("Siyamrupali.ttf", size=fontsize, layout_engine=ImageFont.Layout.RAQM)

        if args.recognize:
            box_width = img_fraction * im.size[0]
        else:
            box_width = img_fraction * im.size[0] + 30

        if args.recognize:
            box_height = box_width / 4
        else:
            box_height = box_width / 3

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

        try:
            draw = ImageDraw.Draw(im)
            draw.rectangle([box_xmin, box_ymin, box_xmax, box_ymax], fill='yellow')
            draw.rectangle([xmin, ymin, xmax, ymax], outline='yellow', width=3)
            draw.text([box_xmin + 10, box_ymin, box_xmax, box_ymax], text, font=font, fill='black')
        except Exception as e:
            print(filepath)
            print(plates)
            raise

        output_filename = os.path.basename(filepath)
        im.save(os.path.join(args.outputdir, 'frames', output_filename))


def main(input):
    for n, file in enumerate(read_image(input)):
        filepath = file[0]
        filename = os.path.splitext(os.path.basename(filepath))[0]
        image_data = file[1]
        image_to_write = cv2.imread(filepath)

        t0 = time.time()
        detected_plates = detect_plate(image_data)
        t1 = time.time()

        for i, plate in enumerate(detected_plates):
            cv2.imwrite(os.path.join(args.outputdir, 'plates', '{}_{}.jpg'.format(filename, i)),
                        convert_base64(plate['image']))

            t1 = time.time()
            if args.recognize:
                resp = call_recognizer(plate['image'])

                city = resp[0][1]
                cs = truncate(resp[0][2], 2)
                detected_plates[i]['text'] = "[{:.2f}] {}".format(cs, city)

                number = resp[1][1]
                ns = truncate(resp[1][2], 2)
                detected_plates[i]['number'] = "[{:.2f}] {}".format(ns, number)

                text_part, number_part = split_plate(convert_base64(plate['image']))

                cv2.imwrite(os.path.join(args.outputdir, 'texts', '{}_{}_text.jpg'.format(filename, i)), text_part)
                cv2.imwrite(os.path.join(args.outputdir, 'numbers', '{}_{}_number.jpg'.format(filename, i)),
                            number_part)

                # text_part_path = os.path.join(args.outputdir, 'texts', '{}_{}_text.jpg'.format(filename, i))
                # with open(text_part_path, "rb") as f:
                #     text_part = f.read()

                # number_part_path = os.path.join(args.outputdir, 'numbers', '{}_{}_number.jpg'.format(filename, i))
                # with open(number_part_path, "rb") as f:
                #     number_part = f.read()

                # text = recognize_city(text_part)
                # detected_plates[i]['text'] = text['msg']
                #
                # number = recognize_number(number_part)
                # detected_plates[i]['number'] = number['msg']

        # Print in console
        if n == 0:
            print("{:<50} {:<10} {:13}".format('FILENAME', '# PLATES', 'TIME TOOK(ms)'))
            print("{:<50} {:<10} {:13}".format('-' * 50, '-' * 10, '-' * 13))
        print("{:<50} {:<10} {:>13.2f}".format(filename, len(detected_plates), (t1 - t0) * 1000, ))

        # Output to file
        if len(detected_plates) > 0:
            draw(filepath, detected_plates)


def path_validator(string):
    if os.path.isdir(string):
        return string
    elif os.path.isfile(string):
        return string
    else:
        raise Exception("not a file or directory")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Recognize number plate from a vehicle image')
    parser.add_argument('--input', type=path_validator, default='/home/kaiser/datasets/0004')
    parser.add_argument('--outputdir', default='/home/kaiser/datasets/0004_out')
    parser.add_argument('--recognize', default=True, action='store_true')
    parser.add_argument('--ip', type=str, default='192.168.1.219',
                        help='Number plate detection & recognition server IP address')
    args = parser.parse_args()

    # Make output directories
    OUTPUT_DIR = args.outputdir if args.outputdir else os.path.join(cwd, 'output')
    FRAME_DIR = os.path.join(OUTPUT_DIR, "frames")
    TEXT_DIR = os.path.join(OUTPUT_DIR, "texts")
    NUMBER_DIR = os.path.join(OUTPUT_DIR, "numbers")
    PLATE_DIR = os.path.join(OUTPUT_DIR, "plates")

    os.makedirs(FRAME_DIR, exist_ok=True)
    os.makedirs(TEXT_DIR, exist_ok=True)
    os.makedirs(NUMBER_DIR, exist_ok=True)
    os.makedirs(PLATE_DIR, exist_ok=True)

    if is_video_file(args.input):
        fps = calculate_fps(args.input)
        extract_frame(args.input, FRAME_DIR)
        main(FRAME_DIR)
        write_video(os.path.join(OUTPUT_DIR, 'output.mp4'), FRAME_DIR, fps)
    else:
        main(args.input)