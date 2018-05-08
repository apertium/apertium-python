import re, pprint, subprocess, argparse

def analyze(fileName, moduleDir, strPair):
    p1 = subprocess.Popen(["cat", fileName], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["apertium", "-d %s" % moduleDir, strPair], stdin = p1.stdout, stdout = subprocess.PIPE)
    p1.stdout.close()
    return p2.communicate()[0].decode('utf-8')

def getLexicalUnitsStrings(analysis, splitByLines=False):
    if splitByLines:
        return [getLexicalUnitsStrings(splitAnalysis) for splitAnalysis in analysis.splitlines()]
    else:
        return re.findall(r'\^([^\$]*)\$([^\^]*)', analysis)

def parseLexicalUnitsString(lexicalUnitsStrings, splitByLines=False):
    if splitByLines:
        return [parseLexicalUnitsString(splitLexicalUnitsStrings) for splitLexicalUnitsStrings in lexicalUnitsStrings]
    else:
        lexicalUnits = []
        for (lexicalUnitString, seperator) in lexicalUnitsStrings:
            forms = lexicalUnitString.split('/')
            surfaceForm = forms[0]
            ambiguousUnitsString = forms[1:]
            
            ambiguousUnits = []
            for ambiguousUnit in ambiguousUnitsString:
                if not ambiguousUnitsString[0][0] == '*':
                    splitUnit = re.findall(r'([^<]*)<([^>]*)>', ambiguousUnit)
                    if len(splitUnit):
                        lemma = splitUnit[0][0]
                        tags = ['<%s>' % tagGroup[1] for tagGroup in splitUnit]
                        ambiguousUnits.append((lemma, tags))
            lexicalUnits.append(((surfaceForm, ambiguousUnits), seperator))
        return lexicalUnits

def getLexicalUnit(lexicalUnit):
    return lexicalUnit[0]

def getSeperator(lexicalUnit):
    return lexicalUnit[1]

def getSurfaceForm(lexicalUnit):
    return lexicalUnit[0][0]

def getTextFromUnit(lexicalUnit):
    return getSurfaceForm(lexicalUnit) + getSeperator(lexicalUnit)

def getTextFromUnits(lexicalUnits):
    return ''.join([getTextFromUnit(lexicalUnit) for lexicalUnit in lexicalUnits])

def getLemmas(lexicalUnit):
    return [ambiguousForm[0] for ambiguousForm in lexicalUnit[0][1]]

def getAmbiguousForms(lexicalUnit):
    return [ambiguousForm for ambiguousForm in lexicalUnit[0][1]]

def getLexicalUnitString(lexicalUnit):
    return getSurfaceForm(lexicalUnit) + '/' +  '/'.join([ambiguousForm[0] + ''.join(ambiguousForm[1]) for ambiguousForm in getAmbiguousForms(lexicalUnit)])

def getTags(lexicalUnit):
    return set(sum([ambiguousForm[1] for ambiguousForm in lexicalUnit[0][1]], []))

def stringSearch(lexicalUnitsStrings, searchTerm):
    return [(index, lexicalUnitString) for (index, lexicalUnitString) in enumerate(lexicalUnitsStrings) if searchTerm in lexicalUnitString[0]]

def tagSearch(lexicalUnits, searchTags, regex=True):
    searchTags = set(re.findall('<[^>]*>', searchTags))
    if regex:
        return [(index, lexicalUnit) for (index, lexicalUnit) in enumerate(lexicalUnits) if all([any([re.match(searchTag + '$', tag) for tag in getTags(lexicalUnit)]) for searchTag in searchTags])]
    else:
        return [(index, lexicalUnit) for (index, lexicalUnit) in enumerate(lexicalUnits) if getTags(lexicalUnit).issuperset(searchTags)]

def surfaceFormSearch(lexicalUnits, searchTerm, regex=True):
    if regex:
        return [(index, lexicalUnit) for (index, lexicalUnit) in enumerate(lexicalUnits) if re.match(searchTerm + '$', getSurfaceForm(lexicalUnit))]
    else:
        return [(index, lexicalUnit) for (index, lexicalUnit) in enumerate(lexicalUnits) if searchTerm in getSurfaceForm(lexicalUnit)]

def lemmaSearch(lexicalUnits, searchTerm, regex=True):
    if regex:
        return [(index, lexicalUnit) for (index, lexicalUnit) in enumerate(lexicalUnits) if any([re.match(searchTerm + '$', lemma) for lemma in getLemmas(lexicalUnit)])]
    else:
        return [(index, lexicalUnit) for (index, lexicalUnit) in enumerate(lexicalUnits) if searchTerm in getLemmas(lexicalUnit)]

def rawTextSearch(lexicalUnits, searchTerm, regex=True):
    return [(index, lexicalUnit) for (index, lexicalUnit) in enumerate(lexicalUnits) if re.match(re.escape(searchTerm) if not regex else searchTerm, getTextFromUnit(lexicalUnit))]

def getContext(lexicalUnits, index, window=15):
    surfaceForm = lexicalUnits[index][0]
    start = index - window
    end = index + window
    length = len(lexicalUnits)
    
    if start < 0 and end > length:
        output = (getTextFromUnits(lexicalUnits[0:index]), getTextFromUnits(lexicalUnits[index:end]))
    elif start > 0 and end > length:
        output = (getTextFromUnits(lexicalUnits[start:index]), getTextFromUnits(lexicalUnits[index:end]))
    elif start < 0 and end < length:
        output = (getTextFromUnits(lexicalUnits[0:index]), getTextFromUnits(lexicalUnits[index:end]))
    else:
        output = (getTextFromUnits(lexicalUnits[start:index]), getTextFromUnits(lexicalUnits[index:end]))
    return (output[0].replace('\r\n', ' ').replace('\n', ' '), output[1].replace('\r\n', ' ').replace('\n', ' '))

def searchLines(lines, searchFilterGroups):
    #return [lexicalUnits for lexicalUnits in lines if all([any([all([len(searchFunction([lexicalUnit], args[0], regex=args[1])) > 0 for (searchFunction, args) in searchFiltersGroup]) for lexicalUnit in lexicalUnits]) for searchFiltersGroup in searchFilterGroups])]
    
    #for those who which to retain their sanity:
    output0 = []
    for lexicalUnits in lines:
        output1 = []
        highlight = []
        for searchFiltersGroup in searchFilterGroups:
            output2 = []
            for (index, lexicalUnit) in enumerate(lexicalUnits):
                output3 = []
                for (searchFunction, args) in searchFiltersGroup:
                    output3.append(len(searchFunction([lexicalUnit], args[0], regex=args[1])) > 0)
                if(all(output3)):
                    highlight.append(index)
                output2.append(all(output3))
            output1.append(any(output2))
        if(all(output1)):
            output0.append((lexicalUnits, highlight))
    return output0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Search the morphological analysis of a corpus.')
    parser.add_argument('corpus', help='Path to corpus')
    parser.add_argument('module', help='Path to language module')
    parser.add_argument('pair', help='Name of language pair')
    parser.add_argument('string', help='Search string')
    parser.add_argument('searchType', help='Type of search to perform', choices=['tag', 'surfaceForm', 'lemma'])
    parser.add_argument('-w', '--window', help='Search window', type=int, default=10)
    parser.add_argument('-r', '--regex', help='Enable Regex', type=bool, default=True)
    args = parser.parse_args()
    
    analysis = analyze(args.corpus, args.module, args.pair)
    lexicalUnitsStrings = getLexicalUnitsStrings(analysis)
    lexicalUnits = parseLexicalUnitsString(lexicalUnitsStrings)
    
    searchMethods = {'tag': tagSearch, 'surfaceForm': surfaceFormSearch, 'lemma': lemmaSearch }
    searchResults = searchMethods[args.searchType](lexicalUnits, args.string, regex=args.regex)
    for (index, lexicalUnit) in searchResults:
        print(''.join(getContext(lexicalUnits, index, window=args.window)))
        print(lexicalUnitsStrings[index][0])
        print()

'''if __name__ == '__main__':
    analysis = analyze('3_sentences', '/home/apertium/Desktop/apertium-en-es', 'en-es-anmor')
    lexicalUnitsStrings = getLexicalUnitsStrings(analysis, splitByLines=True)
    lexicalUnits = parseLexicalUnitsString(lexicalUnitsStrings, splitByLines=True)
    print(getRawLine(lexicalUnits, 1))
    searchFilterGroups = [[(tagSearch, ('<n>', True)), (lemmaSearch, ('population', False))], [(surfaceFormSearch, ('[0-9]+', True))]]
    print(searchLines(lexicalUnits, searchFilterGroups))
    
    analysis = analyze('3_sentences', '/home/apertium/Desktop/apertium-en-es', 'en-es-anmor')
    lexicalUnitsStrings = getLexicalUnitsStrings(analysis)
    lexicalUnits = parseLexicalUnitsString(lexicalUnitsStrings)
    testIndex = 8
    print(lexicalUnits[testIndex])
    print(getTags(lexicalUnits[testIndex]))
    print(getSurfaceForm(lexicalUnits[testIndex]))
    print(getLemmas(lexicalUnits[testIndex]))
    print(getContext(lexicalUnits, testIndex))
    
    pprint.pprint(tagSearch(lexicalUnits, '<n><sg>'))
    pprint.pprint(surfaceFormSearch(lexicalUnits, 'previous'))
    pprint.pprint(lemmaSearch(lexicalUnits, 'council'))'''
