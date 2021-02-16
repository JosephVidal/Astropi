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
    bolean = False
    breaker = False
    for i in range(len(msk)):
        for x in range(len(msk[i])):
            if msk[i][x] != 0 and bolean == False:
                minx = x
                miny = i
                bolean = True
            if msk[i][x] > 0 and bolean == True:
                maxx = x
                maxy = i
                breaker = True
                break
        if breaker == True:
            break
    start_point = (minx, miny)
    end_point = (minx + 10, miny + 10)
    return start_point, end_point

def main(file):
    """Main function."""
    try:
        cap = cv2.VideoCapture()
        cap.open(file)
        while True:
            now = datetime.now()
            ret, frame = cap.read()
            if not ret:
                continue
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            msk = generate_mask(gray, 10)
            start_point, end_point = detect_object(msk)
            gray = cv2.rectangle(gray, start_point, end_point, (255, 0, 0), 2)
            cv2.imshow('video', frame)
            cv2.imshow('mask', msk)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            if key == ord('s'):
                cv2.imwrite(os.environ.get('HOME') + "/Desktop/" + now.strftime("%d.%m.%Y-%H:%M:%S") + ".tif", frame)
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
