#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
import operator
from collections import OrderedDict


# In[2]:


#Tokenizer function for the Data Washing Machine
#Replace delimiter with blanks, then compress token by replacing non-word characters with null
def tokenizerCompress(string):
    string = string.upper()
    string = re.sub('[\,]+',' ',string)
    tokenList = re.split('[\s]+',string)
    newList = []
    for token in tokenList:
        newToken = re.sub('[\W]+','',token)
        if len(newToken)>0:
            newList.append(newToken)
    return newList


# In[3]:


#Tokenizer function for the Data Washing Machine
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


# In[4]:


def tokenizeCycle(inputSampleName, delimiter, hasHeader, removeDuplicateTokens, tokenizerType):
    inputFile= open(inputSampleName+'.txt','r')
    if tokenizerType=='Splitter':
        tokenizerFunction = tokenizerSplitter
    if tokenizerType=='Compress':
        tokenizerFunction = tokenizerCompress
#Phase 1, read input file, tokenize, wash tokens, and write to Sample-Tokenized.txt file
    washedFileName = inputSampleName+'-Tokenized.txt'
    washedFile = open(washedFileName,'w')
    print('Tokenizing References')
    refCnt = 0
    # skip header record
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
        outLine = refID
        for j in range(0,len(tokenList)):
            token= tokenList[j]
            outLine = outLine+' '+token
        outLine = outLine + '\n'
        washedFile.write(outLine)           
        line = inputFile.readline()
    inputFile.close()
    washedFile.close()
    print('Total References=',refCnt)
    print('Total Tokens Found =',tokenCnt)
    print('Total Tokens Output =', tokensOut)
    return


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




