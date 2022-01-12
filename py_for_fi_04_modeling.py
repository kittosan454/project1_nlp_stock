import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import *





X_train, X_test, Y_train, Y_test = np.load('./news_data_max_896_size_12169.npy', allow_pickle=True)

print(X_train.shape, Y_train.shape)
print(X_test.shape, Y_test.shape)



model = Sequential()
model.add(Embedding(12169, 300, input_length = 896)) #자연어 처리하는 레이어 wordsize를 준다. 1055차원을 300차원으로 축소 너무 차원이 많으면 희소해진다. 임베딩: 서로 유사한 단어들 좌표평면상 가깝게 위치시킨다
model.add(Conv1D(32, kernel_size =5, padding='same' , activation='relu')) # 문맥을 파악하기 위하여 conv1d를 쓴다.
model.add(MaxPool1D(pool_size=1)) # 맥스풀을 안할꺼면 사이즈는 1준다.
model.add(LSTM(128, activation='tanh', return_sequences=True)) # LSTM은 tanh을 준다.
model.add(Dropout(0.3))
model.add(LSTM(64, activation='tanh', return_sequences=True)) # LSTM은 순서가 있는 데이터.
model.add(Dropout(0.3))
model.add(LSTM(64, activation='tanh')) # LSTM은 tanh을 준다.
model.add(Dropout(0.3))
model.add(Flatten())
model.add(Dense(128, activation = 'relu'))
model.add(Dense(2, activation = 'softmax'))
print(model.summary())

model.compile(loss='binary_crossentropy', optimizer = 'adam', metrics =['accuracy'])
fit_hist = model.fit(X_train, Y_train, batch_size = 100, epochs=8, validation_data=(X_test, Y_test))

model.save('./news_stock_{}.h5'.format(fit_hist.history['val_accuracy'][-1]))

plt.plot(fit_hist.history['accuracy'], label='accuracy')
plt.plot(fit_hist.history['val_accuracy'], label='val accuracy')
plt.legend()
plt.show()