#!/usr/bin/python

import subprocess
from subprocess import call as sh
import os

"""
This code preprocesses texts up to, but not including, the point where they will be loaded into a database. That separation allows this to be run on multiple smaller instances if needed.

We start with files at, relative to the main presidio directory:

../texts/raw      The raw text files.  The files themselves should be named
                  'stringidentifier.txt' and the ids 'stringidentifier' should be
                  listed in a textids/ file.

../texts/textids  Any number of text files that each consist of a numeric and a 
                  stringidentifier (the numeric identifier is just an incrementing
                  integer guaranteed to be unique across the full dataset).  This
                  should be tab-delimited and should exclude the ".txt" extension.

Example creation of one such text file, run from ../texts/raw: (this would run better with "find" than "ls" in practice)

ls *.txt | awk -F '.txt' '{count++; print count "\t" $1;}' > ../textids/cat0001.txt

The easiest form of parallelization at the moment is just to shift around the 
number of files in each location at /texts/textfiles. This allows the use of multiple processors.
Adding more locations each with separate bookid files would allow easy multi-machine parallelization as well.

Currently this whole series takes a couple days on a large (8-core) machine with a million article-length documents and remote storage of files.
Disk access seems to be a major bottleneck, as does poor parallelization.

"""

#There are a whole bunch of directories that it wants to be there:
for directory in ['texts','logs','texts/cleaned','logs','logs/clean','texts/unigrams','logs/unigrams','logs/bigrams','texts/bigrams','texts/encoded','texts/encoded/unigrams','texts/encoded/bigrams','logs/encode2','logs/encode1', 'texts/wordlist']:
    if not os.path.exists("../" + directory):
        sh(['mkdir', '../' + directory])

def CopyDirectoryStructuresFromRawDirectory()
    print "Copying directory Structures from primary folder to later ones..."
    sh(["rsync", "-a --include '*/' --exclude '*'","../texts/raw/", "../texts/cleaned"])
    #Copy the later ones from cleaned to save time since "cleaned" will be empty, while "raw" will be full.
    for directory in ["unigrams","bigrams","encoded/unigrams","encoded/bigrams"]:
        sh(["rsync", "-a --include '*/' --exclude '*'","../texts/cleaned/", "../texts/" + directory])

"""Use the cleaning program to make texts that are set for tokenizing, and with sentences at linebreaks."""

def CleanTexts():
    print "Cleaning the texts"
    sh(['python','master.py','clean'])

def MakeUnigramCounts():
    print "Creating 1 gram counts"
    sh(['python','master.py','unigrams'])

def MakeBigramCounts():
    print "Creating 2gram counts"
    sh(['python','master.py','bigrams'])
    #We could add 3grams, and so forth, here.

def MakeTrigramCounts():
    print "Would be creating 3gram counts..."


#Just kidding, this isn't implemented

#These tend to be the most time-intensive scripts, since they involve a lot of dictionary lookups

def EncodeUnigrams():
    print "Creating 1grams encodings"
    sh(['python','master.py','encode1'])

def EncodeBigrams():
    print "Creating 2grams encodings"
    sh(['python','master.py','encode2'])
    
if __name__=="__main__":
    CopyDirectoryStructuresFromRawDirectory()

    CleanTexts()
    MakeUnigramCounts()
    MakeBigramCounts()
    MakeTrigramCounts()

    print "Creating a master wordlist"
    #The code in WordsTableCreate.py is the one that could be heavily optimized, and might be worth it.
    #Old version: sh(['python','WordsTableCreate.py'])
    from WordsTableCreate import WordsTableCreate
    #These values shouldn't be hard-coded in, probably:
    WordsTableCreate(maxDictionaryLength=1000000,maxMemoryStorage = 15000000)

    EncodeUnigrams()
    EncodeBigrams()
