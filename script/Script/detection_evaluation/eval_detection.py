import argparse
import json
import requests
import os

DETECTOR_IP = '192.168.1.219'
DETECTOR_PORT = '5008'

rs = requests.session()

def call_detector(image_data):
    url = 'http://{}:{}/detect'.format(DETECTOR_IP, DETECTOR_PORT)
    resp = rs.post(
        url=url,
        data=image_data)
    resp.raise_for_status()
    response = resp.json()
    return response

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Input')
    parser.add_argument('--input', type=str, help='Source File',
                        default='/home/kaiser/datasets/model_evaluation/input')
    parser.add_argument('--output', type=str, help='Destination File',
                        default='/home/kaiser/datasets/model_evaluation/det')
    parser.add_argument('--input_gt', type=str, help='Source File',
                        default='/home/kaiser/datasets/model_evaluation/gt')
    args = parser.parse_args()
    object_name = "np"
    count = 0
    not_detected_images = []

    for filename in os.listdir(args.input):
        if filename.endswith('.jpg'):
            img = open(os.path.join(args.input, filename), "rb")
            detected_plates = call_detector(img)
            if detected_plates != []:
                for i, plate in enumerate(detected_plates):
                    pred = "{:.5f}".format(detected_plates[i]['probability'])
                    tlX = int(detected_plates[i]['bbox']['start_x'] * 1920)
                    tlY = int(detected_plates[i]['bbox']['start_y'] * 1080)
                    brX = int(detected_plates[i]['bbox']['end_x'] * 1920)
                    brY = int(detected_plates[i]['bbox']['end_y'] * 1080)

                    with open(os.path.join(args.output, filename.replace('.jpg', '') + '.txt'), 'a+') as f:
                        f.write(f'{object_name} {pred} {tlX} {tlY} {brX} {brY}\n')
            else:
                count = count + 1
                not_detected_images.append(filename)
                print("NOT detected!")

                for f in os.listdir(args.input_gt):
                    if (os.path.splitext(f)[0]) == (os.path.splitext(filename)[0]):
                        with open(os.path.join(args.input_gt, f), 'r') as fp:
                            x = len(fp.readlines())
                        for i in range(x):
                            with open(os.path.join(args.output, filename.replace('.jpg', '') + '.txt'), 'a+') as f:
                                f.write(f'{object_name} 0.0 0 0 0 0\n')

    print(f'Number of plates not detected: {count}')
    print('Name of not detected files: ')
    print(not_detected_images)