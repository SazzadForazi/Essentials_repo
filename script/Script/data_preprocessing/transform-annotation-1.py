# annotation checking script
import json
import os

input_dir = '/home/kaiser/Downloads/0501/fazle/1'

def normalize_coordinates(row_i, col_j, img):
    num_rows, num_cols = img.shape[:2]
    x = col_j / (num_cols - 1.)
    y = row_i / (num_rows - 1.)
    return x, y

for filename in os.listdir(input_dir):
    if filename.endswith('.json'):
        try:
            with open(os.path.join(input_dir, filename)) as f:
                jsondata = json.load(f)
                w = jsondata['imageWidth']
                h = jsondata['imageHeight']
                for shape in jsondata['shapes']:
                    points = shape['points']
                    if len(points) == 4:
                        # N, tlx, tly, trx, try, brx, bry, blx, bly, LABEL,
                        N = len(points)
                        tlX = points[0][0] * w
                        tlY = points[0][1] * h

                        trX = points[1][0] * w
                        trY = points[1][1] * h

                        brX = points[2][0] * w
                        brY = points[2][1] * h

                        blX = points[3][0] * w
                        blY = points[3][1] * h
                        LABEL = shape['label']
                    else:
                        print(f'ERROR: Points != 4 {filename}')
        except:
            print(f'filename: {filename}')

print('Finished!')