#!/usr/bin/env python3.9
##
## EPITECH PROJECT, 2020
## Astropi
## File description:
## astropi
##

from sys import argv, stderr, exit
from datetime import datetime

import cv2
import os
import numpy as np


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

def main(file):
    """Main function."""
    try:
        cap = cv2.VideoCapture()
        cap.open(file)
        video = False
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        while True:
            now = datetime.now()
            ret, frame = cap.read()
            key = cv2.waitKey(1) & 0xFF
            if key == ord('d'):
                cv2.imwrite(os.environ.get('HOME') + "/Desktop/" + now.strftime("%d.%m.%Y-%H:%M:%S") + ".tif", frame)
                print("Image saved as " + os.environ.get('HOME') + "/Desktop/" + now.strftime("%d.%m.%Y-%H:%M:%S") + ".tif")
            if not ret:
                continue
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            msk = generate_mask(gray, 10)
            start_point, end_point = detect_object(msk)
            frame = cv2.rectangle(frame, start_point, end_point, (0, 0, 255), 2)
            cv2.imshow('video', frame)
            cv2.imshow('mask', msk)
            if key == ord('q'):
                break
            if key == ord('s'):
                cv2.imwrite(os.environ.get('HOME') + "/Desktop/" + now.strftime("%d.%m.%Y-%H:%M:%S") + ".tif", frame)
                print("Image saved as " + os.environ.get('HOME') + "/Desktop/" + now.strftime("%d.%m.%Y-%H:%M:%S") + ".tif")
            if key == ord('v'):
                out = cv2.VideoWriter(os.environ.get('HOME') + "/Desktop/" + now.strftime("%d.%m.%Y-%H:%M:%S") + ".avi", fourcc, 20.0, (width, height))
                video = True
            if key == ord('p'):
                video = False
                print("Video saved as " + os.environ.get('HOME') + "/Desktop/" + now.strftime("%d.%m.%Y-%H:%M:%S") + ".avi")
            if video:
                out.write(frame)
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
