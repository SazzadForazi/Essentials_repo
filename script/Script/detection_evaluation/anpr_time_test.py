# -*- coding: utf-8 -*-
import os
import time

import requests

cwd = os.getcwd()
rs = requests.session()


def read_image(input):
    for filename in sorted(os.listdir(input)):
        multipart_form_data = {
            'file': (filename, open(os.path.join(input, filename), "rb"))
        }
        yield os.path.join(input, filename), multipart_form_data


def recognize_plate(multipart_form_data):
    resp = rs.post(url='http://{}:5010/recognize'.format(server_ip), files=multipart_form_data)
    resp.raise_for_status()
    return resp.json()


def main(input):
    for n, file in enumerate(read_image(input)):
        filepath = file[0]
        multipart_form_data = file[1]
        filename = os.path.splitext(os.path.basename(filepath))[0]
        resp = recognize_plate(multipart_form_data)

        # Print in console
        #if n == 0:
            #print("{:<50} {}".format('FILENAME', 'PLATES'))
            #print("{:<50} {}".format('-' * 50, '-' * 20))
        #print("{:<50} {}".format(filename,', '.join([x['city']['msg'] + ' ' + x['number']['msg'] for x in resp['result']])))


if __name__ == '__main__':
    server_ip = "127.0.0.1"
    #input_directories = [['./images/1920x1080', 12.469], ['./images/960x540', 9.110]]
    input_directories = [['./images/1920x1080', 12.469]]
    while True:
        for item in input_directories:
            input_dir = item[0]
            expected_time = item[1]
            t0 = time.time()
            main(input_dir)
            print("==========================================================================")
            print("time took: {:.3f} seconds (expected time: ~{} seconds)".format(time.time() - t0, expected_time))
