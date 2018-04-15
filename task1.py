# class for literal objects
class Literal:

    # initializes the literal object
    def __init__(self, name="", bool=True):
        self.name = name # Contains the String name of the literal
        self.bool = bool  # Whether literal is true or false


# class hornClause for storing clause as an object
class HornClause:

    # stores list of clauses
    def __init__(self):
        self.literalList = []

    def addLiteral(self, literal):
        self.literalList.append(literal)


# method that parses text file, and from which it produces a list of horn clauses called "clauseList"
def textToClauses(fileName):

    clauseList = []  # stores list of clauses, that in turn stores literals

    # opens file
    f = open(fileName,"r")

    # loop while character retrieval is true
    while 1:

        ch = f.read(1)  # reads 1 character from the file
        if not ch: break  # breaks when no longer holds true

        if(ch == '['):
            tempC = HornClause()  # initialize new temporary horn clause
            tempL = Literal()  # initialize new temporary literal

        elif (ch == '!'):
            tempL.bool = False  # sets boolean value to false

        elif (ch == ','):
            tempC.addLiteral(tempL)   # add finished literal to object
            tempL = Literal()  # initialize new temporary literal

        elif (ch == ']'):
            tempC.addLiteral(tempL)  # add finished literal to object
            clauseList.append(tempC)   # append finished object to list

        elif (ch == '\n'):

            pass  # condition used to catch '\n' so it doesn't get detected as alphanumeric and put in name attribute

            ''' UNCOMMENT TO PRINT CONTENTS PER CLAUSE
            for i in range(len(tempC.literalList)): # loops through whole literalList of current finished clause
                print "%s, %s"%(tempC.literalList[i].bool,tempC.literalList[i].name)  # prints True/False, and name

            print ""  # skips line for next clause
            '''

        elif (ch.isalpha):
            tempL.name += ch   # concatenates character to literal string name

    return clauseList  # returns list of horn clauses


hcList = textToClauses("clauseStatements.txt")   # stores all the clauses from "clauseStatements.txt" into hcList