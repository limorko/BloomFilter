import math
from BitHash import BitHash
from BitVector import BitVector 

class BloomFilter(object):
    
    # Return the estimated number of bits needed in the Bloom Filter 
    # with the following 
    # parameters: numKeys: number of keys the Bloom Filter will store 
    #            numHashes: number of hash functions to be used 
    #            maxFalsePositive: false positive rate 
    # using the two equations (B, D)
    def __bitsNeeded(self, numKeys, numHashes, maxFalsePositive):
        
        #number of keys the Bloom Filter will store
        n = numKeys 
        #numHashes: number of hash functions to be used 
        d = numHashes
        #maxFalsePositive: false positive rate 
        P = maxFalsePositive 
        
        #equation B
        phi = (1 - (P ** (1/d)))
        
        #equation D
        N = d / (1 - (phi ** (1/n)))        
        
        #return how many bits the Bloom Filter will have to be 
        return round(N)
    
    # Create a Bloom Filter that will store numKeys keys, using 
    # numHashes hash functions, and that will have a false positive 
    # rate of maxFalsePositive.
    # All attributes must be private
    # #parameters: numKeys: number of keys the Bloom Filter will store 
    #              numHashes: number of hash functions to be used 
    #              maxFalsePositive: false positive rate 
    #
    def __init__(self, numKeys, numHashes, maxFalsePositive):
        
        #number of keys the Bloom Filter will store 
        self.__numKeys = numKeys
        #number of hash functions to be used 
        self.__numHashes = numHashes
        #false positive rate 
        self.__maxFalsePositive = maxFalsePositive
        
        #number of bits needed in the Bloom Filter is computed through the method __bitsNeeded
        self.__numBits = self.__bitsNeeded(numKeys, numHashes, maxFalsePositive)
        
        #creating the BitVector that will store the bits of the Bloom Filter 
        self.__BFArray = BitVector(size = self.__numBits)
        
        #to keep track of the number of bits that are set in the BF
        self.__numBitsSet = 0
     
    #inserting a key into the Bloom Filter
    #does not return anything, it always succeeds 
    def insert(self, key):
        
        #number of hash functions to be used
        d = self.__numHashes
        
        #tot number of bits in the BF
        N = self.__numBits
        
        #starting seed of the first BitHash function is 0 
        seed = 0
        
        #while we need to hash the key another time 
        while d:
            #invoke BitHash with the current seed 
            hash = BitHash(key, seed)
            
            #find the index where the bit will be set 
            index = hash % N 
            
            #if the bit at that index is not set already 
            if self.__BFArray[index] != 1:
                #set it to 1 
                self.__BFArray[index] = 1
                #increment the num of bits set in the Bloom Filter 
                self.__numBitsSet += 1
            
            #move on to the next seed 
            seed = hash
            #decrement the number of hashes still needed 
            d = d - 1
            
            
            
    # searching for a key inserted in the BF
    # Returns True if the key being searched MAY have been inserted into the BF
    # Returns False if key being searched definitely hasn't been inserted into the BF
    def find(self, key):
        
        #number of hash functions
        d = self.__numHashes
        
        #tot number of bits in the BF
        N = self.__numBits

        #starting seed of the first BitHash function is 0         
        seed = 0
        
        #while we need to hash the key another time
        while d:
            #invoke BitHash with the current seed 
            hash = BitHash(key, seed)
            
            #find the index where the bit would have been set 
            #if the key had already been inserted 
            index = hash % N 
            
            #if the bit at that index is not set, 
            #then the key was definitely not inserted, return False
            if self.__BFArray[index] != 1: return False
            
            #otherwise, move on to the next seed 
            seed = hash
            #decrement the number of hashes still needed 
            d = d - 1        
        
        #all the bits that correspond to the key were set, then the key MAY 
        #have been inserted in the BF, return True
        return True 
       
    
    # Returns the PROJECTED current false positive rate based on the
    # ACTUAL current number of bits actually set in this Bloom Filter
    def falsePositiveRate(self):
        
        #number of hash functions 
        d = self.__numHashes
        #tot number of bits in the BF
        N = self.__numBits
        #current number of bits set in the BF
        n = self.__numBitsSet
        
        #computing the actual measured current proportion of bits 
        #in the bit vector that are still zero
        phi = ( N - n ) / N
        
        #computing the false positive rate 
        P = (1 - phi) ** d
        
        #return the false positive rate 
        return P  
       
    # Returns the current number of bits actually set in this Bloom Filter
    def numBitsSet(self):
        # returning the attribute that keeps track of the bits already set in the BF
        return self.__numBitsSet


       

def __main():
 
    
    # create the Bloom Filter
    # 100,000 keys to be inserted, 4 hash functions, a maximum false pos. rate of 5%
    numKeys = 100000
    numHashes = 4
    maxFalse = .05  
    b = BloomFilter( numKeys, numHashes, maxFalse)    
    
    # read the first numKeys words from the file and insert them 
    # into the Bloom Filter. 
    fin = open("wordlist.txt")
    
    # keep track of how many keys have been inseted already 
    count = 0 
    
    # read the line 
    line = fin.readline()
    
    # while the num of keys inserted is < numKeys
    while count < numKeys:
        
        # insert the current line being read 
        b.insert(line)
        # increment num of keys inserted 
        count += 1
        # read the next line
        line = fin.readline()
        
    # close the input file
    fin.close()
        

    # Print out what the PROJECTED false positive using the falsePositiveRate method.
    print("Projected false positive rate: ", b.falsePositiveRate())
    
    
    # re-open the file
    fin = open("wordlist.txt")
    
    # keep track of how many keys have been checked already (stop at 100,000)
    count = 0 
    
    # keep track of the num of words that have been inserted but can't be found in the BF
    wordsMissing = 0
    
    # read the line 
    line = fin.readline()
    
    # while we haven't checked for the first 100,000 keys 
    while count < numKeys:
        # if  the current line is not found in the BF, increment words missing
        if b.find(line) == False: wordsMissing += 1
        # increment num of keys checked 
        count += 1
        # move on to next line 
        line = fin.readline()
        
    # print the num of words missing (must be 0) 
    print("words missing", wordsMissing)
    
    
    # Read the next numKeys words from the file (none inserted in the BF)
    # count how many of the words can be (falsely) found in the Bloom Filter
    
    # keep track of how many keys have been checked already (stop at 100,000)
    count = 0 
    
    # keep track of the num of words that have been found but never inserted in the BF
    falselyFound = 0
    
    # read the line 
    line = fin.readline()
    

    # while we haven't checked for the second 100,000 keys    
    while count < numKeys:
        
        # if the key is found in the BF, increment falsely found by 1
        if b.find(line) == True: falselyFound += 1
        
        # incremnet num of keys checked 
        count += 1
        
        # read the next line of the file 
        line = fin.readline()
        
    #print how many words were found but never inserted in the BF 
    print("words falsely found", falselyFound)
        
    # Print out the percentage rate of false positives
    # num of falsely inserted keys found / num of keys to be inserted in the BF
    falsePositiveRate = falselyFound/numKeys
    print("actual false positive rate", falsePositiveRate)
 

    
if __name__ == '__main__':
    __main()       

