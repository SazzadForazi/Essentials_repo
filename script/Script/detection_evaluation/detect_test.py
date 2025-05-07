import argparse
import json
import requests
import os
import base64

DETECTOR_IP = '192.168.1.219'
DETECTOR_PORT = '5008'
rs = requests.session()

def detect_plate(image_data):
    resp = rs.post(url='http://{}:{}/detect'.format(DETECTOR_IP, DETECTOR_PORT), data=image_data)
    resp.raise_for_status()
    return resp.json()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Input')
    parser.add_argument('--input', type=str, help='Source File',
                        default='/home/kaiser/Downloads/double')
    parser.add_argument('--output', type=str, help='Destination File',
                        default='/home/kaiser/Documents/projects/detection_evaluation/detections')
    parser.add_argument('--output_image', type=str, help='Destination File',
                        default='/home/kaiser/Documents/projects/detection_evaluation/detection_images')
    args = parser.parse_args()
    object_name = "np"
    count = 0
    not_detected_images = []

    for filename in os.listdir(args.input):
        if filename.endswith('.jpg'):
            img = open(os.path.join(args.input, filename), "rb")
            detected_plates = detect_plate(img)
            print(len(detected_plates))
            if detected_plates != []:
                for i, plate in enumerate(detected_plates):
                    img = detected_plates[i]['image']
                    pred = "{:.5f}".format(detected_plates[i]['probability'])
                    tlX = int(detected_plates[i]['bbox']['start_x'] * 1920)
                    tlY = int(detected_plates[i]['bbox']['start_y'] * 1080)
                    brX = int(detected_plates[i]['bbox']['end_x'] * 1920)
                    brY = int(detected_plates[i]['bbox']['end_y'] * 1080)

                    with open(os.path.join(args.output_image, filename.replace('.jpg', '') + f'_{i+1}.jpg'), 'ab+') as fh:
                        fh.write(base64.b64decode(img))

                    with open(os.path.join(args.output, filename.replace('.jpg', '') + '.txt'), 'a+') as f:
                        f.write(f'{object_name} {pred} {tlX} {tlY} {brX} {brY}\n')
            else:
                count = count + 1
                not_detected_images.append(filename)
                print("NOT detected!")
    print(f'Number of plates not detected: {count}')
    print('Name of not detected files: ')
    print(not_detected_images)