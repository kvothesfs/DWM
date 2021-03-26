#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import re
import subprocess
import operator
from collections import OrderedDict
from textdistance import Levenshtein
import json


# In[ ]:


def globalReplace(logFile, sampleName, minFreqStdToken, minLenStdToken, maxFreqErrToken):
    print ("\n>>Starting DWM25 --- runReplacement is set to True, starting global token replacement")
    print("\n>>Starting DWM25 --- runReplacement is set to True, starting global token replacement", file=logFile)
    Class = Levenshtein()
    NewDict = json.load(open("NewDict.txt"))
    print("Dictionary Load =", len(NewDict))
    print(type(NewDict))
#Phase 1: Build token dictionary from tokenized file
    tokenizedFileName = sampleName+'-Tokenized.txt'
    tokenizedFile = open(tokenizedFileName,'r')
    print('Global Replace Cycle')
    print('Global Replace Cycle', file=logFile)
    index ={}
    refCnt = 0
    tokenCnt = 0
    line = tokenizedFile.readline()
    while line !='':
        refCnt +=1
        line = line.strip()
        tokenList = re.split('\s+', line)
        refID = tokenList[0]
        for j in range(1,len(tokenList)):
            token= tokenList[j]
            tokenCnt +=1
            if token!='':
                if token not in index:
                    index[token]=1
                else:
                    count = index.get(token)
                    count = count + 1
                    index[token]=count      
        line = tokenizedFile.readline()
    tokenizedFile.close()
    print('Total References=',refCnt)
    print('Total Tokens=',tokenCnt)
    print('Unique Tokens=',len(index))
    print("Minimum Frequency of Standard Token = ", minFreqStdToken)
    print("Minimum Length of Standard Token = ", minLenStdToken)
    print("Maximum Frequency of Error Token = ", maxFreqErrToken)
    print('Total References=',refCnt, file=logFile)
    print('Total Tokens=',tokenCnt, file=logFile)
    print('Unique Tokens=',len(index), file=logFile)
    print("Minimum Frequency of Standard Token = ", minFreqStdToken, file=logFile)
    print("Minimum Length of Standard Token = ", minLenStdToken, file=logFile)
    print("Maximum Frequency of Error Token = ", maxFreqErrToken, file=logFile)
#Phase 2, build list of token-frequency pairs and sort descending by token frequency
    print('References Processed=',refCnt)
    print('References Processed=',refCnt, file=logFile)
    sortedIndex = sorted(index.items(),reverse=True, key=operator.itemgetter(1))
    tokenCnt = len(sortedIndex)
    print("Sorted Token Size =", tokenCnt)
    print("Sorted Token Size =", tokenCnt, file=logFile)
    cleanIndex = []
    for j in range(0,tokenCnt):
        pairJ = sortedIndex[j]
        wordJ = pairJ[0]
        lenJ = len(wordJ)
        freqJ = pairJ[1]
        if lenJ<minLenStdToken:
            continue
        if not wordJ.isalpha():
            continue
        cleanIndex.append(pairJ)
    cleanCnt = len(cleanIndex)
    print("Clean Token Size =", cleanCnt)
    print("Clean Token Size =", cleanCnt, file=logFile)
#Phase 3 Build Dictionary (stdToken) of token corrections
    stdToken = {}
    checkCnt = 0
    changeTable = open('Token_Substitution_Table.txt','w')
    for j in range(0,cleanCnt-1):
        pairJ = cleanIndex[j]
        wordJ = pairJ[0]
        lenJ = len(wordJ)
        freqJ = pairJ[1]
        if freqJ < minFreqStdToken:
            print("*Stop Replacements here")
            print("*Stop Replacements here", file=logFile)
            break
        for k in range(cleanCnt-1, 1, -1):
            pairK = cleanIndex[k]
            wordK = pairK[0]
            lenK = len(wordK)
            freqK = pairK[1]
            if k == j+1:
                break
            if Class.distance(wordJ,wordK)==1 and freqK<=maxFreqErrToken and not (wordK.lower() in NewDict):
                stdToken[wordK] = wordJ
                string = wordJ+'\t'+str(freqJ)+'\t'+wordK+'\t'+str(freqK)
                changeTable.write(string+'\n')
                cleanIndex[k] = ('',freqK)
                checkCnt = checkCnt + freqK
    replacementPairs = len(stdToken)
    changeTable.close
#Phase 4, re-read washed file and replace tokens in the stdToken dictionary, write to CleanedFile
    tokenizedFile = open(tokenizedFileName, 'r')
    tokenReplaceFileName = sampleName+'-TokenReplace.txt'
    tokenReplaceFile = open(tokenReplaceFileName,'w')
    changeCnt = 0
    tokenCnt = 0
    line = tokenizedFile.readline()
    refCnt = 0
    refsChanged = 0
    while line !='':
        refCnt +=1
        line = line.strip()
        tokenList = re.split('\s+', line)
        refID = tokenList[0]
        outLine = refID
        change = False
        for j in range(1,len(tokenList)):
            token= tokenList[j]
            tokenCnt +=1
            if token in stdToken:
                change = True
                oldToken = token
                token = stdToken[oldToken]
                changeCnt +=1
                #print(refID, oldToken,token)
            outLine = outLine + ' '+token
        if change:
            refsChanged +=1
        outLine = outLine + '\n'
        tokenReplaceFile.write(outLine)           
        line = tokenizedFile.readline()
    tokenizedFile.close()
    tokenReplaceFile.close()
    print("References Processed = ", refCnt)
    print("Total Replacement Pairs =",replacementPairs)
    print("Tokens Read =",tokenCnt)
    print("Tokens Changed = ",changeCnt)
    print("References Changed =",refsChanged)
    print("References Processed = ", refCnt, file=logFile)
    print("Total Replacement Pairs =",replacementPairs, file=logFile)
    print("Tokens Read =",tokenCnt, file=logFile)
    print("Tokens Changed = ",changeCnt, file=logFile)
    print("References Changed =",refsChanged, file=logFile)
    return

