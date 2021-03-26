#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import math
def calculateEntropy(epsilon, cluster):
    #print('Cluster')
    entropy = 0.0
    clusterSize = len(cluster)
    #print('cluster size =', clusterSize)
    for j in range(0, len(cluster)-1):
        jList = cluster[j]
        #print('j=',j,'jList=', jList)
        for token in jList:
            cnt = 1
            #print('token=', token, 'cnt=', cnt)
            for k in range(j+1,len(cluster)):
                #print('k=',k)
                if token in cluster[k]:
                    cnt +=1
                    cluster[k].remove(token)
                    #print('token found in ',k, cluster[k])
            tokenProb = cnt/clusterSize
            term = -tokenProb*math.log(tokenProb,2)
            entropy +=term
            if entropy > epsilon:
                #print('quit early')
                return entropy
            #print('**token=',token,'tokenProb=',tokenProb,' term=', term, 'entropy=', entropy)
            cnt = 0
    # Finish up for any tokens left in the last reference of the cluster
    for token in cluster[clusterSize-1]:
        tokenProb = 1.0/clusterSize
        term = -tokenProb*math.log(tokenProb,2)
        entropy +=term
        if entropy > epsilon:
            #print('quit early')
            return entropy
        #print('last row token=', token, 'tokenProb=',tokenProb,' term=', term, 'entropy=', entropy)
    return entropy

