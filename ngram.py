#!/usr/bin/env python3

'''

James M. Stallings
Student ID V00859712

'''

import re
import sys
import random
from _collections import defaultdict

startkey = ""
start = '<start> '
end = ' <end>'
tokenCount = 0


def readfile(fileAtIndex):
    try:
        file = open(sys.argv[fileAtIndex], 'r')
        filetext = file.read()
        file.close()
        return filetext
    except:
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
    filetext = re.sub(r'[\[\]\(\):;,_—]', '', filetext)  # remove colon, comma, [ and ] characters,
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
    filetext = re.sub(r'(\﻿) ', '', filetext)  # remove UTF-8 NULL character
    return filetext

def makeCodedSentences(filetext, n):
    newList = []
    for line in filetext:
        sentence = str(line)
        if (getwordCount(sentence) >= n-1):
            sentence = "{}{}{}".format(n*start, sentence, end)
            newList.append(sentence)
    return newList

def makeNgramTable(filetext, n, lookupTable):
    count = 0
    for line in filetext:  # for each line in the corpus
        words = line.split(' ')  # break the line into individual words
        for j in range(len(words)-n):  # for each word in a line
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

def listToString(alist):
    # initialize an empty string
    str1 = " "
    # return string
    return (str1.join(alist))

def moveNgramWindow(loopkey, nextWordString, n):
    loopkey = loopkey + ' ' + nextWordString
    alpha = loopkey.split(' ')
    length = len(alpha)
    alpha = alpha[length - (n):length]
    loopkey = listToString(alpha)
    return loopkey

def printIntroData(n, m):
    print("\nThis program generates random sentences based on an Ngram model."
          "\n\nAuthored by: James M. Stallings\nVCU student ID: V00859712\n")
    print("Command line settings:  {} {} {}\n".format(sys.argv[0], n, m))

def openAndReadInputFiles():
    filetext = ""
    for i in range(3, len(sys.argv), 1):  # for each input file ...
        '''read the file into memory as a string object & append to filetext '''
        filetext = "{} {}".format(filetext, readfile(i))
    return filetext


def main():
    start = '<start> '
    n = int(sys.argv[1])
    m = int(sys.argv[2])
    ngramTable = defaultdict(dict)
    counts = dict()
    relFreqTable = defaultdict(dict)

    ''' display required intro data '''
    printIntroData(n, m)

    ''' read files from disk '''
    filetext = openAndReadInputFiles()

    ''' prepare the text for processing '''
    filetext = cleanText(filetext)  # regex operations
    filetext = filetext.split('\n')  # create list of sentences from filetext.
    filetext = makeCodedSentences(filetext, int(n))  #  add <start> and <end> tags

    ''' construct the unigram raw frequency table '''
    for line in filetext:
        unigram_table = makeUnigramTable(line, counts)

    if n > 1:

        ''' construct the n-gram raw frequency table'''
        makeNgramTable(filetext, n, ngramTable)

        ''' construct the n-gram relative frequency table '''
        makeRelFreqTable(unigram_table, ngramTable, relFreqTable)

        ''' Make m sentences'''
        for x in range(m):  # for each sentence

            atend = False

            ''' construct the startkey    (in the form <start> <start> .... <start>) having n-1 <start> tags '''
            startkey = "{}".format((n - 1) * start).lstrip().rstrip()

            ''' pick a startword at random from first words in filetext sentences '''
            startword = random.choice(list(ngramTable[startkey]))
            sentence = startword

            ''' revise the startkey with startword '''
            startkey = moveNgramWindow(startkey, startword, n - 1)

            ''' build sentence until end detected '''
            while not atend:
                words = []
                weights = []

                ''' construct matching word and weight lists for current key '''
                for ngramWordsFromKey in (list(ngramTable[startkey])):
                    if not ngramWordsFromKey == '':
                        words.append(ngramWordsFromKey)
                        weights.append(relFreqTable[startkey][ngramWordsFromKey])

                ''' 
                build a sentence by selecting weighted random word from words list and adding it to sentence.
                in the except block (catches end of sentence), append sentence to sentences list
                '''
                try:
                    nextWordString = listToString(random.choices(words, weights=weights))
                    sentence = sentence + ' ' + nextWordString  # add next word to sentence

                    ''' 
                    revise startkey by appending nextWordString and trimming
                    words from the left until only n-1 words remain.
                    '''
                    startkey = moveNgramWindow(startkey, nextWordString, n - 1)
                except:
                    atend = True  # end of sentence was detected
            sentence = re.sub(r'( \.)', '.', sentence)  # move puctuation to left one space
            sentence = re.sub(r'( \!)', '!', sentence)  # move puctuation to left one space
            sentence = re.sub(r'( \?)', '?', sentence)  # move puctuation to left one space
            print("{}".format(sentence.capitalize()))  # Display the sentence
        print("\n")
    else:
        '''
        deal with unigrams by creating random length sentences from random 
        words found in corpus.
        '''
        sentences = []
        for sentenceCount in range(m):
            count = 0
            sentence = ""
            lim = random.randint(1, 15)
            while count <= lim:
                word = random.choice(((list(unigram_table))))
                if word not in ['<start>','<end>','.','!','?']:
                    sentence = sentence + ' ' + word
                    count = count + 1
            sentence = str(sentence + random.choice(['.','!','?'])).lstrip()  # add random punctuation at sentence end.
            sentence = ("{}".format(sentence.capitalize()))  # capitalize first letter
            sentences.append(sentence)  # add sentence to list of sentences
        for i in range(m):  # we are making m sentences (m is the number of sentences tpo make)
            print(sentences[i])  # dsiplay the sentences
        print("")  # display a blank line before exiting.


if __name__ == '__main__':
    main()