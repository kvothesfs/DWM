#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def buildBlocks(logFile, refList, parms, tokenFreqDict):
    print('\n>>Starting DWM40')
    print('\n>>Starting DWM40', file=logFile)
    blockList = []
    stopCnt = 0
    beta = parms['beta']
    print('beta =',beta)
    print('beta =',beta, file=logFile)
    sigma = parms['sigma']
    print('sigma =',sigma)
    print('sigma =',sigma, file=logFile)
    for triple in refList:
        refID = triple[1]
        body = triple[2]
        tokenList = body.split(' ')
        skinnyBody = ''
        blockTokenList = []
        for token in tokenList:
            freq = tokenFreqDict[token]
            if freq <= sigma:
                skinnyBody = skinnyBody + ' ' + token
            else:
                stopCnt +=1
            if freq > 1 and freq <= beta:
                blockTokenList.append(token)
        if len(skinnyBody) > 0 and len(blockTokenList) > 0:
            for token in blockTokenList:
                blockList.append((token,refID,skinnyBody))
    print('Stop Words excluded=',stopCnt)
    print('Stop Words excluded=',stopCnt, file=logFile)
    print('Total Blocking Records Created', len(blockList))
    print('Total Blocking Records Created', len(blockList), file=logFile)
    return blockList

