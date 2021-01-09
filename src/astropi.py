#!/usr/bin/env python3
## EPITECH PROJECT, 2021
## Astropi
## File description:
## astropi
##

from sys import argv, stderr

def main(file):
    try:
        fd = open(file)
    except FileNotFoundError as err:
        print(err, file=stderr)
        return (84)

if __name__ == "__main__":
    if len(argv) != 2:
        print("USAGE:\n\t./astropi <file>", file=stderr)
        exit(84)
    main(argv[1])
