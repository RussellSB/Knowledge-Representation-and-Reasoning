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

    print "--------\nKnowledge Base has been constructed.\n"

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


# method for resolving query by searching for all possible paths in knowledgeBase
def searchAll(knowledgeBase, query):

    currNode = query.nodeA  # sets node1 as nodeA
    endNode = query.nodeB  # set endPoint as nodeB

    flag = 0  # flag used for detecting previous edge's relations - 0: IS-A, 1: IS-NOT-A

    tempPath = []  # list to append nodes names to to describe the path

    print "Searching for all possible paths:\n-------\n"

    _searchAll(knowledgeBase, currNode, endNode, flag, tempPath)  # calls recursive function

    print "\n-------"

def _searchAll(knowledgeBase, currNode, endNode, flag, tempPath):

    # base cases for when last node is reached
    if(currNode.name == endNode.name and flag == 0):

        tempPath.append(currNode.name) # appends to List

        # prints path contents with IS-A at the end
        for i in range(len(tempPath)):

            # when i is at the last node in the path
            if(i == len(tempPath)-1):
                print "%s"%tempPath[i]
            else:
                print "%s IS-A" % (tempPath[i]),

        tempPath.remove(currNode.name)  # removes currNode from list

    # since its the last step it allows "IS-NOT-A" when flag=1
    elif(currNode.name == endNode.name and flag == 1):

        tempPath.append(currNode.name)  # appends to List

        # prints path contents with IS-NOT-A at the end
        for i in range(len(tempPath)):

            # when i is at the last node in the path
            if (i == len(tempPath)-1):
                print "%s" % tempPath[i]

            # when i is at the one before the last node in the path
            elif(i == len(tempPath)-2):
                print "%s IS-NOT-A" % (tempPath[i]),

            else:
                print "%s IS-A" % (tempPath[i]),

        tempPath.remove(currNode.name)  # removes currNode from list

    # traverses through all edges in knowledgeBase
    for edge in knowledgeBase:

        # if match is found and relation is "IS-A", with previous Relation "IS-A"
        if (edge.nodeA.name == currNode.name and edge.polarity == True and flag == 0):

            tempPath.append(currNode.name)  # append to pathList
            currNodeClone = edge.nodeB  # set currNodeClone to nodeB

            _searchAll(knowledgeBase, currNodeClone, endNode, 0, tempPath)

            tempPath.remove(currNode.name)  # remove currNode when back-chaining

        # if match is found and relation is "IS-NOT-A", with previous Relation "IS-A"
        elif (edge.nodeA.name == currNode.name and edge.polarity == False and flag == 0):

            tempPath.append(currNode.name)  # append to pathList
            currNodeClone = edge.nodeB  # set currNodeClone to nodeB

            _searchAll(knowledgeBase, currNodeClone, endNode, 1, tempPath)

            tempPath.remove(currNode.name)  # remove currNode when back-chaining


edgeList = textToKnowledgeBase("inheritanceNetwork.txt")
query = requestQuery()  # requests for user input then parses user input into a query horn clause
searchAll(edgeList, query)


