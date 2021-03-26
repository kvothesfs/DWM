#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
import sys
def tokenizeInput(logFile, parms, tokenFreqDict, tokenizedFileName):
    #***********Inner Function*******************************
    #Replace delimiter with blanks, then compress token by replacing non-word characters with null
    def tokenizerCompress(string):
        string = string.upper()
        string = string.replace(delimiter,' ')
        tokenList = re.split('[\s]+',string)
        newList = []
        for token in tokenList:
            newToken = re.sub('[\W]+','',token)
            if len(newToken)>0:
                newList.append(newToken)
        return newList
    #***********Inner Function*******************************
    #Replace all non-words characters with blanks, then split on blanks
    def tokenizerSplitter(string):
        string = string.upper()
        string = re.sub('[\W]+',' ',string)
        tokenList = re.split('[\s]+',string)
        newList = []
        for token in tokenList:
            if len(token)>0:
                newList.append(token)
        return newList
    #***********Outer Main Function*******************************
    # Start of Main Tokenizer Function
    print('\n>> Starting DWM20')
    print('\n>> Starting DWM20', file=logFile)
    inputFileName = parms['inputFileName']
    print('Input Reference File Name =',inputFileName)
    print('Input Reference File Name =',inputFileName, file=logFile)
    hasHeader = parms['hasHeader']
    print('Input File has Header Records =', hasHeader)
    print('Input File has Header Records =', hasHeader, file=logFile)
    delimiter = parms['delimiter']
    print('Input File Delimiter =',delimiter)
    print('Input File Delimiter =',delimiter, file=logFile)
    tokenizerType = parms['tokenizerType']
    print('Tokenizer Function Type =',tokenizerType)
    print('Tokenizer Function Type =',tokenizerType, file=logFile)
    removeDuplicateTokens = parms['removeDuplicateTokens']
    print('Remove Duplicate Reference Tokens =',removeDuplicateTokens)
    print('Remove Duplicate Reference Tokens =',removeDuplicateTokens, file=logFile)
    print('Tokenized Reference Output File Name =',tokenizedFileName)
    print('Tokenized Reference Output File Name =',tokenizedFileName, file=logFile)
    goodType = False
    if tokenizerType=='Splitter':
        tokenizerFunction = tokenizerSplitter
        goodType = True
    if tokenizerType=='Compress':
        tokenizerFunction = tokenizerCompress
        goodType = True
    if goodType == False:
        print('**Error: Invalid Parameter value for tokenizerType ',tokenizerType)
        sys.exit()
    #Phase 1, read input file, tokenize, wash tokens, and write to Sample-Tokenized.txt file
    washedFile = open(tokenizedFileName,'w')
    inputFile= open(inputFileName,'r')
    refCnt = 0
    # skip header record
    print()
    if hasHeader:
        line = inputFile.readline()
    line = inputFile.readline()
    tokenCnt = 0
    tokensOut = 0
    while line !='':
        refCnt +=1
        line = line.strip()
        firstDelimiter = line.find(delimiter)
        refID = line[0:firstDelimiter]
        body = line[firstDelimiter+1:]
        tokenList = tokenizerFunction(body)
        tokenCnt = tokenCnt + len(tokenList)
        if removeDuplicateTokens:
            tokenList = list(dict.fromkeys(tokenList))
        tokensOut = tokensOut + len(tokenList)
        outLine = ''
        for j in range(0,len(tokenList)):
            token= tokenList[j]
            outLine = outLine+' '+token
            if token in tokenFreqDict:
                tokenFreqDict[token] +=1
            else:
                tokenFreqDict[token] = 1
        outLine = refID+outLine + '\n'
        washedFile.write(outLine)           
        line = inputFile.readline()
    inputFile.close()
    washedFile.close()
    print('Total References Read=',refCnt)
    print('Total References Read=',refCnt, file=logFile)
    print('Total Tokens Found =',tokenCnt)
    print('Total Tokens Found =',tokenCnt, file=logFile)
    print('Total Unique Tokens =', len(tokenFreqDict))
    print('Total Unique Tokens =', len(tokenFreqDict), file=logFile)
    return

