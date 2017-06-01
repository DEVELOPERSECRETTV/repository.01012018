# -*- coding: utf-8 -*-

import re

def findall(data,regex):
    p_reg = re.compile(regex, re.IGNORECASE + re.DOTALL + re.MULTILINE + re.UNICODE)
    result = p_reg.findall(data)
    return result

def parseTextToGroups(txt, regex):
    p = re.compile(regex, re.IGNORECASE + re.DOTALL + re.MULTILINE + re.UNICODE)
    m = p.match(txt)
    '''cipq'''
    '''Printar todos los grupos'''
    #try:print '***parseTextToGroups***',txt.decode('utf-8','ignore'),m.groups()
    #except:print 'puto UNICODE parseTextToGroups';pass
    if m:
        return m.groups()
    else:
        return None
    
def parseText(txt, regex, variables=[]):
    groups = parseTextToGroups(txt, regex)
    if variables == []:
        if groups:
            '''Printar grupo[0]'''
            #try:print '***parseText***',regex,variables,groups[0]
            #except:print 'UNICODE parseText';pass
            return groups[0]
        else:
            return ''
    else:
        resultArr = {}
        i = 0
        for v in variables:
            if groups:
                resultArr[v] = groups[i]
            else:
                resultArr[v] = ''
            i += 1
        return resultArr