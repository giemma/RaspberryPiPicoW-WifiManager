

def GetParameterValue(string, parameterName):
    startpos= string.find(parameterName)+len(parameterName)
    if startpos < 0:
        return ''
    
    endpos=string.find('&',startpos+1)
    if endpos < 0:
        endpos=len(string)
        
    return string[startpos:endpos]

def GetRequestPageGet(requestString):
    if requestString == '':
        return '/'
        
    startpos= requestString.find('GET ')+4
    endpos=requestString.find(' ',startpos+1)
    return requestString[startpos:endpos] 