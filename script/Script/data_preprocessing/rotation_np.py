# calculate the rotation of np
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

                c = 0.0000000000001
                m = ((tlY - trY) / (tlX - trX + c))
                angle_rad = math.atan(m)
                angle_deg = math.degrees(angle_rad)
                print(f'Rotation= {angle_deg:.2f}')