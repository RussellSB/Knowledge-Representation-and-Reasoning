"""
Task 1: Parsing of Horn Clauses, and Reasoning using Back-Chaining
"""

# class for literal objects
class Literal:

    # initializes the literal object
    def __init__(self, name="", polarity=True):
        self.name = name # Contains the String name of the literal
        self.polarity = polarity  # Whether literal is true or false


# class hornClause for storing clause as an object
class HornClause:

    # stores list of clauses
    def __init__(self):
        self.literalList = []

    def addLiteral(self, literal):
        self.literalList.append(literal)


# method that parses text file, and from which it produces a list of horn clauses called "formula"
def textToKnowledgeBase(fileName):

    formula = []  # stores list of clauses, that in turn stores literals

    print "Scanning text file: \"%s\"\n--------\n"%fileName

    # opens file
    f = open(fileName,"r")

    # loop while character retrieval is true
    while 1:

        ch = f.read(1)  # reads 1 character from the file
        if not ch: break  # breaks when no longer holds true

        if(ch == '['):
            queryC = HornClause()  # initialize new temporary horn clause
            tempL = Literal()  # initialize new temporary literal

        elif (ch == '!'):
            tempL.polarity = False  # sets boolean value to false

        elif (ch == ','):
            queryC.addLiteral(tempL)   # add finished literal to object
            tempL = Literal()  # initialize new temporary literal

        elif (ch == ']'):
            queryC.addLiteral(tempL)  # add finished literal to object
            formula.append(queryC)   # append finished object to list

        elif (ch == '\n'):

            pass  # condition used to catch '\n' so it doesn't get detected as alphanumeric and put in name attribute

            for i in range(len(queryC.literalList)): # loops through whole literalList of current finished clause
                print "%s, %s"%(queryC.literalList[i].polarity,queryC.literalList[i].name)  # prints True/False, and name

            print ""  # skips line for next clause


        elif (ch.isalpha):
            tempL.name += ch   # concatenates character to literal string name

        else:
            print "Error: unrecognized character in text file \"%s\""%fileName

    print "--------\nKnowledge base has been loaded.\n"

    return formula  # returns list of horn clauses


# method to parse string query to clause object, to later be used for SLD back-chaining
def requestQuery():

    queryString = raw_input("Please input a query clause to resolve from the Knowledge Base (Use ! for negation): ")
    print ""  # skips a line

    # parses queryString, storing all the information in an object clause "queryC"
    for ch in queryString:

        if (ch == '['):
            queryC = HornClause()  # initialize query horn clause
            tempL = Literal()  # initialize new temporary literal

        elif (ch == '!'):
            tempL.polarity = False  # sets boolean value to false

        elif (ch == ','):
            queryC.addLiteral(tempL)  # add finished literal to object
            tempL = Literal()  # initialize new temporary literal

        elif (ch == ']'):
            queryC.addLiteral(tempL)  # add finished literal to object

        elif (ch.isalpha):
            tempL.name += ch  # concatenates character to literal string name

        else:
            print "Error: unrecognized character in user input string \"%s\"\n" % queryString

    return queryC


# recursive method that returns whether the query is solvable or unsolvable
def _resolve(knowledgeBase, query):

    # checks if query list at current depth is empty, if it is then the query is solved
    if(len(query.literalList)==0):
        print"Empty List: %s"%query.literalList
        print "SOLVED"
        return True

    # traverses through clauses in the knowledgeBase
    for clause in knowledgeBase:

        # traverses through literals in clause
        for literal in clause.literalList:

                # checks whether same literal as last literal in query is found, with opposite polarity
                if (literal.name == query.literalList[-1].name) and (literal.polarity != query.literalList[-1].polarity):

                    # for printing out match with clause from knowledge base with clause from query
                    print"Match found : [",

                    for literal in clause.literalList:

                        if (literal.polarity == True):  # checks whether to print '!' for negation
                            print"%s"%literal.name,
                        else:
                            print"!%s" % literal.name,

                    print "] with Query [",

                    for literal in query.literalList:

                        if (literal.polarity == True):  # checks whether to print '!' for negation
                            print"%s"%literal.name,
                        else:
                            print"!%s" % literal.name,

                    print "]"

                    # when query has one literal
                    if(len(query.literalList)==1):

                        clauseClone = clause
                        clauseClone.literalList.remove(clauseClone.literalList[-1])  # removes the last element of the clauseClone
                        _resolve(knowledgeBase, clauseClone)  # recursively calls itself with the clauseClone as a query

                        return True  # returns True for when it backtracks

                    # when query has more than one literal
                    elif(len(query.literalList)>1):

                        clauseClone = query
                        clauseClone.literalList.remove(
                            clauseClone.literalList[-1])  # removes the last element of the clauseClone
                        _resolve(knowledgeBase, clauseClone)  # recursively calls itself with the clauseClone as a query

                        return True  # returns True for when it backtracks


    # goes through all clauses and finds no literal matches, therefore query is not solved
    print "NOT SOLVED"
    return False


hcFormula = textToKnowledgeBase("clauseStatements.txt")   # stores all the clauses from "clauseStatements.txt" into hcFormula
query = requestQuery()  # requests for user input then parses user input into a query horn clause
_resolve(hcFormula, query)  # resolves query with knowlegeBase



