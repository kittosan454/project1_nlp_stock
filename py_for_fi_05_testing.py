import pandas as pd
import numpy as np

from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
import pickle
from tensorflow.keras.models import load_model


X_train, X_test, Y_train, Y_test = np.load('./news_data_max_896_size_12169.npy', allow_pickle=True)


model = load_model('./news_stock_0.6917626261711121.h5')

score = model.evaluate(X_test, Y_test)
print('Evaluation loss :', score[0])
print('Evaluation accuracy :', score[1])