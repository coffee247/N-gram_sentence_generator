#!/usr/bin/env python3

'''

This program will allow a user to create any number of sentences constructed from
n-grams of any order from the any given corpus of text.
An n-gram is a sequence of N words.  The idea is to look at text as though examining
it through a window that can display only N words at a time, ... and while sliding
the window over the corpus of text, try to predict what the next word will be.

The problem can be solved in the following way:
1) clean the corpus of text using regex operations.
2) create list of sentences from the corpus of text.
3) add <start> and <end> tags to each sentence in the corpus.
4) Construct UnigramTable (a dictionary to hold raw frequencies of
each word in the entire corpus)
4b) If n is 1, do skip to unigram specific solution.
5) Construct NgramTable of raw frequencies (a nested dictionary containing n-grams in the outer dict
and a dictionary of raw frequencies of "next words" that follow the ngram.)
6) Construct n-gram relative frequency table (a nested dictionary  containing n-grams in the outer dict
and a dictionary of relative frequencies of "next words" that follow the ngram.)  Relative frequencies
being computed as ratio of ngramtable raw frequency over unigramtable raw frequency for each ngram.
7) Construct sentences by:
 7a) "sliding a window of length n-1" over the corpus of text and ...
 7b) predicting the next word by selecting a weighted random choice from the ngram Relative
    Frequency Table having ngram key that matches "windowed" text.
  7c) if next word is "<end>" mark sentence complete
  7c) if sentence not complete, Append word identifies in step 7b to current sentence
8) as sentences are completed, append to list of sentences.
9) display sentences.
10) terminate program

UNIGRAM specific solution:
5) Genrate M sentences by:
 5a) using unigram table, generate n sentences by appending random words from unigram table.
   Force construction of relatively short sentences by only appending random number of words.
   Append a random sentence terminator at the end of each sentence.
 5b) Display sentences
 5c) terminate program

******************************************************
actual examples of program input and output, along with usage instructions

GIVEN:
User wishes to generate 12 sentences from n-grams of length 4 occurring in texts found in
files called one.txt, two.txt, and three.txt

USER at command line:
     {(User will enter text after ~$ in command line as shown) Assumes terminal
     is open in same directory as ngram.py, one.txt, two.txt, and three.txt}
user@usersComputer:~$ python3 ngram.py 4 12 one.txt two.txt three.txt

******************************************************
Sample (toy) "test.txt":
This is a test of the emergency broadcast system.  This is only a test.
Had this been an actual emergency, you would have heard a siren!
There is no actual emergency, so no siren was sounded.  Please go about your business smartly!
Also, Don't ignore these tests, ... That would be dangerous!

Sample command line input:
python3 ngram.py 4 5 test.txt

Sample output: (plagiarises)
Had this been an actual emergency you would have heard a siren!
This is only a test.
Please go about your business smartly!
Please go about your business smartly!
Had this been an actual emergency you would have heard a siren!

Sample command line input:
python3 ngram.py 2 5 test.txt

Had this is no actual emergency broadcast system.
This is only a test of the emergency you would be dangerous!
This is a test.
This been an actual emergency you would have heard a siren!
Also don't ignore these tests that would be dangerous!




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
                    sentence = sentence.lstrip('<start> ')

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