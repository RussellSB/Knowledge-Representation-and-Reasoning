"""
Task 2: Construction and Reasoning with Inheritence Networks
"""


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


# stored nodeNames rather than edges as paths because working with discrete information made things more efficient
# class for path, stores list of nodeNames to indicate edges, and stores whether of type IS-A all throughout, or IS-NOT-A
class Path:

    def __init__(self, pathList, type):
        self.pathList = pathList  # stores list of edges
        self.type = type  # stores True for IS-A all through out, False for IS-NOT-A at the end
        self.len = len(pathList)  # stores length of path (each edge is length 1)


# method for parsing from text file to objects that make an Inheritence Network
def textToKnowledgeBase(fileName):

    edgeList = []  # stores a sequence of edges in object form

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

                edgeList.append(tempE)  # appends edge as at the end of the line

                print "%s --%s--> %s\n"%(tempE.nodeA.name, tempE.polarity, tempE.nodeB.name)

        else:   # when another character (mostly alphanumeric)

            if (flag == 1):
                tempN.name += ch  # concatenates character to node string name
            if (flag == 0):
                tempR += ch  # concatenates character to tempR String

    print "--------\nKnowledge Base has been constructed.\n\n"

    return edgeList  # returns list of edges with their corresponding nodes and relations


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


# method for printing path, being a list of edges
def printPath(path):

    if (path.type == True):

        # prints path contents with IS-A at the end
        for i in range(len(path.pathList)):

            # when i is at the last edge in the path
            if (i == len(path.pathList) - 1):
                print "%s IS-A %s" % (path.pathList[i].nodeA.name, path.pathList[i].nodeB.name)
            else:
                print "%s IS-A" % (path.pathList[i].nodeA.name),

    else:

        # prints path contents with IS-NOT-A at the end
        for i in range(len(path.pathList)):

            # when i is at the last edge in the path
            if (i == len(path.pathList) - 1):
                print "%s IS-NOT-A %s" % (path.pathList[i].nodeA.name, path.pathList[i].nodeB.name)
            else:
                print "%s IS-A" % (path.pathList[i].nodeA.name),


# method for resolving query by searching for all possible paths in knowledgeBase, returns successful paths
def searchAll(knowledgeBase, query):

    currNode = query.nodeA  # sets currNode as nodeA
    endNode = query.nodeB  # set endNode as nodeB

    flag = 0  # flag used for detecting previous edge's relations - 0: IS-A, 1: IS-NOT-A

    tempPath = []  # list to append edges to to describe the path

    pathObjList = []  # path list to store successful object paths

    print "Searching for all possible paths:\n-------\n"

    _searchAll(knowledgeBase, currNode, endNode, flag, tempPath, pathObjList)  # calls recursive function

    print "\n-------\nAll possible paths have been searched.\n\n"

    return pathObjList


def _searchAll(knowledgeBase, currNode, endNode, flag, tempPath, pathObjList):

    # base case: for when last node is reached
    if(currNode.name == endNode.name and flag == 0):

        succPath = []  # temporary arrayList to store successful path

        # appends each edge to succPath to avoid pointer interference
        for edge in tempPath:
            succPath.append(edge)

        path = Path(succPath, True)  # sets path object to to succPath, polarity True
        pathObjList.append(path)  # appends path to pathList with IS-A

        printPath(path)  # prints current successful path

    # base case: the last step it allows "IS-NOT-A" when flag=1
    elif(currNode.name == endNode.name and flag == 1):

        succPath = []  # temporary arrayList to store successful path

        # appends each nodeName to succPath to avoid use of pointers
        for edge in tempPath:
            succPath.append(edge)

        path = Path(succPath, False)  # sets path object to succPath, polarity False
        pathObjList.append(path)  # appends path to pathList with IS-NOT-A

        printPath(path)  # prints current successful path

    # traverses through all edges in knowledgeBase
    for edge in knowledgeBase:

        # if match is found and relation is "IS-A", with previous Relation "IS-A"
        if (edge.nodeA.name == currNode.name and edge.polarity == True and flag == 0):

            tempPath.append(edge)  # append to edge pathList
            currNodeClone = edge.nodeB  # set currNodeClone to nodeB

            _searchAll(knowledgeBase, currNodeClone, endNode, 0, tempPath, pathObjList)

            tempPath.remove(edge)  # remove current edge when backtracking out of the depths

        # if match is found and relation is "IS-NOT-A", with previous Relation "IS-A"
        elif (edge.nodeA.name == currNode.name and edge.polarity == False and flag == 0):

            tempPath.append(edge)  # append edge to pathList
            currNodeClone = edge.nodeB  # set currNodeClone to nodeB

            _searchAll(knowledgeBase, currNodeClone, endNode, 1, tempPath, pathObjList)

            tempPath.remove(edge)  # remove current edge when backtracking of the depths


# method for printing back the shortest path/s from all possible paths
def shortestPath(pathObjList):

    print "Preferred by shortest distance metric:\n-------"

    shortestPaths = [pathObjList[0]]  # list for storing one or more paths of shortest length, starts from the first

    # traverses through paths in pathObjList starting from the second one
    for i in range(1, len(pathObjList)):

        # if current path is less than previous
        if (pathObjList[i].len < pathObjList[i-1].len):

            shortestPaths = []  # clear for new shortest length
            shortestPaths.append(pathObjList[i])  # append new shortest path to shortestPaths list

        # else if current path is the same as previous
        elif (pathObjList[i].len == pathObjList[i-1].len):
            shortestPaths.append(pathObjList[i])  # append same length path to shortestPaths list

    # prints all the shortest paths
    for shortPath in shortestPaths:
        printPath(shortPath)

    return shortestPaths

'''
# method for printing back inferential path from all possible paths
def inferentialPath(pathObjList):

'''

edgeList = textToKnowledgeBase("inheritanceNetwork.txt")  # converts text to knowledgeBase
query = requestQuery()  # request user for string query then stores it in an edge object
pathObjList = searchAll(edgeList, query)  # searches for all possible paths posed by the query
shortestPath(pathObjList)  # shows preferred path/s by shortest distance metric
# inferentialPath(pathObjList)  # shows preferred path if any by inferential distance metric
