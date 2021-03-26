#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
from textdistance import Cosine
from textdistance import MongeElkan
import DWM65_ScoringMatrix
def processBlock(comparator, mu, blockCount, block, compareCache):
    blockToken = block[0][0]
    validComparator = False
    if comparator == 'MongeElkan':
        Class = MongeElkan()
        validComparator = True
    if comparator == 'Cosine':
        Class = Cosine()
        validComparator = True
    if comparator == 'ScoringMatrix':
        Class = DWM65_ScoringMatrix
        DWM65_ScoringMatrix.setMu(mu)
        validComparator = True
    if not validComparator:
        print('**Error: Invalid Comparator Value in Parms File', comparator)
        sys.exit()
    blockLen = len(block)
    for j in range(0, blockLen-1):
        jTriple = block[j]
        jRecID = jTriple[1]
        for k in range(j+1, blockLen):
            kTriple = block[k]
            kRecID = kTriple[1]
            if jRecID > kRecID:
                key = kRecID+':'+jRecID
            else:
                key = jRecID+':'+kRecID
            if key not in compareCache:
                refJ = jTriple[2]
                refJList = refJ.split()
                refK = kTriple[2]
                refKList = refK.split()
                result = Class.normalized_similarity(refJList[:],refKList[:])
                #score = pythonMatrix(list1[:], list2[:])
                #print('comparing',jTriple[1],' to ', kTriple[1], 'result=', result)
                compareCache[key] = result
            #else:
                #print(key, ' already compared')
    return

