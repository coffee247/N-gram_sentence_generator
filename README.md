# N-gram_sentence_generator

This program will allow a user to create any number of sentences constructed from
n-grams of any order from the any given corpus of text.

An n-gram is a sequence of N words.  

The idea is to look at text as though examining

it through a window that can display only N words at a time, ... and while sliding

the window over the corpus of text, try to predict what the next word will be.

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

## Sample (toy) "test.txt":

This is a test of the emergency broadcast system.  This is only a test.
Had this been an actual emergency, you would have heard a siren!
There is no actual emergency, so no siren was sounded.  Please go about your business smartly!
Also, Don't ignore these tests, ... That would be dangerous!

### Sample command line input: (*with output following*)

      python3 ngram.py 4 5 test.txt

*Had this been an actual emergency you would have heard a siren!*

*This is only a test.*

*Please go about your business smartly!*

*Please go about your business smartly!*

*Had this been an actual emergency you would have heard a siren!*

### Sample command line input: (*with output following*)

      python3 ngram.py 2 5 test.txt
      
*Had this is no actual emergency broadcast system.*

*This is only a test of the emergency you would be dangerous!*

*This is a test.*

*This been an actual emergency you would have heard a siren!*

*Also don't ignore these tests that would be dangerous!*
