#!/usr/bin/env python3

'''
James M. Stallings
Student ID V00859712

TODO try this REGEX --> ([\S]+?[[\S\s]+?(?:[\.?!]))
    https://regex101.com/r/4HlcNd/1

'''

import re
import sys
import logging
import random
from _collections import defaultdict

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

def makeUnigramTable(str, counts):
    words = str.split()
    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    return counts

def getwordCount(str):
    count = 0
    words = str.split()
    for word in words:
            count += 1
    return count - 1

def cleanText(filetext):
    filetext = filetext.lstrip()
    filetext = filetext.lower()
    filetext = re.sub(r'[\[\]\(\):,_]', '', filetext)  # remove colon, comma, [ and ] characters,
    filetext = re.sub(r'[\"\”\“\*\‘]', '', filetext)  # remove quote marks and *
    filetext = re.sub(r'(\’\s)', ' ', filetext)
    filetext = re.sub(r'(\n)', ' ', filetext)  # turn newlines into spaces
    filetext = re.sub(r'(\s{2,})', ' ', filetext)  # remove multiple whitespace characters
    filetext = re.sub(r'(\.{2,})', ' ', filetext)  # remove multiple periods
    filetext = re.sub(r'(\-{2,})', ' ', filetext)  # remove multiple hyphens
    filetext = re.sub(r'(\s{2,})', ' ', filetext)  # remove multiple whitespace characters
    filetext = re.sub(r'[!] ', ' !\n', filetext)  # add newline after exclamation
    filetext = re.sub(r'[.] ', ' .\n', filetext)  # add newline after period
    filetext = re.sub(r'[?] ', ' ?\n', filetext)  # add newline after question mark
    return filetext

def makeCodedSentences(filetext, n):
    n = n-1
    start = '<start> '
    end = ' <end>'
    newList = []
    for line in filetext:
        sentence = str(line)
        if (getwordCount(sentence) >= n):
            sentence = "{}{}{}".format(n*start, sentence, end)
            newList.append(sentence)
    return newList

def makeNgramTable(filetext, n, lookupTable):

    for line in filetext:
        words = line.split(' ')
        for j in range(len(words)-n):
            ngram = ""
            k = j + n-1
            for l in range(j, k, 1):
                ngram = (ngram + ' ' + words[l]).lstrip()
                if (len(ngram.split(' ')) == (n-1)):
                    try:
                        count = lookupTable[ngram][words[l+1]]
                        lookupTable[ngram][words[l + 1]] = count + 1
                    except:
                        count = 0
            lookupTable[ngram][words[l + 1]] = count + 1

def makeRelFreqTable(unigramTable, nGramTable, relFreqTable):
    for ngramKey in nGramTable:
        unigramKey = nGramTable[ngramKey]
        for val in list(unigramKey):
            if val is not '':
                numerator = nGramTable[ngramKey][val]
                denominator = unigramTable[val]
                relFreqTable[ngramKey][val] = round(numerator/denominator, 4)



def getUnigramRawFreq(unigram_table, instr):
    returnString = unigram_table[instr]
    return int(returnString)

def getNgramRawFreq(nGramTable, instr):
    returnString = nGramTable[instr]
    return int(returnString)


def main():
    filetext = ""
    start = '<start> '
    end = ' <end>'
    n = int(sys.argv[1])
    m = int(sys.argv[2])
    firstwords = []
    lookupTable = defaultdict(dict)
    counts = dict()
    relFreqTable = defaultdict(dict)


    print("\nThis program generates random sentences based on an Ngram model."
          "\nAuthored by: James M. Stallings\nVCU student ID: V00859712\n\n")
    print("Command line settings:  {} {} {}".format(sys.argv[0], n, m))

    for i in range(3, len(sys.argv), 1):  # for each input file ...

        '''read the file into memory as a string object & append to filetext '''
        filetext = "{} {}".format(filetext, readfile(i))

    ''' prepare the text for processing '''
    filetext = cleanText(filetext)



    filetext = filetext.split('\n')  # create new list from filetext split on newline.
    filetext = makeCodedSentences(filetext, int(n))
    for line in filetext:
        ''' produce a Unigram table of raw frequencies '''
        unigram_table = makeUnigramTable(line, counts)




    makeNgramTable(filetext, n, lookupTable)
    makeRelFreqTable(unigram_table, lookupTable, relFreqTable)
    startkey = "{}".format((n-1)*start).lstrip().rstrip()
    startword = random.choice(list(lookupTable[startkey]))
    for x in range(m):
        words = []
        weights = []
        for wordToWeight in (list(lookupTable[startkey])):
            words.append(wordToWeight)
            weights.append(relFreqTable[startkey][wordToWeight])
        nextWord = random.choices(words, weights)
        print(nextWord[0])

if __name__ == '__main__':
    main()
