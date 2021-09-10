# BloomFilter
Implementation of a Bloom Filter class as a project for the Data Structures college course. 
The __main() function provides an example of how the class works by reading 100,000 words from an external file (wordlist.txt downloaded from http://introcs.cs.princeton.edu/java/data/wordlist.txt) and inserting them in the Bloom Filter, then checking that all words inserted can be found. 

# What 
A Bloom Filter is a probabilistic data structure that can tell you with a specified false postive rate if a piece of information was inserted into the data structure. The searching algorithm of the class returns True if the key being searched MAY have been inserted into the Bloom filter and returns False if the key being searched has definitely not been inserted into the Bloom Filter. Elements can be added to the Bloom Filter, but can never be removed; the more items added, the larger the probability of false positives.

# Why 
This data structure is very efficient because the keys (containing the data) can be any size input, but all keys of all sizes consume the same (very small) number of bits.

# How 
The data structure starts off as a list of 0s. This class uses the program BitVector to create different Hash functions that will "hash" the keys to be inserted.
When a key is inserted into the Bloom Filter, it is hashed numHashes number of times, and the item at the corresponindng index in the list, is set to 1. There is a false positive rate because some keys might correspond to the same index after being hashed (so a key that was never inserted could still have its index in the list set to 1). 


# Methods 
- insert(key): inserts a key into the Bloom Filter, does not return anything because it always succeeds 
- find(key): Returns True if the key being searched MAY have been inserted into the Bloom Filter 
             Returns False if key being searched definitely hasn't been inserted into the Bloom Filter 
- falsePositiveRate(): Returns the projected current false positive rate based on the actual current number of bits actually set in this Bloom Filter
- numBitsSet():  Returns the current number of bits actually set in this Bloom Filter

