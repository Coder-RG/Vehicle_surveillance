import cv2
import os
import sys

class NoInputFile(Exception):
    def __init__(self):
        self.message = "\033[31mError:\033[0m No input file provided as argument"
        super().__init__(self.message)

class NoFileAccess(Exception):
    def __init__(self, file_name):
        self.message = "\033[31mError:\033[0m Cannot acces file: {}".format(file_name)

def delete_pre_frames():
    with os.scandir("frames/") as scanner:
        for frame in scanner:
            os.remove(frame)

def frameCapture(path):
    vidObj = cv2.VideoCapture(path)
    count = 0
    frame_id = 0
    while True:
        success, image = vidObj.read()
        if not success:
            break
        if count%60 == 0:
            cv2.imwrite("frames/frame%d.jpg" % frame_id, image)
            frame_id += 1
        count += 1

def main():
    try:
        if len(sys.argv) == 1:
            raise NoInputFile()
        file_name = sys.argv[1]
        if not os.access(file_name, os.F_OK):
            raise NoFileAccess(file_name)
    except Exception as e:
        print(e.message)
        sys.exit(1)
    delete_pre_frames()
    frameCapture()

if __name__ == "__main__":
    main()
