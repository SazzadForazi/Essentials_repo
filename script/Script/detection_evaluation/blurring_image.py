from pgmagick import Image
import json
import os
import argparse
import cv2
import numpy as np

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Input')
    parser.add_argument('--input', type=str, help='Source File',
                        default='/home/kaiser/datasets/model_1/blurry')
    parser.add_argument('--output', type=str, help='Destination File',
                        default='/home/kaiser/datasets/model_1/blurry_out')
    args = parser.parse_args()

    for filename in os.listdir(args.input):
        if filename.endswith('.jpg'):
            img = cv2.imread(os.path.join(args.input, filename))
            # sharpening image
            # img.sharpen(50)

            sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
            sharpen = cv2.filter2D(img, -1, sharpen_kernel)
            cv2.imshow('sharpen', sharpen)
            cv2.waitKey(500)
            # sharpen.write(os.path.join(args.output, filename))