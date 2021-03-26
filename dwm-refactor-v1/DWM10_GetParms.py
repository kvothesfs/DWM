#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys
def getParms(parmFileName):
    validParmNames = ['inputFileName','delimiter', 'hasHeader', 'tokenizerType', 'removeDuplicateTokens',                      'runReplacement', 'minFreqStdToken', 'minLenStdToken', 'maxFreqErrToken',                     'mu', 'muIterate', 'beta', 'sigma', 'epsilon', 'epsilonIterate',                      'runClusterMetrics', 'createFinalJoin',                       'comparator','truthFileName']
    parmFile = open(parmFileName,'r')
    parms = {}
    line = (parmFile.readline()).strip()
    while line != '':
        if  not line.startswith('#'):
            part = line.split('=')
            parmName = part[0].strip()
            if parmName not in validParmNames:
                print('**Error: Invalid Parameter Name in Parm File ',parmName)
                sys.exit()
            parmValue = part[1].strip()
            appended = False
            if '.' in parmValue and parmValue[len(parmValue)-1].isdigit():
                value = float(parmValue)
                parms[parmName]=value
                appended = True
            if parmValue.isdigit():
                value = int(parmValue)
                parms[parmName]=value
                appended = True
            if (parmValue=="True"):
                value = True
                parms[parmName]=value
                appended = True
            if (parmValue=="False"):
                value = False
                parms[parmName]=value
                appended = True
            if not appended:
                parms[parmName]=parmValue
        line = (parmFile.readline()).strip()
    return parms

