from enum import Enum

class LRN_STATE(Enum):
    ROOT = 1
    SECTION = 2
    SPECIAL_ACQUIRE_ROOT = 3
    SPECIAL_ACQUIRE_SECTION = 4

def lrnParser(lrn):
    lrnDict = dict()
    s = LRN_STATE.ROOT

    sectionName = ''
    acquireChannel = ''

    i = 0
    while i < len(lrn):
        if s == LRN_STATE.ROOT:
            if lrn[i:i+15] == ':ACQuire:FILTer':
                sectionName = ':ACQuire:FILTer'
                if not sectionName in lrnDict:
                    lrnDict[sectionName] = dict()
                s = LRN_STATE.SPECIAL_ACQUIRE_ROOT
                continue

            if lrn[i] == ':':
                sectionIndex = lrn.find(':',i+1)
                sectionName = lrn[i+1:sectionIndex]
                s = LRN_STATE.SECTION
                i = sectionIndex+1
        
        elif s == LRN_STATE.SECTION:
            if lrn[i] == ':':
                s = LRN_STATE.ROOT
            else:
                index = lrn.find(' ',i)
                endIndex = lrn.find(';',index)
                parameterName = lrn[i:index]
                parameterValue = lrn[index+1:endIndex]
                lrnDict[':'+sectionName+':'+parameterName] = parameterValue
                i = endIndex+1
                if sectionName == 'SEARCH' and not parameterName == 'TOTAL':
                    i = i+1
        
        elif s == LRN_STATE.SPECIAL_ACQUIRE_ROOT:
            parameterIndex = lrn.find(' ',i)
            if lrn[i:parameterIndex] == ':ACQuire:FILTer:SOURce':
                endIndex = lrn.find(';',parameterIndex+1)
                acquireChannel = lrn[parameterIndex+1:endIndex]
                if not acquireChannel in lrnDict[sectionName]:
                    lrnDict[sectionName][acquireChannel] = dict()
                i = endIndex+1
                s = LRN_STATE.SPECIAL_ACQUIRE_SECTION

        elif s == LRN_STATE.SPECIAL_ACQUIRE_SECTION:
            parameterIndex = lrn.find(' ',i)
            endIndex = lrn.find(';',parameterIndex+1)
            parameterName = lrn[i:parameterIndex]
            parameterValue = lrn[parameterIndex+1:endIndex]
            lrnDict[sectionName][acquireChannel][parameterName] = parameterValue
            i = endIndex+1
            parameterIndex = lrn.find(':',i+1)
            if lrn[i:parameterIndex] != ':ACQuire':
                s = LRN_STATE.ROOT
                continue
            parameterIndex = lrn.find(' ',i)
            if lrn[i:parameterIndex] == ':ACQuire:FILTer:SOURce':
                s = LRN_STATE.SPECIAL_ACQUIRE_ROOT
                continue
    
    return lrnDict