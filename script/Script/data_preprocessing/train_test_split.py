# train-test split of the np data
import json
import os
import re
import shutil
import random

input_dir = '/home/kaiser/datasets/0_original_annotated_detector/all_in_one'
output_dir = '/home/kaiser/datasets/model_evaluation/input'
filename_list = []
TEST_SIZE = 1000

for filename in os.listdir(input_dir):
    if filename.endswith('.jpg'):
        filename_list.append(filename)

random_list = random.sample(filename_list, TEST_SIZE)

for filename in random_list:
    filename_json = filename.replace('.jpg', '') + '.json'
    # shutil.move(os.path.join(input_dir, filename), os.path.join(output_dir, filename))
    # shutil.move(os.path.join(input_dir, filename_json), os.path.join(output_dir, filename_json))

    shutil.copy(os.path.join(input_dir, filename), os.path.join(output_dir, filename))
    shutil.copy(os.path.join(input_dir, filename_json), os.path.join(output_dir, filename_json))