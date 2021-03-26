#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def generateProfile(linkIndex):
    print('\n>>Starting DWM97')
    profile = {}
    caboose = ('X','X')
    linkIndex.append(caboose)
    clusterSize = 0
    for j in range(0,len(linkIndex)-1):
        thisPair = linkIndex[j]
        thisCID = thisPair[0]
        nextPair = linkIndex[j+1]
        nextCID = nextPair[0]
        clusterSize +=1
        if thisCID != nextCID:
            if clusterSize not in profile:
                profile[clusterSize] = 1
            else:
                cnt = profile[clusterSize]
                cnt +=1
                profile[clusterSize] = cnt
            clusterSize = 0
    return profile

