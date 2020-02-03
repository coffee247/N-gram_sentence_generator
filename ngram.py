#!/usr/bin/env python3

'''
James M. Stallings
Student ID V00859712

'''

import re
import sys
import logging

logging.basicConfig(filename='debug.log', level=logging.DEBUG)


def readfile(fileAtIndex):
    try:
        file = open(sys.argv[fileAtIndex], 'r')
        filetext = file.read()
        file.close()
        return filetext
    except:
        logging.info('Exception:  error loading file %s', sys.argv[fileAtIndex])
        print("{} \n\tException:  error loading file {}\n\tApplication will quit so you can try again!\n{}".format("*"*72, sys.argv[fileAtIndex], "*"*72))
        input("press ENTER key to continue quitting\n\n")
        print("Bye!\n\n")
        exit()



def main():
    filetext = ""
    n = sys.argv[1]
    m = sys.argv[2]

    print("\nThis program generates random sentences based on an Ngram model."
          "\nAuthored by: James M. Stallings\nVCU student ID: V00859712\n\n")
    print("Command line settings:  {} {} {}".format(sys.argv[0], n, m))

    for i in range(3, len(sys.argv), 1):
        filetext = "{} {}".format(filetext, readfile(i))
    filetext = re.compile(r'[?.!]\s+').split(filetext)
    print(filetext)


if __name__ == '__main__':
    main()
