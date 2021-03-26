#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def transitiveClosure(logFile, pairList):
    # Bootstap process by add reverse of all pairs to the pairList
    print('\n>>Starting DWM80')
    print('\n>>Starting DWM80', file=logFile)
    iterationCnt = 0
    clusterList = []
    for pair in pairList:
        clusterList.append(pair)
        pairRev = (pair[1],pair[0])
        clusterList.append(pairRev)
        pairSelf = (pair[0],pair[0])
        clusterList.append(pairSelf)
    pairList = []
    for pr in clusterList:
        if pr not in pairList:
            pairList.append(pr)
    # Sort pairs in order by the first position (the key)
    pairList.sort()
    #print('***sorted pairList size =', len(pairList))
    #print('***sorted pairList =', pairList)
    # All of the pairs with same key are a Key Group
    clusterList = []
    moreWorkToDo = True
    iteration = 0
    while moreWorkToDo:
        moreWorkToDo = False
        iteration +=1
        # Add a caboose record to the end of the pairList
        caboose = ('---','---')
        pairList.append(caboose)
        keyGroup = []
        for j in range(0,len(pairList)-1):
            currentPair = pairList[j]
            keyGroup.append(currentPair)
            # Look ahead to the next key
            nextPair = pairList[j+1]
            currentKey = currentPair[0]
            nextKey = nextPair[0]
            # When next key is different, at end of Key Group and ready to process keyGroup
            if currentKey != nextKey:
                firstGroupPair = keyGroup[0]
                firstGroupPairKey = firstGroupPair[0]
                firstGroupPairValue = firstGroupPair[1]
                # Add new pairs to clusterList from key groups starting with reversed pair and larger than 1 pair
                keyGroupSize = len(keyGroup)
                if firstGroupPairKey > firstGroupPairValue:
                    if keyGroupSize>1:
                        moreWorkToDo = True
                        for k in range(keyGroupSize):
                            groupPair = keyGroup[k]
                            groupPairValue = groupPair[1]
                            newPair = (firstGroupPairValue, groupPairValue)
                            clusterList.append(newPair)
                            newReversePair = (groupPairValue, firstGroupPairValue)
                            clusterList.append(newReversePair)
                        # Decide if first pair of keyGroup should move over to clusterList
                        lastGroupPair = keyGroup[keyGroupSize-1]
                        lastGroupPairValue = lastGroupPair[1]
                        if firstGroupPairKey < lastGroupPairValue:
                            clusterList.append(firstGroupPair)   
                else:
                    # pass other key groups forward to cluster list
                    clusterList.extend(keyGroup)
                keyGroup = []
        pairList = []
        for pr in clusterList:
            if pr not in pairList:
                pairList.append(pr)
        pairList.sort()
        iterationCnt +=1
        clusterList = []
    print('Total Closure Iterations =',iterationCnt)
    print('Total Closure Iterations =',iterationCnt, file=logFile)
    return pairList

