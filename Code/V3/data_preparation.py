'''
df_50k=pd.read_csv('songdata.csv')
artists_in_50k=set(df_50k.artist)

df_330k=pd.read_csv('lyrics.csv')
artists_in_330k=set(df_330k.artist)

print(df_330k.lyrics.isnull().sum())
'''
import pandas as pd
import string
from nltk import word_tokenize,sent_tokenize
import pickle
import random
import numpy


def read_file(file_name):
   return pd.read_csv(open(file_name, 'rb'))

def clean_tokenize(data_frame,story_file_name,min_len=5,max_len=10):
    data = []
    words_in_data = []
    words_in_embedding = []
    missing_words_in_data = []
    to_delete = "./:;<=>?@[\]^_`{|}~#$%&'()*+,!“”’■—‘🙏�"
    to_delete2 = '"\\'
    to_replace = "-"

    # articles

    files = ['india-news-headlines.csv', 'headlines.csv']
    for l, file in enumerate(files):
        print('Article')
        df = pd.read_csv(file)
        for z, paragraph in enumerate(df.headline_text):
            print(l, z)
            sentences = sent_tokenize(paragraph.lower())
            for sentence in sentences:
                sentence = sentence.strip()
                if (len(sentence) != 0):
                    sentence = sentence.rstrip().strip().translate(str.maketrans('', '', to_delete)).translate(
                        str.maketrans('', '', '1234567890')).translate(str.maketrans('', '', to_delete2)).translate(
                        str.maketrans(to_replace, " "))
                    words = word_tokenize(sentence)
                    if (max_len > len(words) > min_len):
                        data.append(words)
                        words_in_data += words
    # articles

    # #Story
    # paragraph = ""
    # with open(story_file_name, 'rb') as file:
    #     for i, line in enumerate(file):
    #         print("Builiding Paragraph {0:.2f}".format((i * 100) / 1000000))
    #         paragraph = paragraph + " " + line.decode('ascii', 'ignore').lower()
    #
    # sentences = sent_tokenize(paragraph)
    # with open('Big paragraph','wb') as big_para:
    #     pickle.dump(sentences,big_para)
    #
    # for i, sentence in enumerate(sentences):
    #     sentence = sentence.strip()
    #     if (len(sentence) != 0):
    #         print("Cleanig and building sentence ", (i * 100) / len(sentences))
    #         sentence=sentence.rstrip().strip().translate(str.maketrans('', '', to_delete)).translate(
    #                 str.maketrans('', '', '1234567890')).translate(str.maketrans('', '', to_delete2)).translate(
    #                 str.maketrans(to_replace, " "))
    #         words = word_tokenize(sentence)
    #         if (max_len > len(words) > min_len):
    #             data.append(words)
    #             words_in_data += words
    # # Story



    #building data and formation of all words in data
    for c,lines in enumerate(data_frame[:].text):
        if(isinstance(lines,str)):
            lines = lines.split("\n")
            for line in lines:
                line = line.lower().rstrip().strip().translate(str.maketrans('', '', to_delete)).translate(
                    str.maketrans('', '', '1234567890')).translate(str.maketrans('', '', to_delete2)).translate(
                    str.maketrans(to_replace, " "))
                words = word_tokenize(line)
                if (max_len > len(words) > min_len):
                    data.append(words)
                    words_in_data += words
            print('Building sentences', c / 550, "%")

    words_in_data=set(words_in_data)


    #all the words in glove formation
    with open('glove.840B.300d.txt', 'rb') as file:
        for line in file:
            line = line.split()
            words_in_embedding.append(line[0].decode('ascii', 'ignore').lower().strip().translate(str.maketrans('', '', to_delete)).translate(
                str.maketrans('', '', '1234567890')).translate(str.maketrans('', '', to_delete2)).translate(
                str.maketrans(to_replace, " ")))
    words_in_embedding=set(words_in_embedding)

    #missing words list formation
    for i, word in enumerate(words_in_data):
        if word not in words_in_embedding:
            missing_words_in_data.append(word)
    missing_words_in_data=set(missing_words_in_data)



    return data,words_in_data,words_in_embedding,missing_words_in_data


def remv_sent_with_missing_words_add_start_end(data, missing_words_in_data,is_test):
    final_data = []
    words_in_data=[]

    for c,sentence in enumerate(data):
        i = 0
        temp_sentence=['<<']
        for word in sentence:
            i += 1

            if(is_test):
                temp_sentence.append(word)
            else:
                if word in missing_words_in_data:
                    break
                else:
                    temp_sentence.append(word)

            if i == len(sentence):
                temp_sentence+=['>>']
                for _ in range(22-len(temp_sentence)):
                    temp_sentence.append('--')
                final_data.append(temp_sentence)
        print("rEMOVING sentences",c/len(data))

    if(is_test):
        return final_data


    for c,sentence in enumerate(final_data):
        words_in_data+=sentence


    return final_data,set(words_in_data)

def build_embedding_dic(words_in_data):
    print('BUIDING EMBEDING STARTED')

    to_delete = "./:;<=>?@[\]^_`{|}~#$%&'()*+,!"
    to_delete2 = '"'
    to_replace = "-"
    word_to_vec=dict()
    with open('glove.840B.300d.txt', 'rb') as file:
        for line in file:
            line = line.split()
            word=(line[0].decode('ascii', 'ignore').lower().strip().translate(str.maketrans('', '', to_delete)).translate(
                str.maketrans('', '', '1234567890')).translate(str.maketrans('', '', to_delete2)).translate(
                str.maketrans(to_replace, " ")))
            vec = line[1:]
            if word in words_in_data:
                vec = [float(unit_vec.decode('ascii', 'ignore')) for unit_vec in vec]
                word_to_vec[word] = vec
        print('BUIDING EMBEDING ENDED')

    return word_to_vec

def append_orthogonals_add_extras(word_to_vec):
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', '<' , '>' , '-']

    arr =[[+1, +1, +1, +1, +1, +1, +1, +1, +1, +1, +1, +1, +1, +1, +1, +1, +1, +1, +1, +1, +1, +1, +1, +1, +1, +1, +1, +1, +1, +1, +1, +1],
         [+1, -1, +1, -1, +1, -1, +1, -1, +1, -1, +1, -1, +1, -1, +1, -1, +1, -1, +1, -1, +1, -1, +1, -1, +1, -1, +1, -1, +1, -1, +1, -1],
         [+1, +1, -1, -1, +1, +1, -1, -1, +1, +1, -1, -1, +1, +1, -1, -1, +1, +1, -1, -1, +1, +1, -1, -1, +1, +1, -1, -1, +1, +1, -1, -1],
         [+1, -1, -1, +1, +1, -1, -1, +1, +1, -1, -1, +1, +1, -1, -1, +1, +1, -1, -1, +1, +1, -1, -1, +1, +1, -1, -1, +1, +1, -1, -1, +1],
         [+1, +1, +1, +1, -1, -1, -1, -1, +1, +1, +1, +1, -1, -1, -1, -1, +1, +1, +1, +1, -1, -1, -1, -1, +1, +1, +1, +1, -1, -1, -1, -1],
         [+1, -1, +1, -1, -1, +1, -1, +1, +1, -1, +1, -1, -1, +1, -1, +1, +1, -1, +1, -1, -1, +1, -1, +1, +1, -1, +1, -1, -1, +1, -1, +1],
         [+1, +1, -1, -1, -1, -1, +1, +1, +1, +1, -1, -1, -1, -1, +1, +1, +1, +1, -1, -1, -1, -1, +1, +1, +1, +1, -1, -1, -1, -1, +1, +1],
         [+1, -1, -1, +1, -1, +1, +1, -1, +1, -1, -1, +1, -1, +1, +1, -1, +1, -1, -1, +1, -1, +1, +1, -1, +1, -1, -1, +1, -1, +1, +1, -1],
         [+1, +1, +1, +1, +1, +1, +1, +1, -1, -1, -1, -1, -1, -1, -1, -1, +1, +1, +1, +1, +1, +1, +1, +1, -1, -1, -1, -1, -1, -1, -1, -1],
         [+1, -1, +1, -1, +1, -1, +1, -1, -1, +1, -1, +1, -1, +1, -1, +1, +1, -1, +1, -1, +1, -1, +1, -1, -1, +1, -1, +1, -1, +1, -1, +1],
         [+1, +1, -1, -1, +1, +1, -1, -1, -1, -1, +1, +1, -1, -1, +1, +1, +1, +1, -1, -1, +1, +1, -1, -1, -1, -1, +1, +1, -1, -1, +1, +1],
         [+1, -1, -1, +1, +1, -1, -1, +1, -1, +1, +1, -1, -1, +1, +1, -1, +1, -1, -1, +1, +1, -1, -1, +1, -1, +1, +1, -1, -1, +1, +1, -1],
         [+1, +1, +1, +1, -1, -1, -1, -1, -1, -1, -1, -1, +1, +1, +1, +1, +1, +1, +1, +1, -1, -1, -1, -1, -1, -1, -1, -1, +1, +1, +1, +1],
         [+1, -1, +1, -1, -1, +1, -1, +1, -1, +1, -1, +1, +1, -1, +1, -1, +1, -1, +1, -1, -1, +1, -1, +1, -1, +1, -1, +1, +1, -1, +1, -1],
         [+1, +1, -1, -1, -1, -1, +1, +1, -1, -1, +1, +1, +1, +1, -1, -1, +1, +1, -1, -1, -1, -1, +1, +1, -1, -1, +1, +1, +1, +1, -1, -1],
         [+1, -1, -1, +1, -1, +1, +1, -1, -1, +1, +1, -1, +1, -1, -1, +1, +1, -1, -1, +1, -1, +1, +1, -1, -1, +1, +1, -1, +1, -1, -1, +1],
         [+1, +1, +1, +1, +1, +1, +1, +1, +1, +1, +1, +1, +1, +1, +1, +1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
         [+1, -1, +1, -1, +1, -1, +1, -1, +1, -1, +1, -1, +1, -1, +1, -1, -1, +1, -1, +1, -1, +1, -1, +1, -1, +1, -1, +1, -1, +1, -1, +1],
         [+1, +1, -1, -1, +1, +1, -1, -1, +1, +1, -1, -1, +1, +1, -1, -1, -1, -1, +1, +1, -1, -1, +1, +1, -1, -1, +1, +1, -1, -1, +1, +1],
         [+1, -1, -1, +1, +1, -1, -1, +1, +1, -1, -1, +1, +1, -1, -1, +1, -1, +1, +1, -1, -1, +1, +1, -1, -1, +1, +1, -1, -1, +1, +1, -1],
         [+1, +1, +1, +1, -1, -1, -1, -1, +1, +1, +1, +1, -1, -1, -1, -1, -1, -1, -1, -1, +1, +1, +1, +1, -1, -1, -1, -1, +1, +1, +1, +1],
         [+1, -1, +1, -1, -1, +1, -1, +1, +1, -1, +1, -1, -1, +1, -1, +1, -1, +1, -1, +1, +1, -1, +1, -1, -1, +1, -1, +1, +1, -1, +1, -1],
         [+1, +1, -1, -1, -1, -1, +1, +1, +1, +1, -1, -1, -1, -1, +1, +1, -1, -1, +1, +1, +1, +1, -1, -1, -1, -1, +1, +1, +1, +1, -1, -1],
         [+1, -1, -1, +1, -1, +1, +1, -1, +1, -1, -1, +1, -1, +1, +1, -1, -1, +1, +1, -1, +1, -1, -1, +1, -1, +1, +1, -1, +1, -1, -1, +1],
         [+1, +1, +1, +1, +1, +1, +1, +1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, +1, +1, +1, +1, +1, +1, +1, +1],
         [+1, -1, +1, -1, +1, -1, +1, -1, -1, +1, -1, +1, -1, +1, -1, +1, -1, +1, -1, +1, -1, +1, -1, +1, +1, -1, +1, -1, +1, -1, +1, -1],
         [+1, +1, -1, -1, +1, +1, -1, -1, -1, -1, +1, +1, -1, -1, +1, +1, -1, -1, +1, +1, -1, -1, +1, +1, +1, +1, -1, -1, +1, +1, -1, -1],
         [+1, -1, -1, +1, +1, -1, -1, +1, -1, +1, +1, -1, -1, +1, +1, -1, -1, +1, +1, -1, -1, +1, +1, -1, +1, -1, -1, +1, +1, -1, -1, +1],
         [+1, +1, +1, +1, -1, -1, -1, -1, -1, -1, -1, -1, +1, +1, +1, +1, -1, -1, -1, -1, +1, +1, +1, +1, +1, +1, +1, +1, -1, -1, -1, -1]]

    extr= [list(arr) for arr in numpy.random.normal(0, 1, (3, 300))]

    word_to_vec['<<']=extr[0]
    word_to_vec['>>']=extr[1]
    word_to_vec['--']=extr[2]

    ov = dict(zip(letters, arr))

    i = 0
    for key, value in word_to_vec.items():
        word_to_vec[key] = word_to_vec[key] + ov[key[:1]]
        print(i / 445)
        i += 1

    return word_to_vec
from random import shuffle
def prepare_X_y(final_data,word_to_vec,is_test):
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', ' ']

    char2vec = dict()
    for i, letter1 in enumerate(letters):
        for j, letter2 in enumerate(letters):
            after=i * 27 + j + 1
            char2vec[letter1 + letter2] = after

    char2vec['<<']=after+1
    char2vec['>>']=after+2
    char2vec['--']=after+3

    X = []
    y = []
    for h,sentence in enumerate(final_data):
        print(h/30000)
        t_X = []
        t_y = []
        for word in sentence:
            c_l = word[:2]
            if len(c_l) == 1:
                c_l = c_l + " "
            c_l = char2vec[c_l]
            t_X.append(c_l)
            if(not is_test):
                vec = word_to_vec[word]
                t_y.append(vec)

        X.append(t_X)
        y.append(t_y)

    if(is_test):
        return X

    words = []
    matrix = []

    for key, value in word_to_vec.items():
            words.append(key)
            matrix.append(value)

    return X,y,words,matrix

def build_trigram_KN(X):
    from nltk import trigrams,KneserNeyProbDist

    with open('X', 'rb') as file:
        file = pickle.load(file)

    lis = []
    for line in file:
        lis += (list(trigrams(line)))
    from nltk import FreqDist
    freq_dist = FreqDist(lis)
    k = KneserNeyProbDist(freq_dist)

    dic = dict()
    for i in k.samples():
        dic[i] = k.prob(i)

    with open('trigram_smoothened', 'wb') as output_file:
        pickle.dump(dic, output_file)

def save(list_of_files_to_save,list_of_file_name):
    for file,file_name in zip(list_of_files_to_save,list_of_file_name):
        with open(file_name, 'wb') as output_file:
            pickle.dump(file, output_file)






data,words_in_data,words_in_embedding,missing_words_in_data=clean_tokenize(read_file('songdata.csv'),'Story.txt')
save([data,words_in_data,words_in_embedding,missing_words_in_data],['data','words_in_data','words_in_embedding','missing_words_in_data'])
final_data,words_in_data=remv_sent_with_missing_words_add_start_end(data,missing_words_in_data,0)
save([final_data,words_in_data],['final_data','words_in_data'])
word_to_vec=build_embedding_dic(words_in_data)
word_to_vec=append_orthogonals_add_extras(word_to_vec)
save([word_to_vec],['word_to_vec'])

with open('word_to_vec','rb') as word_to_vec:
    word_to_vec=pickle.load(word_to_vec)

with open('final_data','rb') as final_data:
    final_data=pickle.load(final_data)

with open('missing_words_in_data','rb') as missing_words_in_data:
    missing_words_in_data=pickle.load(missing_words_in_data)



X,y,words,matrix=prepare_X_y(final_data,word_to_vec,0)
build_trigram_KN(X)
save([X,y,words,matrix],['X','y','words','matrix'])

'''
<< you are the kind of in and pain >> -- -- 
<< in the your are kind of an pain >> -- -- 
<< ohhow ashame pretty sensitive tree need days phone >> -- -- 
<< never seen ohhow apart pretty train days phone >> -- -- 
<< all deep fire in our existed >> -- -- -- -- 
<< deep in all find our existed >> -- -- -- -- 
<< so me questions but sensitive in her >> -- -- -- 
<< set me so questions but in here >> -- -- -- 
<< every sarcastic im vengo open >> -- -- -- -- -- 
<< open sentence everything im valley >> -- -- -- -- -- 
'''

Test=[['you','are','the','king','of','india','and','pakistan'], #original
      ['india', 'the', 'you', 'are', 'king', 'of', 'and', 'pakistan'], #bigram


      ['osi model','application','presentation','session','transport','network','datalink','physical'], #original
      ['network', 'session', 'osi model', 'application', 'presentation', 'transport', 'datalink', 'physical'], #bigram

      ['alogirthm','definiteness','finiteness','input','output','effectiveness'], #original
      ['definiteness', 'input', 'alogirthm', 'finiteness', 'output', 'effectiveness'], #bigram

      ['sorting','merge','quick','bubble','selection','insertion','heap'], #original
      ['selection', 'merge', 'sorting', 'quick', 'bubble', 'insertion', 'heap'], #bigram

      ['evolution','specification','implementation','validation','operation'], #original
      ['operation', 'specification', 'evolution', 'implementation', 'validation']] #bigram


'''
with open('missing_words_in_data','rb') as missing_words_in_data:
    missing_words_in_data=pickle.load(missing_words_in_data)


with open('word_to_vec','rb') as word_to_vec:
    word_to_vec=pickle.load(word_to_vec)
'''

Test=remv_sent_with_missing_words_add_start_end(Test,missing_words_in_data,1)
X_test=prepare_X_y(Test,word_to_vec,1)

save([X_test],['X_test'])




'''
['network', 'session', 'osi model', 'application', 'presentation', 'transport', 'datalink', 'physical'], #input
<< never seen ohhow apart pretty train days phone >> -- --  #mnemonic

['definiteness', 'input', 'alogirthm', 'finiteness', 'output', 'effectiveness'], #bigram
<< deep in all find our existed >> -- -- -- --  #mnemonic

['selection', 'merge', 'sorting', 'quick', 'bubble', 'insertion', 'heap'], #bigram
<< set me some queen but in heaven >> -- -- --   #mnemonic

['operation', 'specification', 'evolution', 'implementation', 'validation']] #bigram
<< open sentence everything im valley >> -- -- -- -- --   #mnemonic
'''










