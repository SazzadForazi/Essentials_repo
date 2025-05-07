import os
from PIL import Image, ImageDraw

image_folder = "/home/kaiser/Documents/projects/detection_evaluation/45_images"
ground_truth_folder = "/home/kaiser/Documents/projects/detection_evaluation/groundtruths"
detections_folder = "/home/kaiser/Documents/projects/detection_evaluation/detections"
output_folder = "/home/kaiser/Documents/projects/detection_evaluation/45_images_output"

def draw(filepath, x1, y1, x2, y2, color):
    im = Image.open(filepath)
    draw = ImageDraw.Draw(im)
    draw.rectangle([x1, y1, x2, y2], outline=color, width=3)
    output_filename = filepath.rsplit('/')[-1]
    im.save(os.path.join(output_folder, output_filename))

for gfile in os.listdir(ground_truth_folder):
    with open(os.path.join(ground_truth_folder, gfile)) as f:
        lines = f.readlines()
        for line in lines:
            splits = line.split()
            x1 = int(splits[1])
            y1 = int(splits[2])
            x2 = int(splits[3])
            y2 = int(splits[4])
            draw(os.path.join(image_folder, gfile.replace('.txt', '.jpg')), x1, y1, x2, y2, 'green')

for dfile in os.listdir(detections_folder):
    with open(os.path.join(detections_folder, dfile)) as f:
        lines = f.readlines()
        for line in lines:
            splits = line.split()
            x1 = int(splits[2])
            y1 = int(splits[3])
            x2 = int(splits[4])
            y2 = int(splits[5])
            draw(os.path.join(output_folder, dfile.replace('.txt', '.jpg')), x1, y1, x2, y2, 'red')