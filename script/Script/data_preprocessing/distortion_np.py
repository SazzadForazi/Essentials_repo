# calculate the distortion of np
import json
import os
import math
import re

input_dir = '/home/kaiser/projects/data_preprocessing_scripts/input'

# Function to sort the filename numerically
def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(data, key=alphanum_key)

# Function to find the interior angles of the cyclic quadrilateral
def findAngles(a, b, c, d):
    numerator = a * a + d * d - b * b - c * c
    denominator = 2 * (a * b + c * d)
    x = numerator / denominator
    A = ((math.acos(x) * 180) / 3.141592)

    numerator = a * a + b * b - c * c - d * d
    x = numerator / denominator
    B = ((math.acos(x) * 180) / 3.141592)

    numerator = c * c + b * b - a * a - d * d
    x = numerator / denominator
    C = ((math.acos(x) * 180) / 3.141592)

    numerator = d * d + c * c - a * a - b * b
    x = numerator / denominator
    D = ((math.acos(x) * 180) / 3.141592)

    return A, B, C, D

for filename in sorted_alphanumeric(os.listdir(input_dir)):
    if filename.endswith('.json'):
        with open(os.path.join(input_dir, filename)) as f:
            jsondata = json.load(f)
            w = jsondata['imageWidth']
            h = jsondata['imageHeight']
            total_area = w * h
            N = len(jsondata['shapes'])
            print(f'Total Plate(s): {N} in {filename}')
            for shape in jsondata['shapes']:
                points = shape['points']

                tlX = points[0][0]
                tlY = points[0][1]

                trX = points[1][0]
                trY = points[1][1]

                brX = points[2][0]
                brY = points[2][1]

                blX = points[3][0]
                blY = points[3][1]

                A = abs(tlX - trX) + abs(tlY - trY)
                B = abs(trX - brX) + abs(trY - brY)
                C = abs(brX - blX) + abs(brY - blY)
                D = abs(blX - tlX) + abs(blY - tlY)

                a, b, c, d = findAngles(A, B, C, D)
                # print(f'Angles: {a:.2f} {b:.2f} {c:.2f} {d:.2f}')
                a1 = abs(a - 90)
                b1 = abs(b - 90)
                c1 = abs(c - 90)
                d1 = abs(d - 90)
                total_distortion = a1 + b1 + c1 + d1
                # print(f'Distortions: {a1:.2f} {b1:.2f} {c1:.2f} {d1:.2f}')
                print(f'Total Distortion: {total_distortion:.2f}')