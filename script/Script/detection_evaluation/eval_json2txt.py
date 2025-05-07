import json
import os
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Input')
    parser.add_argument('--input', type=str, help='Source File',
                        default='/home/kaiser/datasets/model_evaluation/input')
    parser.add_argument('--output', type=str, help='Destination File',
                        default='/home/kaiser/datasets/model_evaluation/gt')
    args = parser.parse_args()
    object_name = "np"

    for filename in os.listdir(args.input):
        if filename.endswith('.json'):
            with open(os.path.join(args.input, filename)) as f:
                jsondata = json.load(f)
                for shape in jsondata['shapes']:
                    points = shape['points']
                    tlX = int(points[0][0])
                    tlY = int(points[0][1])
                    brX = int(points[2][0])
                    brY = int(points[2][1])
                    with open(os.path.join(args.output, filename.replace('.json', '') + '.txt'), 'a+') as f:
                        f.write(f'{object_name} {tlX} {tlY} {brX} {brY}\n')