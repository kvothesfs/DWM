#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
import os
import subprocess
import math
from collections import OrderedDict
import datetime
import time
from datetime import date
from textdistance import Levenshtein
from textdistance import DamerauLevenshtein
index = {}
sigma = 0
beta = 0
ERtype=''
mu = 0.0
muIterate = 0.0
clusterProfile ={}
erMetricsPrefix = ''
runClusterMetrics = False
epsilon = 0.0
epsilonIncrement= 0.0


# In[2]:


def sortFirst(val):
    return val[0]

def sortSecond(val): 
    return val[1]

def passTableToJava(fileName):
    start6 = time.perf_counter()
    print("Running NewMatrix Jar!")    
    subprocess.run(["java", "-jar", "RunNewMatrix.jar", str(mu), fileName,str(beta),str(sigma)], text=True)
    inputClusterInput = open('BlockNumbers.txt', 'r')
    newSingleBlockNbr = inputClusterInput.readline()
    newBlockNumber = inputClusterInput.readline()
    inputClusterInput.close()
    runStatistics.write('    Single-Reference Blocks = '+str(newSingleBlockNbr.rstrip())+'\n')
    print(" Single-Reference Blocks = " + newSingleBlockNbr)
    print(" Multi-Reference Blocks = " + newBlockNumber)
    runStatistics.write('    Multi-Reference Blocks = '+str(newBlockNumber)+'\n')
    end6 = time.perf_counter()
    totalTime6 = end6 - start6
    print('NewMatrix Iterateblocks Total Time = '+str(totalTime6)+'\n')

    return


# In[3]:


def buildLinkFile():
    global clusterProfile
    origInput = open(sourceFileName, 'r')
    goodClusterInput = open('GoodClusters.txt', 'r')
    List1 = []
    rec = origInput.readline()
    cnt1 = 0
    #rec = origInput.readline()
    while rec!='':
        cnt1 +=1
        rec = rec.strip()
        firstBlank = rec.find(' ')
        part0 = rec[0:firstBlank]
        List1.append(part0)
        rec = origInput.readline()
    List1.sort()
    origInput.close()

    List2 = []
    rec = goodClusterInput.readline()
    cnt2 = 0
    while rec!='':
        cnt2 +=1
        rec = rec.strip()
        parts = re.split(' ',rec)
        List2.append((parts[0],parts[1]))
        rec = goodClusterInput.readline()
    List2.sort(key=sortFirst)
    goodClusterInput.close()
    #################################################################
    joinFinalCluster = open('ResultsLinkFile.txt', 'w')
    moreRecs = True
    index1 = 0
    index2 = 0
    cnt3 = 0
    while moreRecs:
        if index2 >= len(List2):
            for j in range (index1,len(List1)):
                RefID1 = List1[j]
                joinFinalCluster.write(RefID1+','+RefID1+'\n')
                cnt3 +=1
            moreRecs = False 
            break 
        if index1 >= len(List1):
            for j in range (index2,len(List2)):
                pair = List2[index2]
                RefID2 = pair[0]
                LinkID2 = pair[1]
                joinFinalCluster.write(RefID2+','+LinkID2+'\n')
                cnt3 +=1
            moreRecs = False
            break 
        RefID1 = List1[index1]
        pair = List2[index2]
        RefID2 = pair[0]
        LinkID2 = pair[1]
        if RefID1==RefID2:
            joinFinalCluster.write(RefID2+','+LinkID2+'\n')
            cnt3 +=1
            index1 += 1
            index2 += 1
        if RefID1 < RefID2:
            joinFinalCluster.write(RefID1+','+RefID1+'\n')
            cnt3 +=1
            index1 += 1 
        if RefID1 > RefID2:
            joinFinalCluster.write(RefID2+','+LinkID2+'\n')
            cnt3 +=1
            index2 += 1      
    joinFinalCluster.close()
    runStatistics.write('Final Join Counts\n')
    runStatistics.write('Source Ref Count = '+str(cnt1)+'\n')
    runStatistics.write('Good Cluster Ref Count = '+str(cnt2)+'\n')
    runStatistics.write('Final Output Ref Count = '+str(cnt3)+'\n')
    lostRefs = cnt1 - cnt2
    if 1 in clusterProfile:
        count = clusterProfile[1]
        count = count + lostRefs
        clusterProfile[1] = count
    else:
        clusterProfile[1] = lostRefs
    return


# In[4]:


def joinFiles(linkFileName, outFileName, refIDFirst):
    origInput = open(sourceFileName, 'r')
    closureInput = open(linkFileName, 'r')
    dic = {}
    rec = origInput.readline()
    rec = rec.strip()
    while rec!='':
        pos = rec.find(' ')
        part1 = rec[0:pos]
        part2 = rec[pos+1:]
        if(len(part2) > 0):             
            dic[part1] = part2
        rec = origInput.readline()
        rec = rec.strip()
    origInput.close()
    runStatistics.write('>Join Operation: Recs from Source '+str(len(dic))+'\n')

    cList = []
    rec = closureInput.readline()
    rec = rec.strip()
    while rec!='':
        parts = re.split(',',rec)
        if refIDFirst:
            clusterID = parts[1]
            refID = parts[0]
        else:
            clusterID = parts[0]
            refID = parts[1]
        cList.append((clusterID,refID))
        rec = closureInput.readline()
        rec = rec.strip()
    cList.sort(key=sortFirst)
    closureInput.close()
    runStatistics.write('>Join Operation: Recs from Closure Output '+str(len(cList))+'\n')
    #################################################################
    clusterOutput = open(outFileName, 'w')
    for pair in cList:
        clusterID = pair[0]
        refID = pair[1]
        if refID in dic.keys():   
            body = dic[refID]
            clusterOutput.write(refID+':'+clusterID+':'+body+'\n')
    clusterOutput.close()
    runStatistics.write('>Join Operation: Refs written to ClusterOutput '+str(len(cList))+'\n')
    #print('Join Operation: Refs written to ClusterOutput '+str(len(cList)))
    return


# In[5]:


def run_ERMetics_Final():
    global erMetricsPrefix
    erMetricsProperties = erMetricsPrefix + 'final.properties'
    subprocess.run(["java", "-jar", "er-metrics.jar", erMetricsProperties], text=True)
    p = subprocess.Popen(['java', '-jar', 'er-metrics.jar', erMetricsProperties],stdout=subprocess.PIPE)
    stdout = p.communicate()[0]
    stdout = stdout.split(b'\n')
    Precision = 0.0
    Recall = 0.0
    FMeasure = 0.0
    for line in stdout:
        if line.startswith(b"Precision"):
            line = line.decode('utf-8')
            print(line)
            Precision = re.findall("\d+\.\d+",line)
            if len(Precision) > 0:
                Precision = float(Precision[0])
            else:
                Precision = 0.0
    for line in stdout:
        if line.startswith(b"Recall"):
            line = line.decode('utf-8')
            print(line)
            Recall = re.findall("\d+\.\d+",line)
            if len(Recall) > 0:
                Recall = float(Recall[0])
            else:
                Recall = 0.0
    for line in stdout:
        if line.startswith(b"F-Measure"):
            line = line.decode('utf-8')
            print(line)
            FMeasure = re.findall("\d+\.\d+",line)
            if len(FMeasure) > 0:
                FMeasure = float(FMeasure[0])
            else:
                FMeasure = 0.0              
    #print(sourceFileName , ERtype, beta, sigma, mu, Precision, Recall, FMeasure)
    runStatistics.write('\n***Final Results***\n')
    runStatistics.write('Precision = '+str(Precision)+'\n')
    runStatistics.write('Recall = '+str(Recall)+'\n')  
    runStatistics.write('F-Measure = '+str(FMeasure)+'\n')
    triple = (Precision, Recall, FMeasure)
    return triple
    
    


# In[6]:


def run_Cluster_ERMetics():
    global erMetricsPrefix
    erMetricsProperties = erMetricsPrefix + 'clusters.properties'
    subprocess.run(["java", "-jar", "er-metrics.jar", erMetricsProperties], text=True)
    p = subprocess.Popen(['java', '-jar', 'er-metrics.jar', erMetricsProperties],stdout=subprocess.PIPE)
    stdout = p.communicate()[0]
    stdout = stdout.split(b'\n')
    Precision = 0.0
    Recall = 0.0
    FMeasure = 0.0
    for line in stdout:
        if line.startswith(b"Precision"):
            line = line.decode('utf-8')
            #print(line)
            Precision = re.findall("\d+\.\d+",line)
            if len(Precision) > 0:
                Precision = float(Precision[0])
            else:
                Precision = 0.0
    for line in stdout:
        if line.startswith(b"F-Measure"):
            line = line.decode('utf-8')
            #print(line)
            FMeasure = re.findall("\d+\.\d+",line)
            if len(FMeasure) > 0:
                FMeasure = float(FMeasure[0])
            else:
                FMeasure = 0.0
    for line in stdout:
        if line.startswith(b"Recall"):
            line = line.decode('utf-8')
            #print(line)
            Recall = re.findall("\d+\.\d+",line)
            if len(Recall) > 0:
                Recall = float(Recall[0])
            else:
                Recall = 0.0
    triple = [FMeasure, Precision, Recall]
    return triple


# In[7]:


def calculateEntropy(clusterList):
    #print('Starting Cluster Process')
    blockList = []
    triple = clusterList[0]
    clusterID = triple[1]
    for j in range(0,len(clusterList)):
        triple = clusterList[j]
        body = triple[2]
        tokenList = re.split(' ',body)
        if '' in tokenList:
            print('Find blank =', triple)
        blockList.append(tokenList)
    nbrRecs=len(blockList)
    reprocessFlag = False
    clusterEntropy = 0
    for j in range(0, nbrRecs):
        tokenList = blockList[j]
        #print('Starting Row',j,'Token List =',tokenList)
        while len(tokenList)>0:
            token = tokenList.pop(0)
            tokenCnt = 1
            for k in range(j+1, nbrRecs):
                rowTokens = blockList[k]
                if len(rowTokens)>0:
                    if token in rowTokens:
                        index = rowTokens.index(token)
                        rowTokens.pop(index)
                        tokenCnt = tokenCnt + 1
            probability = tokenCnt/nbrRecs
            entropy = -(math.log2(probability)*probability)
            clusterEntropy = clusterEntropy + entropy
    #print("Cluster Entropy =",clusterEntropy)
    return clusterEntropy


# In[8]:


def iterateClusters():
    global runClusterMetrics
    global epsilon
    clusterInputFile= open('ClusterOutput.txt', 'r')
    reprocessFile = open('ReprocessClusters.txt', 'w') 
    rec = clusterInputFile.readline()
    rec = rec.strip()
    clusterTable =[]
    while rec!='':
        parts = re.split(':',rec)
        clusterTable.append((parts[0], parts[1], parts[2]))
        rec = clusterInputFile.readline()
        rec = rec.strip() 
    clusterInputFile.close()
    #print('clusterTable size=',len(clusterTable))
    clusterTable.sort(key = sortSecond)
    #find blocks
    cluster=[]
    prevBlkID=''
    reprocessFlag = False
    clusterToFinalCnt = 0
    refsToFinalCnt = 0
    clusterToReprocess = 0
    refsToReprocess = 0
    # Find clusters in clusterTable
    for x in clusterTable:
        refID = x[0]
        blkID = x[1]
        body = x[2]
        if blkID==prevBlkID:
            cluster.append((refID,blkID, body))
        else:
            clusterSize = len(cluster)
            if clusterSize>1:
                #print('------process cluster---------')
                #print(clusterSize)  
                #for y in cluster:
                    #print(y)
                clusterEntropy = calculateEntropy(cluster)
                clusterLink = open('ClusterLinks.txt','w')
                for x in cluster:
                    line = x[0]+' '+x[1]+'\n'
                    clusterLink.write(line)
                clusterLink.close()
                if runClusterMetrics:
                    triple = run_Cluster_ERMetics()
                    FMeas = triple[0]
                    Precision = triple[1]
                    Recall = triple[2]
                    traceStatistics.write(str(mu)+'\t'+str(epsilon)+'\t'+str(clusterSize)+'\t'+str(clusterEntropy)+'\t')
                    traceStatistics.write(str(FMeas)+'\t'+str(Precision)+'\t'+str(Recall)+'\n')
                else:
                    traceStatistics.write(str(mu)+'\t'+str(epsilon)+'\t'+str(clusterSize)+'\t'+str(clusterEntropy)+'\n')
                if clusterEntropy > epsilon:
                    reprocessFlag = True
                    clusterToReprocess +=1
                    refsToReprocess = refsToReprocess + clusterSize
                    for y in cluster:
                        ref = y[0]+' '+y[2]+'\n'
                        reprocessFile.write(ref)
                else:
                    clusterToFinalCnt +=1
                    if clusterSize in clusterProfile:
                        clusterCount = clusterProfile[clusterSize]
                        clusterCount +=1
                        clusterProfile[clusterSize] = clusterCount
                    else:
                        clusterProfile[clusterSize] = 1
                    refsToFinalCnt = refsToFinalCnt + clusterSize                                                                                                            
                    for z in cluster:
                        ref = z[0]+' '+z[1]+'\n'
                        goodClusterFile.write(ref)                                                                             
            else:
                if clusterSize==1:
                    #print('---process single block')
                    if runClusterMetrics:
                        traceStatistics.write(str(mu)+'\t'+str(epsilon)+'\t1\t0.0\t1.0\t1.0\t1.0\n')
                    else:
                        traceStatistics.write(str(mu)+'\t'+str(epsilon)+'\t1\t0.0\n')
                    for y in cluster:
                        #print(y)
                        reID = y[0]
                        blID = y[1]
                        bdy = y[2]
                        finalCluster= reID+' '+blID+'\n'
                        goodClusterFile.write(finalCluster)
                        clusterToFinalCnt = clusterToFinalCnt + 1
                        if clusterSize in clusterProfile:
                            clusterCount = clusterProfile[clusterSize]
                            clusterCount +=1
                            clusterProfile[clusterSize] = clusterCount
                        else:
                            clusterProfile[clusterSize] = 1
                        refsToFinalCnt = refsToFinalCnt + clusterSize
            cluster=[]
            cluster.append((refID,blkID,body))
        prevBlkID = blkID
    clusterSize = len(cluster)
    if clusterSize>1:
        #print('------process cluster---------')
        #print(clusterSize)  
        #for y in cluster:
            #print(y)
        clusterEntropy = calculateEntropy(cluster)
        clusterLink = open('ClusterLinks.txt','w')
        for x in cluster:
            line = x[0]+' '+x[1]+'\n'
            clusterLink.write(line)
        clusterLink.close()
        if runClusterMetrics:
            triple = run_Cluster_ERMetics()
            FMeas = triple[0]
            Precision = triple[1]
            Recall = triple[2]
            traceStatistics.write(str(mu)+'\t'+str(epsilon)+'\t'+str(clusterSize)+'\t'+str(clusterEntropy)+'\t')
            traceStatistics.write(str(FMeas)+'\t'+str(Precision)+'\t'+str(Recall)+'\n')
        else:
            traceStatistics.write(str(mu)+'\t'+str(epsilon)+'\t'+str(clusterSize)+'\t'+str(clusterEntropy)+'\n')
        if clusterEntropy > epsilon:
            reprocessFlag = True
            clusterToReprocess +=1
            refsToReprocess = refsToReprocess + clusterSize
            for y in cluster:
                ref = y[0]+' '+y[2]+'\n'
                reprocessFile.write(ref)
        else:
            clusterToFinalCnt +=1
            if clusterSize in clusterProfile:
                clusterCount = clusterProfile[clusterSize]
                clusterCount +=1
                clusterProfile[clusterSize] = clusterCount
            else:
                clusterProfile[clusterSize] = 1
            refsToFinalCnt = refsToFinalCnt + clusterSize                                                                                                            
            for z in cluster:
                ref = z[0]+' '+z[1]+'\n'
                goodClusterFile.write(ref)                                                                             
    else:
        if clusterSize==1:
            #print('---process single block')
            if runClusterMetrics:
                traceStatistics.write(str(mu)+'\t'+str(epsilon)+'\t1\t0.0\t1.0\t1.0\t1.0\n')
            else:
                traceStatistics.write(str(mu)+'\t'+str(epsilon)+'\t1\t0.0\n')
            for y in cluster:
                #print(y)
                reID = y[0]
                blID = y[1]
                bdy = y[2]
                finalCluster= reID+' '+blID+'\n'
                goodClusterFile.write(finalCluster)
                clusterToFinalCnt = clusterToFinalCnt + 1
                if clusterSize in clusterProfile:
                    clusterCount = clusterProfile[clusterSize]
                    clusterCount +=1
                    clusterProfile[clusterSize] = clusterCount
                else:
                    clusterProfile[clusterSize] = 1
                refsToFinalCnt = refsToFinalCnt + clusterSize
    reprocessFile.close()
    #print("mu =", mu, "Clusters to Final= ",clusterToFinalCnt, " Refs to Final=",refsToFinalCnt)
    runStatistics.write('Clusters to Final = '+str(clusterToFinalCnt)+' Refs to Final = '+str(refsToFinalCnt)+'\n')
    runStatistics.write('Clusters to Reprocess = '+str(clusterToReprocess)+' Refs to Reprocess = '+str(refsToReprocess)+'\n')
    return(reprocessFlag)


# In[9]:


def runTransitiveClosure():
    runStatistics.write('Transitive Closure of Pairs'+'\n')
    #print('Transitive Closure of Pairs')
    inPairs = open('RefidClusteridPairs.txt', 'r')
    outPairs = open('Input_TC.txt', 'w')
    rec = inPairs.readline() 
    rec = rec.strip()
    recCount=0
    table =[]
    while rec != '':
        recCount = recCount+1
        tokens = re.split(',',rec)
        table.append((tokens[0], tokens[1]))
        rec = inPairs.readline()
        rec = rec.strip()
    pairCnt = len(table)
    runStatistics.write('(RefID, ClusterID) pair count = '+str(pairCnt)+'\n')
    #print('(RefID, ClusterID) pair count = '+str(pairCnt))
    table.sort(key = sortSecond)
    refList=[]
    prevToken=''
    cnt=0
    for j in range(0,len(table)):
        pair = table[j]
        refID = pair[0]
        token = pair[1]
        if token==prevToken:
            refList.append(refID)
        else:
            if len(refList)>0:
                anchor = refList[0]
                for k in range(0,len(refList)):
                    new = refList[k]
                    newpair = anchor+', '+new
                    newpair2 = new+', '+new
                    outPairs.write(newpair+'\n')
                    outPairs.write(newpair2+'\n')
                    cnt = cnt + 2
            refList=[]
            refList.append(refID)
        prevToken = token
    if len(refList)>0:
        anchor = refList[0]
        for k in range(0, len(refList)):
            new = refList[k]
            newpair= anchor+', '+new
            newpair2 = new+', '+new
            #print(anchor+', '+new)
            outPairs.write(newpair+'\n')
            outPairs.write(newpair2+'\n')
            cnt = cnt + 2     
    # Be sure to close files so all records are written to output
    inPairs.close()
    outPairs.close()
    runStatistics.write('(RefID, RefID) pair count = '+str(cnt)+'\n')
    #print('(RefID, RefID) pair count = '+str(cnt))
    MRun = ('Input_TC.txt')
    subprocess.run(["java", "-jar", "sorting-closure-1.0.jar"], input="\n".join([MRun, ""]), text=True)
    joinFiles('ClosureOuput.txt','ClusterOutput.txt',False)
    return


# In[10]:


def scoringMatrix(block, blockNbr, pairFile):
    output = open('MatrixRobotInput.txt','w')
    for j in range(0,len(block)):
        output.write(block[j]+'\n')
    output.close()
    runscoringMatrix()
    input = open ('MatrixRobotIndex.link','r')
    recLink = input.readline()
    recLink = input.readline()
    while recLink != '':
        recLink = re.sub('[\W]+',' ',recLink)
        tokens = re.split(' ',recLink)
        #print(tokens)
        recLink = input.readline()
        RefID = tokens[1]
        OID = tokens[2]
        pairRec=RefID+","+str(blockNbr)+OID+'\n'
        #print(pairRec)
        pairFile.write(pairRec)
    input.close()
    return


# In[11]:


def pythonMatrix(ref1, ref2):
    #print(ref1,'***',ref2)
    Class = DamerauLevenshtein()
    score = 0.0  
    if len(ref1)==0 or len(ref2)==0:
        return score
    stillMore = True
    total = 0.0
    loops = 0
    while stillMore:
        len1 = len(ref1)
        len2 = len(ref2)
        maxVal = 0.0
        for j in range(0,len1):
            token1 = ref1[j]
            for k in range(0,len2):
                token2 = ref2[k]
                led = Class.normalized_similarity(token1,token2)
                if led >= maxVal:
                    maxVal = led 
                    saveJ = j
                    saveK = k
                if maxVal == 1.00:
                    break
        #end of nested loops
        loops +=1
        total = total + maxVal
        ref1.pop(saveJ)
        ref2.pop(saveK)
        if (len(ref1)==0) or (len(ref2)==0):
            stillMore = False
    #end of while loop
    score = total/loops
    return score


# In[12]:


def newMatrix(block, blockNbr, pairFile):
    blockSize = len(block)
    for j in range(0, blockSize-1):
        ref1 = block[j]
        part = ref1.split(':')
        refID1 = part[0]
        list1 = part[1].split( )
        for k in range(j+1, blockSize):
            ref2 = block[k]
            part = ref2.split(':')
            refID2 = part[0]
            list2 = part[1].split()
            score = pythonMatrix(list1[:], list2[:])
            #print('>>score= ',score,' mu= ', mu)
            if score >= mu:
                oid1 = refID1+str(blockNbr)
                pairFile.write(refID1+','+oid1+'\n')
                pairFile.write(refID2+','+oid1+'\n')                
    return


# In[13]:


def runER(ERtype, block, blockNbr, pairFile):
    if ERtype == "NewMatrix":
        newMatrix(block, blockNbr, pairFile)
        return
    print("Invalid ERrun type given")
    return


# In[14]:


def iterateBlocks(ERtype, table):
    runStatistics.write('Start of Block Iteration, mu = '+str(mu)+'\n')
    pairFile = open('RefidClusteridPairs.txt', 'w')
    blockToken = ''
    block = []
    refID =[]
    singleNbr = 0
    blockNbr = 0
    for line in table:
        #print(line)
        part = re.split(':', line)
        if part[0]== blockToken:
            block.append(part[1]+":"+part[2])
        else: 
            blockSize = len(block)
            if blockSize> 1:
                blockNbr +=1
                runER(ERtype, block, blockNbr, pairFile)
            else:
                if blockSize ==1:
                    singleNbr +=1
            block = []
            block.append(part[1]+":"+part[2])
        blockToken = part[0]
    ## end of read loop
    if len(block)>1 :
        blockNbr +=1
        runER(ERtype, block, blockNbr, pairFile)
    runStatistics.write('  **End of Block Iteration\n')
    runStatistics.write('    Single-Reference Blocks = '+str(singleNbr)+'\n')
    runStatistics.write('    Multi-Reference Blocks = '+str(blockNbr)+'\n')
    #print('  **End of Block Iteration, Total Blocks = '+str(blockNbr))
    pairFile.close()
    return


# In[15]:


def buildBlocks(fileName):
    global runStatistics
    input = open(fileName,'r')
    #IMPORTANT - Reference ID must be first token 
    blkCount=0
    outCount=0
    inCount=0
    stopCount=0
    uniBlk = []
    table = []
    rec = input.readline()
    while rec != '':
        inCount +=1
        rec = rec.strip()
        tokens = re.split(' ',rec)
        refID = tokens[0]
        # This look runs through all tokens in the record following RecID
        blockTokens=[]
        NewRec = refID+':'
        for j in range(1, len(tokens)):
            token = tokens[j]
            if token != '':
                count = index.get(token)
                if count<sigma:
                    NewRec = NewRec + ' '+token
                else:
                    stopCount +=1
                if count<beta and count>1:
                    blkCount +=1
                    blockTokens.append(token)
                    if token not in uniBlk:
                        uniBlk.append(token)
        for j in range(0, len(blockTokens)):
            token = blockTokens[j]
            table.append(token+":"+NewRec)
            #print(token, NewRec)
            outCount = outCount + 1
        rec = input.readline()
    input.close()
    runStatistics.write('  Total Records Read = '+str(inCount)+'\n')
    runStatistics.write('  Stop Words Removed = '+str(stopCount)+'\n') 
    runStatistics.write('  Unique Blocking Tokens = '+str(len(uniBlk))+'\n') 
    runStatistics.write('  Total Blocking Records = '+str(outCount)+'\n')
    table.sort()
    return table


# In[16]:

def main(fileName):
    
    if runKrisJavaJar:
        passTableToJava(fileName)
    else:
        table = buildBlocks(fileName) 
        iterateBlocks(ERtype, table)
    runTransitiveClosure()
    reprocess = iterateClusters()
    global mu
    global epsilon

   
    #mu = 1
    if reprocess and (mu + muIterate < 1.0):
        mu = mu + muIterate
        epsilon = epsilon + epsilonIncrement
        print("\n>>>>>>>>>>>>\nStarting Iteration mu=",mu)
        print("Starting Iteration epsilon=",epsilon)
        runStatistics.write('---------------------\n')
        runStatistics.write('New Iteration of file '+fileName+' mu='+str(mu)+'\n')
        runStatistics.write('New Iteration of file '+fileName+' epsilon='+str(epsilon)+'\n')
        main('ReprocessClusters.txt')
   
    return


# In[17]:


def driver(fn, bt, sg, m, mi, eps, epsin, rCM, rFM, cFJ,rpf, jar):
    global sourceFileName
    global hasHeader 
    hasHeader = rpf  
    global clusterProfile
    sourceFileName = fn
    global runKrisJavaJar
    runKrisJavaJar = jar
    #start time
    start = time.perf_counter()

    #set paramters
    programVersion = 'DWM3_Entropy_Cluster'
    currentDT = datetime.datetime.now()
    #ERtype = "ML_doc2vec_DBScan"
    #ERtype = "ScoringMatrix"
    global ERtype
    ERtype = "NewMatrix"
    #sourceFileName = 'S8-TokenReplace.txt'
    hyphenIndex = sourceFileName.find('-')
    samplePrefix = sourceFileName[0:hyphenIndex]
    sampleName = samplePrefix +'.txt'

    global beta
    beta = bt
    global sigma
    sigma = sg
    global mu
    mu = m
    global muIterate
    muIterate = mi
    global epsilon
    epsilon = eps
    global epsilonIncrement
    epsilonIncrement= epsin
    global runClusterMetrics
    runClusterMetrics = rCM
    runFinalMetrics = rFM
    createFinalJoin = cFJ

    #build file name suffix
    part = sourceFileName.split('.')
    source = part[0]
    today = date.today()
    #suffix = '_'+source+'_'+str(today)+'_B'+str(beta)+'S'+str(sigma)+'E'+str(epsilon)
    runStatsName = samplePrefix+'-ResultsStats.txt'
    traceStatsName = samplePrefix+'-ResultsTrace.txt'
    #open files
    global goodClusterFile
    goodClusterFile = open('GoodClusters.txt', 'w')
    global runStatistics
    runStatistics = open(runStatsName,'w')
    global traceStatistics
    traceStatistics = open(traceStatsName,'w')

    #Initialize Cluster Profile Dictionary
    clusterProfile = {}
    #Initialize Sample to Truth Dictionary
    truthSelect = {
        'S1.txt':'ERMetricsGoodDQ',
        'S2.txt':'ERMetricsGoodDQ',
        'S3.txt':'ERMetricsRestaurant',
        'S4.txt':'ERMetricsGoodDQ',
        'S5.txt':'ERMetricsGoodDQ',
        'S6.txt':'ERMetricsGeCo',
        'S7.txt':'ERMetricsGoodDQ',
        'S8.txt':'ERMetricsPoorDQ',
        'S8_afterCleaning.txt':'ERMetricsPoorDQ',
        'S9.txt':'ERMetricsPoorDQ',
        'S10.txt':'ERMetricsPoorDQ',
        'S11.txt':'ERMetricsPoorDQ',
        'S12.txt':'ERMetricsPoorDQ',
        'S13.txt':'ERMetricsGoodDQ',
        'S14.txt':'ERMetricsGoodDQ',
        'S15.txt':'ERMetricsGoodDQ',
        'S16.txt':'ERMetricsPoorDQ',
        'S17.txt':'ERMetricsPoorDQ',
        'S18.txt':'ERMetricsPoorDQ'
        }
    global erMetricsPrefix
    if runFinalMetrics or runClusterMetrics:
        erMetricsPrefix = truthSelect.get(sampleName)

    #create token frequency table
    global index
    index = {}
    input = open(sourceFileName,'r')
    cntAllTokens = 0
    cntUniqueTokens = 0
    cntRefs = 0
    rec = input.readline()
    while rec != '':
        cntRefs += 1
        rec = rec.strip()
        firstComma = rec.find(',')
        tokens = re.split(r'\s+',rec)
        for j in range(1,len(tokens)):
            if tokens[j]!='':
                token = tokens[j]
                cntAllTokens += 1
                if token not in index:
                    index[token]=1
                    cntUniqueTokens += 1
                else:
                    count = index.get(token)
                    count = count + 1
                    index[token]=count
        rec =  input.readline()
    input.close()
    sum = 0
    avgFreq = cntAllTokens/cntUniqueTokens
    maxFreq = 0
    minFreq = 1000000
    for key in index:
        count = index[key]
        sum = sum + (count - avgFreq)*(count - avgFreq)
        if count > maxFreq:
            maxFreq = count
        if count < minFreq:
            minFreq = count
    stdev = math.sqrt(sum/cntUniqueTokens)
    resultsList = []
    resultsList.append(cntRefs)
    resultsList.append(cntAllTokens) 
    resultsList.append(cntUniqueTokens)
    resultsList.append(avgFreq)
    resultsList.append(stdev)
    resultsList.append(maxFreq)
    resultsList.append(minFreq)
    
    #record parameters
    runStatistics.write('Program Version = '+programVersion+'\n')
    runStatistics.write('Start Date/Time = '+str(currentDT)+'\n')
    runStatistics.write('Source File = '+sourceFileName+'\n')
    runStatistics.write('Run Mode = '+ERtype+'\n')
    traceStatistics.write('Program Version = '+programVersion+'\n')
    traceStatistics.write('Data/Time = '+str(currentDT)+'\n')
    traceStatistics.write('Source File = '+sourceFileName+'\n')
    traceStatistics.write('Run Mode = '+ERtype+'\n')
    if runClusterMetrics:
        traceStatistics.write('mu\tepsilon\tSize\tEntropy\tF-Meas\tPrecision\tRecall\n')
    else:
        traceStatistics.write('mu\tepsilon\tSize\tEntropy\n')
    runStatistics.write('Beta (blocking) = '+str(beta)+'\n')
    runStatistics.write('Sigma (stop word) = '+str(sigma)+'\n')
    runStatistics.write('Mu (match start) = '+str(mu)+'\n')
    runStatistics.write('Mu Increment = '+str(muIterate)+'\n')
    runStatistics.write('Epsilon (entropy) = '+str(epsilon)+'\n')
    runStatistics.write('Epsilon Increment = '+str(epsilonIncrement)+'\n')
    runStatistics.write('---------------------\n')
    runStatistics.write('Number of References = '+str(cntRefs)+'\n')
    runStatistics.write('Total Number of Tokens = '+str(cntAllTokens)+'\n')
    runStatistics.write('Number of Unique Tokens = '+str(cntUniqueTokens)+'\n')
    runStatistics.write('Average Token Frequency = '+str(avgFreq)+'\n')
    runStatistics.write('Std Dev of Frequency = '+str(stdev)+'\n')
    runStatistics.write('Maximum Frequency = '+str(maxFreq)+'\n')
    runStatistics.write('Minimum Frequency = '+str(minFreq)+'\n')

    #start program
    print("\n>>>>>>>>>>>>\nStarting Iteration mu=",mu)
    print("Starting Iteration epsilon=",epsilon)
    runStatistics.write('---------------------\n')
    runStatistics.write('Initial Processing of file '+sourceFileName+' mu='+str(mu)+'\n') 
    main(sourceFileName)
    goodClusterFile.close()
    buildLinkFile()
    runStatistics.write('\nCluster Profile\n')
    runStatistics.write('Size\tCount\tReferences\n')
    totalClusters = 0
    totalRefs = 0
    for key in sorted(clusterProfile.keys()):
        count = clusterProfile[key]
        totalClusters = totalClusters + count
        refs = key * count
        totalRefs = totalRefs + refs
        runStatistics.write(str(key)+'\t'+str(count)+'\t'+str(refs)+'\n')
    runStatistics.write('Totals\t'+str(totalClusters)+'\t'+str(totalRefs)+'\n')
    if runFinalMetrics:
        triple = run_ERMetics_Final()
    else:
        triple = (0.0,0.0,0.0)
        runStatistics.write('\nFlag for Final ER Metrics set to False\n')
    if createFinalJoin:
        joinFiles('ResultsLinkFile.txt',samplePrefix+'-ResultsFinalJoin.txt',True)
    newName = samplePrefix+'-ResultsLinkFile.txt'
    if os.path.exists(newName):
        os.remove(newName)
    os.rename('ResultsLinkFile.txt',newName)

    #end of program
    currentDT = datetime.datetime.now()
    runStatistics.write('\nFinish Date/Time = '+str(currentDT)+'\n')
    end = time.perf_counter()
    totalTime = end - start
    runStatistics.write('Total Time = '+str(totalTime)+'\n')

    #close files
    runStatistics.close()
    traceStatistics.close()
    resultsList.append(triple[0])
    resultsList.append(triple[1])
    resultsList.append(triple[2])
    return resultsList


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




