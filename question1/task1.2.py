#Name: Russell Sammut-Bonnici
#Date: Apr 11 2018
#Unit: ICS1019

def parseTextInput(fileName):

    clauseList = [] #initialized list for storing clauses line by line

    #reads file line by line, stores each clause statement in clauseList
    with open(fileName) as f:
        clauseList = f.readlines()
        f.close()

    #
    for clause in clauseList:


    print clauseList[2]

fileName = "clauseStatements.txt"
parseTextInput(fileName)