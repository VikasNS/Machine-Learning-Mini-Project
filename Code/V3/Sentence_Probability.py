from keras.models import Sequential
from keras.layers import Bidirectional,LSTM,Dense,Embedding,TimeDistributed
from keras.optimizers import rmsprop
from sklearn.utils import shuffle
from numpy import array
from keras.callbacks import Callback
import pickle
from keras.utils import to_categorical
class cus_call(Callback):
    def __init__(self, model):
        super().__init__()
        self.model=model
        self.i=0
    def on_epoch_end(self, epoch, logs=None):
        model.save_weights('Sentence_Probability')


def cus_gen(X,batch_size):
    while 1:
        X= shuffle(X)
        for i in range(len(X)//batch_size):
            X_final=[]
            y_final=[]
            for line in X[i * batch_size:(i + 1) * batch_size]:
                X_final.append(line[:-1])
                y_final.append(to_categorical(line[1:],num_classes=733))
            yield (array(X_final),array(y_final))

with open('X','rb') as X:
    X=pickle.load(X)

optimizer=rmsprop()
model=Sequential()
model.load_weights('Sentence_Probability')

c=cus_call(model)
model.add(Embedding(input_dim=733,output_dim=40,input_length=21))
model.add(LSTM(units=200,activation='relu',return_sequences=True))
model.add(LSTM(units=500,activation='relu',return_sequences=True))
model.add(TimeDistributed(Dense(733,activation='softmax')))
model.compile(optimizer=optimizer,loss='cosine_proximity',metrics=['acc'])
model.fit_generator(generator=cus_gen(X,32),steps_per_epoch=(5000),epochs=100,callbacks=[c])
