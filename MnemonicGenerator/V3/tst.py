import pickle
import nltk
from collections import Counter,defaultdict
from nltk import trigrams
from itertools import permutations
from math import log10

def find_prob(grams,model):
    grams = trigrams(temp_sentence)

    prob = 0
    for m, gram in enumerate(grams):
        tri=model[(gram[0],gram[1])][gram[2]]
        bi=sum(model[(gram[0],gram[1])].values())
        if (tri > 0):
            prob += log10(tri)



    return prob



with open('X','rb') as input_file:
    X=pickle.load(input_file)

count_all=0
count_extra=0

model=defaultdict(lambda : defaultdict(lambda : 0))

for line in X:
    for w1,w2,w3 in trigrams(line):
        model[(w1,w2)][w3]+=1

for w1_w2 in model:
    total_count=float(sum(model[w1_w2].values()))
    for w3 in model[w1_w2]:
        model[w1_w2][w3]/=total_count

final_test = []
for k,case in enumerate([[394, 502, 130, 229, 568]]):
    p = permutations(case)
    max = -999
    best = []
    for j,one_comb in enumerate(p):
        print(k,j)
        i = 0
        temp_sentence = [730, 730]
        for word in one_comb:
            i += 1
            temp_sentence.append(word)

            if i == len(one_comb):
                temp_sentence += [731, 731]
                for _ in range(24 - len(temp_sentence)):
                    temp_sentence.append(732)
        prob=find_prob(temp_sentence,model)
        if(prob>max):
            max=prob
            best=temp_sentence
    final_test.append(best)

print(best)

with open('trigram_test','wb') as output_file:
    pickle.dump(final_test,output_file)

