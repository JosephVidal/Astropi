#!/usr/bin/env python3
##
## EPITECH PROJECT, 2020
## Astropi
## File description:
## astropi
##

from sys import argv, stderr, exit

import cv2
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


def main(file):
    """Main function."""
    try:
        cap = cv2.VideoCapture()
        cap.open(file)
        while True:
            ret, frame = cap.read()
            if not ret:
                continue
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            msk = generate_mask(gray, 10)
            cv2.imshow('video', gray)
            cv2.imshow('mask', msk)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
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
