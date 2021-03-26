#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from textdistance import DamerauLevenshtein
def setMu(value):
    global mu
    mu = value
    return
def normalized_similarity(ref1, ref2):
    #print(ref1,'***',ref2)
    Class = DamerauLevenshtein()
    score = 0.0  
    if len(ref1)==0 or len(ref2)==0:
        return score
    stillMore = True
    total = 0.0
    loops = 0
    while stillMore:
        len1 = len(ref1)
        len2 = len(ref2)
        maxVal = 0.0
        for j in range(0,len1):
            token1 = ref1[j]
            for k in range(0,len2):
                token2 = ref2[k]
                led = Class.normalized_similarity(token1,token2)
                if led >= maxVal:
                    maxVal = led 
                    saveJ = j
                    saveK = k
                if maxVal == 1.00:
                    break
        #end of nested loops
        loops +=1
        total = total + maxVal
        score = total/loops
        global mu
        if score < mu:
            return score
        ref1.pop(saveJ)
        ref2.pop(saveK)
        if (len(ref1)==0) or (len(ref2)==0):
            stillMore = False
    #end of while loop
    score = total/loops
    return score

