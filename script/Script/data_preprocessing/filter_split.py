# split folder according to the filter of the np data
import json
import os
import re
import shutil
import csv

input_dir = '/home/kaiser/datasets/0_original_annotated_detector/all_in_one'
output_dir = '/home/kaiser/Documents/r_-5+5_z_.1-10'
filename_list = []

with open("/home/kaiser/Documents/r_-5+5_z_.1-10.csv", 'r') as file:
  csvreader = csv.reader(file)
  next(csvreader, None)
  for row in csvreader:
    filename_list.append(row[0])

for filename in filename_list:
    filename_json = filename.replace('.jpg', '') + '.json'
    shutil.copy(os.path.join(input_dir, filename), os.path.join(output_dir, filename))
    shutil.copy(os.path.join(input_dir, filename_json), os.path.join(output_dir, filename_json))