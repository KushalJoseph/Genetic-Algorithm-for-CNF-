import random
import itertools
import csv


class CNF_Creator:
    def __init__(self,n): #n is number of symbols
        self._n = n
        self._sentence = None

    def _CreateAClause(self):
        n = self._n
        claus = random.sample(range(1,n+1),3)
        for i in range(3):
            claus[i] = -claus[i] if random.choice(range(2))==0 else claus[i]
            #above statement randomly negates some of the literals in the clause
        claus.sort()
        return claus

    def CreateRandomSentence(self,m): #m is number of clauses in the sentence
        n = self._n
        clauses = list()
        while len(clauses)<m:
            for mi in range(len(clauses),m):
                claus = self._CreateAClause()
                clauses.append(claus)
            clauses.sort()
#            print(clauses,len(clauses))
            clauses = list(clause for clause,_ in itertools.groupby(clauses)) # removes duplicate clauses
#            print(clauses,len(clauses))
            self._sentence = clauses
        return self._sentence
    
    
    def ReadCNFfromCSVfile(self):
        with open('CNF.csv') as csvfile:
            rows = csv.reader(csvfile)
            rows = list(rows)
        sentence = [[int(i) for i in ro] for ro in rows]
        return sentence
    

def main():
    cnfC = CNF_Creator(n=50) # n is number of symbols 
    sentence = cnfC.CreateRandomSentence(m=350) # m is number of clauses in the sentence
    print(len(sentence))

    sentence = cnfC.ReadCNFfromFile()
    print(len(sentence))
    

if __name__=='__main__':
    main()
