#!/usr/bin/env python3

'''
James M. Stallings
Student ID V00859712

No stopwords
No smoothing
No non-contiguous ngrams

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
    filetext = filetext.lstrip()
    filetext = re.sub(r'[\[\]_]','',filetext.rstrip())  # remove [ and ] characters
    filetext = re.sub(r'\s+',' ',filetext)  # turn newlines into spaces
    filetext = re.sub(r'(\")','',filetext)  # remove double quotes
    filetext = re.sub(r'\.{2,}', '', filetext)  # remove multiple periods
    filetext = re.sub(r'(\-{2,})', ' ', filetext)  # remove multiple hyphens
    filetext = re.sub(r'(\s{2,})', ' ', filetext)  # remove multiple whitespace characters
    filetext = re.sub(r'[!] ', '!\n', filetext)  # add newline after exclamation
    filetext = re.sub(r'[.] ', '.\n', filetext)  # add newline after period
    filetext = re.sub(r'[?] ', '?\n', filetext)  # add newline after question mark
    filetext = filetext.split('\n')  # create new list from filetext split on newline.
    for line in filetext:
        print(line)


if __name__ == '__main__':
    main()
