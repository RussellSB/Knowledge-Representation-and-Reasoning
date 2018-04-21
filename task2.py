"""
Task 2: Construction and Reasoning with Inheritence Networks
"""

import random  # used for choosing random pivot

# class for node, stores name as an attribute
class Node:

    def __init__(self, name=""):
        self.name = name

# class for edge, stores nodeA and nodeB and whether the polarity of the relation from A to B is True or False
class Edge:

    def __init__(self):
        self.nodeA = None
        self.nodeB = None
        self.polarity = None

    def add_A(self, nodeA):
        self.nodeA = nodeA

    def add_B(self, nodeB):
        self.nodeB = nodeB

    def polarity(self, polarity):
        self.polarity = polarity


# class for path, stores list of nodeNames to indicate edges, and stores whether of type IS-A all throughout, or IS-NOT-A
class Path:

    def __init__(self, pathList, type):
        self.pathList = pathList  # stores list of nodeNames
        self.type = type  # stores True for IS-A all through out, False for IS-NOT-A at the end
        self.len = len(pathList)  # stores length of pathList


# method for parsing from text file to objects that make an Inheritence Network
def textToKnowledgeBase(fileName):

    path = []  # stores a sequence of edges in object form

    print "Scanning text file: \"%s\"\n--------\n" % fileName

    # opens file
    f = open(fileName, "r")

    # loop while character retrieval is true
    while 1:

        ch = f.read(1)  # reads 1 character from the file
        if not ch: break  # breaks when no longer holds true

        if (ch == '\n'):
            tempE = Edge()  # initialize new temporary edge

        elif (ch == '<'):
            tempN = Node()  # initialize new temporary node
            flag = 1  # flag set to 1 to indicate alphanumerics used for node name

        elif (ch == '>'):

            if (tempE.nodeA == None):

                tempE.add_A(tempN)  # add tempNode as A since A is not filled

                tempR = ""  # temporary relation string used for storing IS-A or IS-NOT-A
                flag = 0  # flag set to 0 to indicate alphanumerics used for polarity of relation

            else:

                tempE.add_B(tempN)  # add tempNode as B since A is already filled

                if(tempR == ' IS-A '):
                    tempE.polarity = True  # set polarity to True as "IS-A"
                elif(tempR == ' IS-NOT-A '):
                    tempE.polarity = False  # set polarity to False as "IS-NOT-A"

                path.append(tempE)  # appends edge as at the end of the line

                print "%s --%s--> %s\n"%(tempE.nodeA.name, tempE.polarity, tempE.nodeB.name)

        else:   # when another character (mostly alphanumeric)

            if (flag == 1):
                tempN.name += ch  # concatenates character to node string name
            if (flag == 0):
                tempR += ch  # concatenates character to tempR String

    print "--------\nKnowledge Base has been constructed.\n\n"

    return path  # returns list of edges with their corresponding nodes and relations


# method for requesting and parsing a query into an edge
def requestQuery():

    queryString = raw_input("Please input a query edge to search all paths from the Knowledge Base: ")
    print ""  # skips a line

    queryE = Edge()  # initialized query edge object

    # parses queryString, storing all the information in an object clause "queryC"
    for ch in queryString:

        if (ch == '<'):
            tempN = Node()  # initialize new temporary node
            flag = 1  # flag set to 1 to indicate alphanumerics used for node name

        elif (ch == '>'):

            if (queryE.nodeA == None):

                queryE.add_A(tempN)  # add tempNode as A since A is not filled

                tempR = ""  # temporary relation string used for storing IS-A or IS-NOT-A
                flag = 0  # flag set to 0 to indicate alphanumerics used for polarity of relation

            else:

                queryE.add_B(tempN)  # add tempNode as B since A is already filled

                if(tempR == ' IS-A '):
                    queryE.polarity = True  # set polarity to True as "IS-A"
                elif(tempR == ' IS-NOT-A '):
                    queryE.polarity = False  # set polarity to False as "IS-NOT-A"

        else:  # when another character (mostly alphanumeric)

            if (flag == 1):
                tempN.name += ch  # concatenates character to node string name
            if (flag == 0):
                tempR += ch  # concatenates character to tempR String

    return queryE

# method for printing path, being a list of nodeNames
def printPath(tempPath, type):

    if (type == True):

        # prints path contents with IS-A at the end
        for i in range(len(tempPath)):

            # when i is at the last node in the path
            if (i == len(tempPath) - 1):
                print "%s" % tempPath[i]
            else:
                print "%s IS-A" % (tempPath[i]),

    else:

        # prints path contents with IS-NOT-A at the end
        for i in range(len(tempPath)):

            # when i is at the last node in the path
            if (i == len(tempPath) - 1):
                print "%s" % tempPath[i]

            # when i is at the one before the last node in the path
            elif (i == len(tempPath) - 2):
                print "%s IS-NOT-A" % (tempPath[i]),

            else:
                print "%s IS-A" % (tempPath[i]),



# method for resolving query by searching for all possible paths in knowledgeBase, returns successful paths
def searchAll(knowledgeBase, query):

    currNode = query.nodeA  # sets currNode as nodeA
    endNode = query.nodeB  # set endNode as nodeB

    flag = 0  # flag used for detecting previous edge's relations - 0: IS-A, 1: IS-NOT-A

    tempPath = []  # list to append string nodes names to to describe the path

    pathObjList = [] # path list to store successful object paths

    print "Searching for all possible paths:\n-------\n"

    _searchAll(knowledgeBase, currNode, endNode, flag, tempPath, pathObjList)  # calls recursive function

    print "\n-------\nAll possible paths have been searched.\n\n"

    return pathObjList


def _searchAll(knowledgeBase, currNode, endNode, flag, tempPath, pathObjList):

    # base case: for when last node is reached
    if(currNode.name == endNode.name and flag == 0):

        tempPath.append(currNode.name)  # appends to List
        succPath = []  # temporary arrayList to store successful path

        # appends each nodeName to succPath to avoid pointer interference
        for nodeName in tempPath:
            succPath.append(nodeName)

        path = Path(succPath, True)
        pathObjList.append(path)  # appends path to pathList with IS-A

        printPath(succPath, True)  # prints current successful path

        tempPath.remove(currNode.name)  # removes currNode from list

    # base case: the last step it allows "IS-NOT-A" when flag=1
    elif(currNode.name == endNode.name and flag == 1):

        tempPath.append(currNode.name)  # appends to List
        succPath = []  # temporary arrayList to store successful path

        # appends each nodeName to succPath to avoid use of pointers
        for nodeName in tempPath:
            succPath.append(nodeName)

        path = Path(succPath, False)
        pathObjList.append(path)  # appends path to pathList with IS-NOT-A

        printPath(succPath, False)  # prints current successful path

        tempPath.remove(currNode.name)  # remove currNode from list

    # traverses through all edges in knowledgeBase
    for edge in knowledgeBase:

        # if match is found and relation is "IS-A", with previous Relation "IS-A"
        if (edge.nodeA.name == currNode.name and edge.polarity == True and flag == 0):

            tempPath.append(currNode.name)  # append to pathList
            currNodeClone = edge.nodeB  # set currNodeClone to nodeB

            _searchAll(knowledgeBase, currNodeClone, endNode, 0, tempPath, pathObjList)

            tempPath.remove(currNode.name)  # remove currNode when backtracking out of the depths

        # if match is found and relation is "IS-NOT-A", with previous Relation "IS-A"
        elif (edge.nodeA.name == currNode.name and edge.polarity == False and flag == 0):

            tempPath.append(currNode.name)  # append to pathList
            currNodeClone = edge.nodeB  # set currNodeClone to nodeB

            _searchAll(knowledgeBase, currNodeClone, endNode, 1, tempPath, pathObjList)

            tempPath.remove(currNode.name)  # remove currNode when backtracking of the depths


# recursive method for sorting paths by length using quick sort
def sortByLength(objList):

    #base case for when segment's length is less than or equal to one
    if(len(objList)<=1):
        return objList

    smaller = []  # initialized for storing the smaller segment of the list
    equivalent = []  # initialized for storing the element at the pivot
    greater = []  # initialized for storing the greater segment of the list

    #randomly chosen pivot selected from list of paths
    pivot = objList[random.randint(0, len(objList)-1)]

    #for loop to go through the list of paths
    for x in objList:

        #when x is less, append to smaller segment
        if(x.len < pivot.len):
            smaller.append(x)

        #when x is at the pivot, store element into equivalent
        elif(x.len==pivot.len):
            equivalent.append(x)

        #when x is greater, append to greater segment
        elif(x.len > pivot.len):
            greater.append(x)

        else:
            print("An unknown error has occurred during sorting by Path")

    #recursively calls method to work on the smaller and greater segment, then returns on backtracking
    return sortByLength(smaller) + equivalent + sortByLength(greater)


def shortestPath(pathObjList):

    print "Preferred by shortest distance metric:\n-------"

    pathObjList_S = sortByLength(pathObjList)  # sorted path object list

    for i in range(len(pathObjList)):

        # if next path is also the shortest, print current then move on to that to print also
        if(pathObjList_S[i].len == pathObjList_S[i+1].len):

            if(pathObjList_S[i].type == True):
                printPath(pathObjList_S[i].pathList, True)  # prints path with IS-A

            else:
                printPath(pathObjList_S[i].pathList, False)  # prints path with IS-NOT-A

        # when at the last shortest path, print last path then break the loop
        else:

            if (pathObjList_S[i].type == True):
                printPath(pathObjList_S[i].pathList, True)  # prints path with IS-A

            else:
                printPath(pathObjList_S[i].pathList, False)  # prints path with IS-NOT-A

            break


def inferentialPath(pathList):

    print "TO DO ;)"


edgeList = textToKnowledgeBase("inheritanceNetwork.txt")
query = requestQuery()  # requests for user input then parses user input into a query horn clause
pathObjList = searchAll(edgeList, query)
shortestPath(pathObjList)
inferentialPath(pathObjList)


