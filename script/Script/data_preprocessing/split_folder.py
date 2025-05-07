# split the np image folder
import json
import os
import re
import shutil

input_dir = '/home/kaiser/datasets/0_original_annotated_detector/fazle'
output_dir = '/home/kaiser/datasets/0_original_annotated_detector/fazle_out'
filename_list = []


# Function to sort the filename numerically
def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(data, key=alphanum_key)

for filename in sorted_alphanumeric(os.listdir(input_dir)):
    filename_list.append(filename)
print(filename_list[0], filename_list[-1])
print(len(filename_list))
# print(filename_list)

# for i, file in enumerate(filename_list):
#     shutil.move(os.path.join(input_dir, file), os.path.join(output_dir, file))
#     if i == ((len(filename_list) / 2) - 1):
#         break