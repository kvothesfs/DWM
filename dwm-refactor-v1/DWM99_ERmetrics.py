#!/usr/bin/env python
# coding: utf-8

# In[1]:


def generateMetrics(logFile, linkIndex, truthFileName):
    def countPairs(dict):
        totalPairs = 0
        for cnt in dict.values():
            pairs = cnt*(cnt-1)/2
            totalPairs +=pairs
        return totalPairs
    print('\n>>Starting DWM99')
    print('>>Starting DWM99', file=logFile)
    print('Truth File Name=', truthFileName)
    print('Truth File Name=', truthFileName, file=logFile)
    erDict = {}
    for pair in linkIndex:
        clusterID = pair[0]
        if clusterID != 'X':
            refID = pair[1]
            newPair = (clusterID,'x')
            erDict[refID] = newPair
    truthFile = open(truthFileName,'r')
    line = (truthFile.readline()).strip()
    line = (truthFile.readline()).strip()
    while line != '':
        part = line.split(',')
        recID = part[0].strip()
        truthID = part[1].strip()
        if recID in erDict:
            oldPair = erDict[recID]
            clusterID = oldPair[0]
            newPair = (clusterID, truthID)
            erDict[recID] = newPair
        line = (truthFile.readline()).strip()
    linkedPairs = {}
    equivPairs = {}
    truePos = {}
    for pair in erDict.values():
        clusterID = pair[0]
        truthID = pair[1]
        if pair in truePos:
            cnt = truePos[pair]
            cnt +=1
            truePos[pair] = cnt
        else:
            truePos[pair] = 1
        if clusterID in linkedPairs:
            cnt = linkedPairs[clusterID]
            cnt +=1
            linkedPairs[clusterID] = cnt
        else:
            linkedPairs[clusterID] = 1
        if truthID in equivPairs:
            cnt = equivPairs[truthID]
            cnt +=1
            equivPairs[truthID] = cnt
        else:
            equivPairs[truthID] = 1   
    # End of counts
    L = countPairs(linkedPairs)
    E = countPairs(equivPairs)
    TP = countPairs(truePos)
    print('L=',L,'E=',E, 'TP=', TP)
    FP = float(L-TP)
    FN = float(E-TP)
    precision = round(TP/float(L),4)
    recall = round(TP/float(E),4)
    fmeas = round((2*precision*recall)/(precision+recall),4)
    print('Precision=',precision)
    print('Precision=',precision, file=logFile)
    print('Recall=', recall)
    print('Recall=', recall, file=logFile)
    print('F-measure=', fmeas)
    print('F-measure=', fmeas, file=logFile)
    return

