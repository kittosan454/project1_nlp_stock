import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from konlpy.tag import Okt # pip로만 깔 수 있다. 한국어 자연어 처리를 위함
from tensorflow.keras.preprocessing.text import *
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical
import pickle
import time
from datetime import *
import re

pd.set_option('display.unicode.east_asian_width', True)

df = pd.read_csv('./all_news_merge.csv')



X = df['title']
Y = df['bi']

encoder = LabelEncoder()
labeled_Y = encoder.fit_transform(Y) # 라벨에 대한 정보를 가진다. 카테고리 값을 숫자로 바꾼다.
label = encoder.classes_ #라벨에 대한 정보를 알려준다.

print(labeled_Y)
print(labeled_Y[0])
print(label)

with open('./encoder.pickle', 'wb') as f:
    pickle.dump(encoder, f)

onehot_Y = to_categorical(labeled_Y)  # 원 핫 인코딩
print(onehot_Y)

## 형태소 분리 제거

okt = Okt()
okt_pos_X = okt.pos(X[0])
print(okt_pos_X )


for i in range(len(X)):
   X[i] = okt.morphs(X[i], stem=True)

stopwords = pd.read_csv('./stopwords_team_project1.csv', index_col=0)


for j in range(len(X)):
    words =[]
    for i in range(len(X[j])):

        if len(X[j][i]) > 1:
            if X[j][i]not in list(stopwords['stopword']):
                words.append(X[j][i])
    X[j] = ' '.join(words)

print(X)

#형태소 하나하나를 숫자로 바꾸기

token = Tokenizer() #딕셔너리 형태임
token.fit_on_texts(X)
print(token)
tokened_X = token.texts_to_sequences(X)
print(tokened_X[0])



with open('./news_token.pickle', 'wb') as f:
    pickle.dump(token,f)

wordsize = len(token.word_index)+1 # 0을 포함한 사용된 단어의 갯수 사이즈가 필요하다
print(wordsize)
print(token.index_word) # 딕셔너리는 슬라이싱이 안된다

max = 0
for i in range(len(tokened_X)):
    if max < len(tokened_X[i]):
        max = len(tokened_X[i])
print(max)

X_pad = pad_sequences(tokened_X, max) # max사이즈로 맞춰서 0을 넣어라

print(X_pad[:10])

X_train, X_test, Y_train, Y_test = train_test_split(X_pad, onehot_Y, test_size=0.1)
print(X_train.shape, Y_train.shape)
print(X_test.shape, Y_test.shape)

xy = X_train, X_test, Y_train, Y_test
print(xy)
np.save('./news_data_max_{}_size_{}'.format(max, wordsize), xy)