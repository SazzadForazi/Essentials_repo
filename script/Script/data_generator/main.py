import os
import argparse
import cv2

def extract_frame(input, output):
    filename = 'GH010817.mp4'
    file, extension = filename.split('.')
    # file = file[0]
    cap= cv2.VideoCapture(os.path.join(input, filename))
    frame_number = 1
    while(cap.isOpened()):
        ret, frame = cap.read()
        original_frame = frame.copy()
        frame = cv2.resize(frame, (960, 540))
        if ret == False:
            break
        else:
            frame_number += 1
            cv2.imshow('frame', frame)
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
            if key == ord('p'):
                cv2.waitKey(-1)
            if cv2.waitKey(50) == 32: # 32 for space, and 50 is for milisecond to wait for each frame
                cv2.imwrite(os.path.join(output, file+'_'+str(frame_number))+'.jpg', original_frame)
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Input')
    parser.add_argument('--input', type=str, help='Source File',
                        default='/home/kaiser/Documents/video_resources/1920x1080')
    parser.add_argument('--output', type=str, help='Destination File',
                        default='/home/kaiser/Documents/video_resources/1920x1080_out')
    args = parser.parse_args()
    extract_frame(args.input, args.output)