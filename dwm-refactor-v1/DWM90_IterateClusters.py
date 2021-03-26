#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import DWM95_CalculateEntropy
def iterateClusters(logFile, epsilon, clusterList, refList, linkIndex):
    print('\n>>Starting DWM90')
    print('\n>>Starting DWM90', file=logFile)
    clusterCnt = 0
    goodClusterCnt = 0
    goodRefsCnt = 0
    # cluster is a list to store one cluster
    cluster = []
    clusterIndexList = []
    caboose = ('---','---')
    # Add caboose to signal end of list
    clusterList.append(caboose)
    # Iterate through cluster pairs, but not caboose
    for j in range(0,len(clusterList)-1):
        currentPair = clusterList[j]
        clusterID = currentPair[0]
        refID = currentPair[1]
        # Extract token string refBody from 3rd position of refList triple
        foundItem = list(filter(lambda x:refID in x, refList))
        ref = foundItem[0]
        clusterIndexList.append(refList.index(ref))
        refBody = ref[2]
        tokenList = refBody.split()
        # Append token string to cluster
        cluster.append(tokenList)
        nextPair = clusterList[j+1]
        currentCID = currentPair[0]
        nextCID = nextPair[0]
        # Look ahead to see if at end of cluster, if yes, process cluster
        if currentCID != nextCID:
            clusterCnt +=1
            entropy = DWM95_CalculateEntropy.calculateEntropy(epsilon, cluster)
            clusterIndexList.sort(reverse=True)
            if entropy <= epsilon:
                goodClusterCnt +=1
                goodRefsCnt +=len(clusterIndexList)
                for k in range(0,len(clusterIndexList)):
                    indexVal = clusterIndexList[k]
                    goodRef = refList[indexVal]
                    newTuple = (clusterID, goodRef[1])
                    linkIndex.append(newTuple)
                    del refList[indexVal]
            cluster.clear()
            clusterIndexList.clear()
    print('Total Clusters Processed =',clusterCnt)
    print('Total Clusters Processed =',clusterCnt, file=logFile)
    print('Total Good Clusters =',goodClusterCnt,' at epsilon =', epsilon)
    print('Total Good Clusters =',goodClusterCnt,' at epsilon =', epsilon, file=logFile)
    print('Total References in Good Cluster =', goodRefsCnt)
    print('Total References in Good Cluster =', goodRefsCnt, file=logFile)
    return

