#/usr/bin/python

"""
This quickly creates a key-value store for textids: storing on disk
dramatically reduces memory consumption for bookworms of over 
1 million documents.
"""

import anydbm
import os

dbm = anydbm.open("files/texts/textids.dbm","c")

for file in os.listdir("files/texts/textids"):
    for line in open("files/texts/textids/" + file):        
        line = line.rstrip("\n")
        splat = line.split("\t")
        dbm[splat[1]] = splat[0]
