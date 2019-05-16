import pandas
import numpy

class KNN():

    def __init__(self,x_train,y_train,K):
        self.x_train = x_train.values
        self.y_train = y_train.values
        self.K = K

    def getDistance(self,row,x_tt):
        return sum([abs(x_t-r)**2  for x_t,r in zip(x_tt,row)])

    def getClass(self,disvec):
        res = numpy.argsort(disvec)[:self.K]
        cl = [0]*11
        for r in res :
            cl[self.y_train[r]]+=1
        return numpy.argmax(cl)

    def predict(self,row):
        dis_vec = []
        for x_tt in self.x_train:
            dis_vec.append(self.getDistance(row,x_tt))
        return self.getClass(dis_vec)

    def getTestAccuray(self,x_test,y_test):
        i=0
        x_test=x_test.values
        y_test=y_test.values

        for x,y in zip(x_test,y_test):
            p = self.predict(x)
            if(p == y) :
                i+=1
        return str((i/len(x_test))*100)+"%"

bestK = [0,12,49,2,4,42,36,3,9]
for i in range(1,9):
    data = pandas.read_csv('IS4'+str(i)+'.csv')
    x_train = data.iloc[:80, :26]
    y_train = data.iloc[:80, 26]
    x_test = data.iloc[80:, :26]
    y_test = data.iloc[80:, 26]
    knn = KNN(x_train,y_train,bestK[i])
    print("Accuracy for "+ str(i) +" file "+knn.getTestAccuray(x_test,y_test))


'''
#8 -> 9 -> 58%
#7 -> 3 -> 84%
#6 -> 36 -> 58%
#5 -> 42 -> 63%
#4 -> 4 -> 52%
#3 -> 2 -> 52%
#2 -> 49 -> 57%
#1 -> 12 -> 79%

IS42	DATA COMMUNICATIONS	
IS41	ENGINEERING MATHEMATICS-IV	
IS43	SOFTWARE ENGINEERING	
IS44	DESIGN & ANALYSIS OF ALGORITHMS
IS45	MICROPROCESSORS	
IS46	FINITE AUTOMATA & FORMAL LANGUAGES	
ISL47	DESIGN & ANALYSIS OF ALGORITHMS LABORATORY	
ISL48	MICROPROCESSORS LABORATORY
'''