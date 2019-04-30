import pickle
from nltk import trigrams
with open('X','rb') as X:
    X=pickle.load(X)

test=X[:10]
trigram=[]
for case in test:
    trigram+=trigrams(case)
from nltk import probability
from nltk import KneserNeyProbDist
gen = KneserNeyProbDist(trigram)
for i in gen.samples():
    print(i)