# calculate the zoom, distortion and rotation of np and make a report in a .csv file
import json
import os
import re
import math
import pandas as pd

input_dir = '/home/kaiser/datasets/0_original_annotated_detector/all_in_one'

filename_list = []
zoom_list = []
angle_list = []
rotation_list = []
CONSTANT = 0.000001

# Function to sort the filename numerically
def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(data, key=alphanum_key)

# Function to find the interior angles of the cyclic quadrilateral
def findAngles(fn, a, b, c, d):
    numerator = a * a + d * d - b * b - c * c
    denominator = 2 * (a * b + c * d)
    x = numerator / denominator
    print(f'filename: {fn}, x: {x}')
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
    tmp_zoom = 0
    tmp_angle = 0
    tmp_rotation = 0
    if filename.endswith('.json'):
        with open(os.path.join(input_dir, filename)) as f:
            jsondata = json.load(f)
            w = jsondata['imageWidth']
            h = jsondata['imageHeight']
            total_area = w * h
            N = len(jsondata['shapes'])
            filename_list.append(filename.replace('.json', '') + '.jpg')

            if N == 1:
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

                    npw = abs(tlX - trX) + abs(tlY - trY)
                    nph = abs(trX - brX) + abs(trY - brY)
                    np_area = npw * nph

                    zoom = round(((np_area / total_area) * 100), 2)
                    zoom_list.append(zoom)

                    A = abs(tlX - trX) + abs(tlY - trY)
                    B = abs(trX - brX) + abs(trY - brY)
                    C = abs(brX - blX) + abs(brY - blY)
                    D = abs(blX - tlX) + abs(blY - tlY)

                    a, b, c, d = findAngles(filename, A, B, C, D)
                    a1 = abs(a - 90)
                    b1 = abs(b - 90)
                    c1 = abs(c - 90)
                    d1 = abs(d - 90)
                    total_distortion = round((a1 + b1 + c1 + d1), 2)
                    angle_list.append(total_distortion)

                    m = ((tlY - trY) / (tlX - trX + CONSTANT))
                    angle_rad = math.atan(m)
                    angle_deg = round((math.degrees(angle_rad)), 2)
                    rotation_list.append(angle_deg)

            else:
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

                    npw = abs(tlX - trX) + abs(tlY - trY)
                    nph = abs(trX - brX) + abs(trY - brY)
                    np_area = npw * nph
                    zoom = round(((np_area / total_area) * 100), 2)

                    A = abs(tlX - trX) + abs(tlY - trY)
                    B = abs(trX - brX) + abs(trY - brY)
                    C = abs(brX - blX) + abs(brY - blY)
                    D = abs(blX - tlX) + abs(blY - tlY)

                    a, b, c, d = findAngles(filename, A, B, C, D)
                    a1 = abs(a - 90)
                    b1 = abs(b - 90)
                    c1 = abs(c - 90)
                    d1 = abs(d - 90)
                    total_distortion = round((a1 + b1 + c1 + d1), 2)

                    m = ((tlY - trY) / (tlX - trX + CONSTANT))
                    angle_rad = math.atan(m)
                    angle_deg = round((math.degrees(angle_rad)), 2)

                    if zoom > tmp_zoom:
                        tmp_zoom = zoom
                    if total_distortion > tmp_angle:
                        tmp_angle = total_distortion
                    if abs(angle_deg) > tmp_rotation:
                        tmp_rotation = angle_deg

                zoom_list.append(tmp_zoom)
                angle_list.append(tmp_angle)
                rotation_list.append(tmp_rotation)

data_dict = {'image': filename_list, 'zoom': zoom_list, 'distortion': angle_list, 'rotation': rotation_list}
dataframe = pd.DataFrame(data_dict)
dataframe.to_csv('/home/kaiser/projects/data_preprocessing_scripts/report_today.csv')