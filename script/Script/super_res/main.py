import os
import cv2
import matplotlib.pyplot as plt

input_dir = '/home/kaiser/projects/super_res/input'
output_dir = '/home/kaiser/projects/super_res/output'
model_path = '/home/kaiser/projects/super_res/models/EDSR_x4.pb'

for filename in os.listdir(input_dir):
    if filename.endswith('.jpg'):
        img = cv2.imread(os.path.join(input_dir, filename))
        sr = cv2.dnn_superres.DnnSuperResImpl_create()
        path = model_path
        sr.readModel(path)
        sr.setModel("edsr", 4)
        # sr.setModel("lapsrn", 8)
        # sr.setModel("fsrcnn", 3)
        # sr.setModel("espcn", 3)
        result = sr.upsample(img)
        # Resized image
        resized = cv2.resize(img, dsize=None, fx=4, fy=4)
        # resized = cv2.resize(img, dsize=None, fx=8, fy=8)
        # resized = cv2.resize(img, dsize=None, fx=3, fy=3)
        cv2.imwrite(os.path.join(output_dir, filename), resized)
        # resized.save(os.path.join(output_dir, filename))