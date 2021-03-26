#!/usr/bin/env python
# coding: utf-8

# In[1]:


import DWM60_ProcessBlock
def iterateBlocks(logFile, comparator, mu, blockList):
    print('\n>>Starting DWM50')
    print('\n>>Starting DWM50', file=logFile)
    compareCache = {}
    block = []
    blockCount = 0
    blockList.append(('----','RID','BODY'))
    for j in range(len(blockList)-1):
        block.append(blockList[j])
        thisBlockToken = blockList[j][0]
        nextBlockToken = blockList[j+1][0]
        if thisBlockToken != nextBlockToken:
            blockCount +=1
            DWM60_ProcessBlock.processBlock(comparator, mu, blockCount, block, compareCache)
            block.clear()
    print('Total Blocks Processed =',blockCount)
    print('Total Blocks Processed =',blockCount, file=logFile)
    print('Total Pairs in Compare Cache =', len(compareCache))
    print('Total Pairs in Compare Cache =', len(compareCache), file=logFile)
    return compareCache

