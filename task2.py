"""
Task 2: Construction and Reasoning with Inheritence Networks
"""

import random  # used for choosing random pivot in quick sort

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


# class for path, stores list of edges, and stores whether of type IS-A all throughout, or IS-NOT-A
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

                    # prompt user that IS-NOT-A is not valid for query
                    print "Error: IS-NOT-A not valid for querying, set as IS-A"
                    queryE.polarity = True  # set polarity to True as "IS-A"

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

    _searchAll(knowledgeBase, currNode, endNode, flag, tempPath, pathObjList)  # calls recursive function

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

    # base case: the last step it allows "IS-NOT-A" when flag=1
    elif(currNode.name == endNode.name and flag == 1):

        succPath = []  # temporary arrayList to store successful path

        # appends each nodeName to succPath to avoid use of pointers
        for edge in tempPath:
            succPath.append(edge)

        path = Path(succPath, False)  # sets path object to succPath, polarity False
        pathObjList.append(path)  # appends path to pathList with IS-NOT-A

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

            tempPath.remove(edge)  # remove current edge when backtracking out of the depths


# recursive method for sorting path objects by length using quick sort
def sortByLength(objList):

    # base case for when segment's length is less than or equal to one
    if (len(objList) <= 1):
        return objList

    smaller = []  # initialized for storing the smaller segment of the list
    equivalent = []  # initialized for storing the element at the pivot
    greater = []  # initialized for storing the greater segment of the list

    # randomly chosen pivot selected from list of paths
    pivot = objList[random.randint(0, len(objList) - 1)]

    for x in objList:

        # when x is less, append to smaller segment
        if (x.len < pivot.len):
            smaller.append(x)

        # when x is at the pivot, store element into equivalent
        elif (x.len == pivot.len):
            equivalent.append(x)

        # when x is greater, append to greater segment
        elif (x.len > pivot.len):
            greater.append(x)

        else:
            print("An unknown error has occurred during sorting by Path")

        # recursively calls method to work on the smaller and greater segment, then returns on backtracking
    return sortByLength(smaller) + equivalent + sortByLength(greater)


# method for printing back the shortest path/s from all possible paths
def shortestPath(pathObjList):

    shortestPaths = []  # initialized list to store shortest path/s

    sortedPaths = sortByLength(pathObjList)  # sorts path object list by their lengths

    shortestPaths.append(sortedPaths[0])  # appends shortest path to shortestPaths list

    # goes through paths in sortedPaths, to check for other shortestPaths (starts from i=1)
    for i in range(1, len(sortedPaths)):

        # if next path is also shortest like the previous one
        if(sortedPaths[i].len == sortedPaths[i-1].len):

            shortestPaths.append(sortedPaths[i])  # append to list

        # if not one of the shortest, stop looping and break
        else:
            break

    return shortestPaths


# method for printing back inferential path from all possible paths, uses knowledgeBase to test redundancy
def inferentialPath(pathObjList, knowledgeBase):

    infPaths = pathObjList  # inferential Paths starts as pathObjList, preempted and redundant paths are then eliminated
    currQuery = Edge()  # initializes query as empty

    '''
    
        REDUNDANCY CHECK
    
        Goes through all possible paths checking for redundancy.
        This method works by eliminating the redundant paths in infPaths.

        It queries the knowledgeBase for subPaths from the beginning of each path,
        to the next node after it, this nodeB keeps on incrementing by one to check
        for longer subPaths each time.

        When more than one possible subPath is found for the query, the shortest
        path/s of the subPaths is/are found and are eliminated from the infPaths list
        as they are considered redundant when compared to the other longer and therefore
        more informative lists.

    '''

    # goes through paths in infPaths for removing redundant paths
    for path in infPaths:

        #  print "\n+In new path"

        currQuery.add_A(path.pathList[0].nodeA)  # sets nodeA in query to first node in paths
        i = 1  # sets counter for going through edges after startNode to 1
        flag = 0  # flag used to detect when the path is removed, stops looping when 1 as path is deleted

        # goes through edges in path list, starting from the second edge (ignores last node)
        while (i <= path.len and flag==0):

            if (i == path.len):  # when at last index

                currQuery.add_B(path.pathList[i-1].nodeB)  # sets nodeB as last node in path on the last iteration

            else:  # when not at last index

                currQuery.add_B(path.pathList[i].nodeA)  # sets nodeB as next node every iteration

            subPaths = searchAll(knowledgeBase, currQuery)  # returns all possible subPaths for current query

            # if more than one possible path is found, find redundant/shortest paths and eliminate them
            if (len(subPaths) > 1):

                shortestSubs = shortestPath(subPaths)  # finds shortest path/s from possible paths and stores in list

                #  print ""

                # goes through shortest subPaths in shortestSubs list
                for shortSub in shortestSubs:

                    # goes through redundant edges in shortSub.pathList
                    for shortEdge in shortSub.pathList:

                        # goes through paths in infPaths
                        for path in infPaths:

                            # goes through edges in path.pathLists
                            for edge in path.pathList:

                                if (shortEdge == edge):
                                    #  print "REMOVING PATH"
                                    #  printPath(path)
                                    #  print ""
                                    infPaths.remove(path)  # removes path with redundant edge
                                    flag = 1  # sets flag to 1 to indicate the path's deletion

            i += 1  # increments the counter

    #  print "==INF SURVIVORS:== after redundancy check"
    #  for path in infPaths:
    #    printPath(path)

    '''
    
        PREEMPTION CHECK
    
        Goes through all paths checking for preemption.
        This method works by eliminating the preemptive paths in infPaths.

        It queries the knowledgeBase for subPaths that have an alternative path
        to the last edge in a False path (path that have IS-NOT-A at the end.
            
        It then removes all the positive alternative paths, allowing for negative
        paths with IS-NOT-A at the end to overrule their positive alternatives
        with IS-A all throughout.

    '''

    # goes through paths in infPaths for removing preemptive paths
    for path in infPaths:

        #  print "\n+In new path"

        # if path type has IS-NOT-A at the end
        if path.type == False:

            currQuery.add_A(path.pathList[-1].nodeA)  # sets nodeA as nodeA from last edge in negative pathList
            currQuery.add_B(path.pathList[-1].nodeB)  # sets nodeB as nodeB from last edge in IS-NOT-A path

            subPaths = searchAll(knowledgeBase, currQuery)  # searches for all possible subPaths alt. to this edge

            # if alternative sub paths are found and are positive, eliminate them
            if(len(subPaths) > 1):

                # traverses through subPaths from the subPath list
                for subPath in subPaths:

                    # when alternative subPath is seen to be True, having IS-A all throughout
                    if subPath.type == True:

                        for subEdge in subPath.pathList:

                            for path in infPaths:

                                for edge in path.pathList:

                                    if (subEdge == edge):
                                        #  print "REMOVING"
                                        #  printPath(path)
                                        #  print ""
                                        infPaths.remove(path)  # removes path that is redundant

    #  print "==INF SURVIVORS:== after preemption check"
    #  for path in infPaths:
    #    printPath(path)

    return infPaths  # returns the survivors of the inferentialPaths list


knowledgeBase = textToKnowledgeBase("inheritanceNetwork.txt")  # converts text to knowledgeBase
query = requestQuery()  # request user for string query then stores it in an edge object


pathObjList = searchAll(knowledgeBase, query)  # searches for all possible paths posed by the query

print "All possible paths:\n-------"  # prints all the possible paths from pathObjList
for possiblePath in pathObjList:
    printPath(possiblePath)

shortestPathList = shortestPath(pathObjList)  # returns preferred path/s by shortest distance metric

print "\n\nPreferred by shortest distance metric:\n-------"  # prints all shortest paths from shortestPathList
for shortest in shortestPathList:
    printPath(shortest)

infPathList = inferentialPath(pathObjList, knowledgeBase)  # shows preferred path if any by inferential distance metric

print "\n\nPreferred by inferential distance metric:\n-------"
for inferential in infPathList:
    printPath(inferential)
