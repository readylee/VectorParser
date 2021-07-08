#!/usr/bin/env python

from collections import deque

adjacencyList = []        

## @fn initSearch
## creates a trie of keywords, 
## sets fail transitions, and stores keywords (search terms)
## @param keywords list containing search term(s)     
def initSearch(keywords):
    createEmptyTrie()
    setSearchTerms(keywords)
    setFailTransitions()

## initalizes the trie root
def createEmptyTrie():
    adjacencyList.append({'value':'', 'nextStates':[],'failState':0,'result':[]})

## add all keywords in the list of keywords
## @param keywords list of keywords to find in search strings
def setSearchTerms(keywords):
    for keyword in keywords:
        addSearchTerm(keyword)

def addSearchTerm(keyword):
    ## add keyword to the trie, mark output at the last node 
    current = 0
    j = 0
    keyword = keyword.lower()
    child = findNext(current, keyword[j])
    while child != None:
        current = child
        j = j + 1
        if j < len(keyword):
            child = findNext(current, keyword[j])
        else:
            break
    for i in range(j, len(keyword)):
        node = {'value':keyword[i],'nextStates':[],'failState':0,'result':[]}
        adjacencyList.append(node)
        adjacencyList[current]["nextStates"].append(len(adjacencyList) - 1)
        current = len(adjacencyList) - 1
    adjacencyList[current]["result"].append(keyword)

def setFailTransitions():
    q = deque()
    child = 0
    for node in adjacencyList[0]["nextStates"]:
        q.append(node)
        adjacencyList[node]["failState"] = 0
    while q:
        r = q.popleft()
        for child in adjacencyList[r]["nextStates"]:
            q.append(child)
            state = adjacencyList[r]["failState"]
            while findNext(state, adjacencyList[child]["value"]) == None and state != 0:
                state = adjacencyList[state]["failState"]
            adjacencyList[child]["failState"] = findNext(state, adjacencyList[child]["value"])
            if adjacencyList[child]["failState"] is None:
                adjacencyList[child]["failState"] = 0
            adjacencyList[child]["result"] = adjacencyList[child]["result"] + adjacencyList[adjacencyList[child]["failState"]]["result"]


def findNext(current, value):
    for node in adjacencyList[current]["nextStates"]:
        if adjacencyList[node]["value"] == value:
            return node
    return None


## @fn findTerms
## @param line the character string in which to search for keywords (commands)
## @returns true if line contains any of the keywords in our trie
def findTerms(line):
    line = line.lower()
    current = 0
    foundWords = []
    
    for i in range(len(line)):
        while findNext(current, line[i]) is None and current != 0:
            current = adjacencyList[current]["failState"]
        current = findNext(current, line[i])
        if current is None:
            current = 0
        else:
            for j in adjacencyList[current]["result"]:
                foundWords.append({"index":i-len(j) + 1,"term":j})
    return foundWords
