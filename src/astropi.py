#!/usr/bin/env python3.9
##
## EPITECH PROJECT, 2020
## Astropi
## File description:
## astropi
##

from sys import argv, stderr, exit, stdin
from datetime import datetime
from threading import Thread, Event

import cv2
import os
import numpy as np

event = Event()


def generate_mask(image, seuil):
    """Generate a mask composed by black or white pixels."""
    height, width = image.shape
    mask = np.zeros([height, width], np.uint8)
    image = image.astype(np.int32)
    for y in range(height):
        for x in range(width):
            if abs(0 - image[y][x]) > seuil:
                mask[y][x] = 255
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=3)
    return mask


def detect_object(msk):
    minx, miny = -1, -1
    maxx, maxy = -1, -1
    lenbool = False
    heithbool = False
    voidbool = True
    for i in range(len(msk)):
        for x in range(len(msk[i])):
            if msk[i][x] != 0:
                voidbool = False
                lenbool = True
                if heithbool != True:
                    minx = x
                    miny = i
                    heithbool = True
            if msk[i][x] != 255 and lenbool == True:
                lenbool = False
                maxx = x
        if heithbool == True and voidbool == True:
            maxy = i - 1
            break
        voidbool = True
    start_point = (minx - 1, miny - 1)
    end_point = (maxx + 1, maxy + 1)
    return start_point, end_point


def getCommand(var):
    while True:
        for line in stdin:
            if line.rstrip() == "help":
                print("Command executable:\n")
                print("\'screenshoot border\' or \'s\':\ttacke a screenshoot with border.")
                print("\'screenshoot\' or \'d\':\t\ttacke a screenshoot without border.")
                print("\'record\' or \'v\':\t\tStart a record of a video.")
                print("\'save\' or \'p\':\t\t\tSave the record of the video")
                print("\'quit\' or \'stop\' or \'exit\':\tExit the programe")
            elif line.rstrip() == "quit" or line.rstrip() == "stop" or line.rstrip() == "exit":
                break
            elif line.rstrip() == "screenshoot" or line.rstrip() == "s":
                var[0] = 's'
            elif line.rstrip() == "screenshoot border" or line.rstrip() == "d":
                var[0] = 'd'
            elif line.rstrip() == "record" or line.rstrip() == "v":
                var[0] = 'v'
            elif line.rstrip() == "save" or line.rstrip() == "p":
                var[0] = 'p'
        break
    var[0] = 'q'

def main(file):
    """Main function."""
    try:
        my_var = ['l']
        t = Thread(target=getCommand, args=(my_var, ))
        t.start()
        cap = cv2.VideoCapture()
        cap.open(file)
        video = False
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = False
        while True:
            now = datetime.now()
            ret, frame = cap.read()
            key = cv2.waitKey(1) & 0xFF
            if my_var[0] == 'd':
                my_var[0] = 'l'
                cv2.imwrite(os.environ.get('HOME') + "/Desktop/" + now.strftime("%d.%m.%Y-%H:%M:%S") + ".tif", frame)
                print("Image saved as " + os.environ.get('HOME') + "/Desktop/" + now.strftime("%d.%m.%Y-%H:%M:%S") + ".tif")
            if not ret:
                continue
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            msk = generate_mask(gray, 10)
            start_point, end_point = detect_object(msk)
            frame = cv2.rectangle(frame, start_point, end_point, (0, 0, 255), 2)
            cv2.imshow('video', frame)
            # cv2.imshow('mask', msk)
            if my_var[0] == 'q':
                break
            if my_var[0] == 's':
                my_var[0] = 'l'
                cv2.imwrite(os.environ.get('HOME') + "/Desktop/" + now.strftime("%d.%m.%Y-%H:%M:%S") + ".tif", frame)
                print("Image saved as " + os.environ.get('HOME') + "/Desktop/" + now.strftime("%d.%m.%Y-%H:%M:%S") + ".tif")
            if my_var[0] == 'v':
                my_var[0] = 'l'
                out = cv2.VideoWriter(os.environ.get('HOME') + "/Desktop/" + now.strftime("%d.%m.%Y-%H:%M:%S") + ".avi", fourcc, 20.0, (width, height))
                video = True
            if my_var[0] == 'p':
                my_var[0] = 'l'
                video = False
                print("Video saved as " + os.environ.get('HOME') + "/Desktop/" + now.strftime("%d.%m.%Y-%H:%M:%S") + ".avi")
            if video:
                out.write(frame)
        t.join()
        if out:
            out.release()
        cap.release()
        cv2.destroyAllWindows()
    except cv2.error as err:
        print(err, file=stderr)
        return 84


if __name__ == "__main__":
    if len(argv) != 2:
        print("USAGE:\n\t./astropi <file>", file=stderr)
        exit(84)
    main(argv[1])
