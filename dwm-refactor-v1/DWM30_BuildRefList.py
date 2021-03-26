#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def buildRefList(logFile, tokenizedFileName):
    print('\n>>Starting DWM30')
    print('\n>>Starting DWM30', file=logFile)
    tokenizedFile = open(tokenizedFileName,'r')
    refList = []
    line = tokenizedFile.readline()
    while line != '':
        line = line.strip()
        firstBlank = line.find(' ')
        refID = line[0:firstBlank]
        body = line[firstBlank+1:]
        refList.append(('',refID,body))
        line = tokenizedFile.readline()
    tokenizedFile.close()
    print('Total References Read from ',tokenizedFileName,'=',len(refList))
    print('Total References Read from ',tokenizedFileName,'=',len(refList), file=logFile)
    return refList

