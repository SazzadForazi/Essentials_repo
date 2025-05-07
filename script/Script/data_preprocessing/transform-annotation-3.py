# .txt file generation script
import json
import os

input_dir = '/home/kaiser/Documents/filters/0.1-0.19_out'
output_dir = '/home/kaiser/Documents/filters/0.1-0.19_out_txt'

def normalize_coordinates(row_i, col_j, img):
    num_rows, num_cols = img.shape[:2]
    x = col_j / (num_cols - 1.)
    y = row_i / (num_rows - 1.)
    return x, y

for filename in os.listdir(input_dir):
    if filename.endswith('.json'):
        with open(os.path.join(input_dir, filename)) as f:
            jsondata = json.load(f)
            w = jsondata['imageWidth']
            h = jsondata['imageHeight']
            output = ''
            if len(jsondata['shapes']) != 1:
                print(filename, len(jsondata['shapes']))
            for shape in jsondata['shapes']:
                points = shape['points']
                if len(points) == 4:
                    N = len(points)
                    tlX = points[0][0] / w
                    tlY = points[0][1] / h

                    trX = points[1][0] / w
                    trY = points[1][1] / h

                    brX = points[2][0] / w
                    brY = points[2][1] / h

                    blX = points[3][0] / w
                    blY = points[3][1] / h
                    # LABEL = shape['label']
                    LABEL = 'white'
                    # LABEL = 'green'
                    with open(os.path.join(output_dir, filename.replace('.json', '') + '.txt'), 'a+') as f:
                        f.write(f'{N},{tlX},{trX},{brX},{blX},{tlY},{trY},{brY},{blY},{LABEL},\n')
                else:
                    print(f'ERROR: Points != 4 {filename}')