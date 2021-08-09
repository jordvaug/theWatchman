import re
import random

def urlParser(url):
    url = findVariablesInUrl(url)
    return url

def findVariablesInUrl(url):
    startVar = False
    var = ''
    newUrl = ''


    for s in url:
        if s == '{':
            startVar = True
        elif s == '}':
            if startVar:
                startVar = False
                var = fillVariables(var)
                newUrl += var
                var = ''
            else:
                newUrl += s
        elif startVar:
            if isAlphaNum(s):
                var += s
        else:
            newUrl += s

    return newUrl

def isAlphaNum(s):
    p = re.complile('\w*', re.IGNORECASE)
    return p.match(s) != None


def fillVariables(var):

    if re.search('user', var, re.IGNORECASE):
        var = fillUserIdVariable()
    elif re.search('id', var, re.IGNORECASE):
        var = fillNumberVariable()
    elif re.search('name', var, re.IGNORECASE):
        var = fillNameVariable()
    else:
        var = fillLettersVariable()

    return var


def fillUserIdVariable():
    return str(random.randrange(10, 1000000))


def fillNumberVariable():
    return str(random.randrange(10, 1000000))


def fillNameVariable():
    #TODO: read random from name file
    with open('./names.txt', 'r') as f:
        names = f.read().splitlines()

    index = random.randrange(0, len(names))

    return names[index]



def fillLettersVariable():
    #TODO: generate some letters
    return 'dsfkjke'



