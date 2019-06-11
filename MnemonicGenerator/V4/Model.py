import numpy
import os

import random
import pickle
from keras.models import Sequential
from keras.layers import Dense
from keras.layers.embeddings import Embedding
from keras.layers import Bidirectional, LSTM, TimeDistributed
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Dropout
from keras.optimizers import rmsprop, adam
from sklearn.utils import shuffle


def cus_gen(batch_size, X, y):
    while True:
        X, y = shuffle(X, y)
        for i in range(len(X) // batch_size):
            yield (
            numpy.array(X[i * batch_size:(i + 1) * batch_size]), numpy.array(y[i * batch_size:(i + 1) * batch_size]))


optimizer = rmsprop(lr=0.0001)
model = Sequential()
model.add(Embedding(input_dim=733, output_dim=40, input_length=12, name='embedding_1'))
model.add(
    Bidirectional(LSTM(250, return_sequences=True, activation='tanh'), merge_mode='concat', name='bidirectional_1'))
Dropout(0.4)
model.add(
    Bidirectional(LSTM(750, return_sequences=True, activation='tanh'), merge_mode='concat', name='bidirectional_2'))
Dropout(0.4)
model.add(
    Bidirectional(LSTM(500, return_sequences=True, activation='tanh'), merge_mode='concat', name='bidirectional_3'))
Dropout(0.4)
model.add(
    Bidirectional(LSTM(500, return_sequences=True, activation='tanh'), merge_mode='concat', name='bidirectional_4'))
Dropout(0.4)
model.add(TimeDistributed(Dense(400, activation='tanh', name='time_distributed_1')))
model.add(TimeDistributed(Dense(332, activation='tanh', name='time_distributed_2')))
model.compile(loss='cosine_proximity', optimizer=optimizer, metrics=['acc'])

with open('X', 'rb') as X:
    X = pickle.load(X)

with open('y', 'rb') as y:
    y = pickle.load(y)

with open('words', 'rb') as words:
    words = pickle.load(words)
with open('X_test', 'rb') as X_test:
    X_test = numpy.array(pickle.load(X_test))

with open('matrix', 'rb') as matrix:
    matrix = pickle.load(matrix)

from keras.callbacks import Callback


class cus_call(Callback):
    def __init__(self, model, words, matrix, X_test):
        super().__init__()
        self.model = model
        self.words = words
        self.matrix = matrix
        self.X_test = X_test
        self.count = 0


    def on_epoch_end(self, epoch, logs=None):
        self.count += 1
        self.model.save_weights('model_weight')

        if self.count % 5 == 0:
            output = self.model.predict(self.X_test)
            for sentence in output:
                for word in sentence:
                    print(self.words[numpy.argmax(numpy.matmul(self.matrix, word))], end=" ")

                print()



model.load_weights('model_weight', by_name=True)
print("0.3")
call = cus_call(model, words, matrix, X_test)
model.fit_generator(generator=cus_gen(170, X, y), steps_per_epoch=(3000), epochs=100, callbacks=[call])

output = model.predict(X_test)
for sentence in output:
    for word in sentence:
        print(words[numpy.argmax(numpy.matmul(matrix, word))], end=" ")

    print()

