from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time
from datetime import datetime,timedelta
import numpy as np
from sklearn.model_selection import train_test_split
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
from sklearn.preprocessing import LabelEncoder
import pickle
from collections import defaultdict
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

form_window = uic.loadUiType('./signal_slot.ui')[0]

class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_1.clicked.connect(self.btn_clicked_slot)
        self.count = 0

        pd.set_option('display.unicode.east_asian_width', True)

        self.Y = datetime.now().year
        self.M = datetime.now().month
        self.D = datetime.now().day

    def btn_clicked_slot(self):
        print('btn_clicked_slot() 실행')
        self.lbl_1.setText(str(self.count))
        self.titles = []
        self.heads = []
        self.dts = []

        self.MK()
        time.sleep(1)
        self.HK()
        self.df = pd.DataFrame(self.titles, columns=['title'])
        self.df['head'] = self.heads
        self.df['date'] = self.dts
        self.driver.close()

        self.df['title_head'] = self.df['title'].str.cat(self.df['head'].astype(str), sep=' ')
        self.df = self.df.drop(['title', 'head'], axis=1)
        print(self.df['date'])

        self.df['date'] = pd.to_datetime(self.df['date'])
        print('debug1')
        self.df = self.df[(self.df['date'].apply(lambda x: x.hour) > 00) & (self.df['date'].apply(lambda x: x.hour) < 9)]
        print('debug3')
        predict_result = self.connectPreprocess()
        print('debug2')
        A = np.sum(predict_result)
        B = len(self.X)
        result = A/B
        self.lbl_1.setText(str(result))

    def MK(self):
        options = webdriver.ChromeOptions()
        options.add_argument('lang=ko_KR')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('disable-gpu')
        options.add_argument('headless')

        self.driver = webdriver.Chrome('../team_project_1_stock/chromedriver.exe')

        for l in range(1, 5):
            try:
                url = 'https://find.mk.co.kr/new/search.php?pageNum={0}&cat=&cat1=&media_eco=&pageSize=10&sub=all&dispFlag=OFF&page=news&s_kwd=%B4%BA%BF%E5%C1%F5%BD%C3&s_page=news&go_page=&ord=1&ord1=1&ord2=0&s_keyword=%B4%BA%BF%E5%C1%F5%BD%C3&period=p_direct&s_i_keyword=%B4%BA%BF%E5%C1%F5%BD%C3&s_author=&y1={1}&m1={2}&d1={3}&y2={1}&m2={2}&d2={3}&media%5B0%5D=all&media%5B1%5D=00001&media%5B3%5D=eco&media%5B4%5D=20000&ord=1&area=ttbd'.format(
                    l, self.Y, self.M, self.D)
                self.driver.get(url)

                for i in range(3, 23):
                    try:
                        title = self.driver.find_element_by_xpath(
                            '/html/body/center/table/tbody/tr[1]/td[1]/div[{}]/span[1]/a'.format(i)).text
                        print('a:',title)
                        title = re.compile('[^가-힣 ]').sub(' ', title)
                        print('b:',title)
                        self.titles.append(title)

                        head = self.driver.find_element_by_xpath(
                            '/html/body/center/table/tbody/tr[1]/td[1]/div[{}]/a'.format(i)).text
                        head = re.compile('[^가-힣 ]').sub(' ', head)
                        print(head)
                        self.heads.append(head)

                        dt = self.driver.find_element_by_xpath(
                            '/html/body/center/table/tbody/tr[1]/td[1]/div[{}]/span[2]'.format(i)).text
                        dt = re.compile('[^0-9|: ]').sub(' ', dt)
                        dt = dt[-22:-3]
                        print(dt)
                        self.dts.append(dt)

                    except StaleElementReferenceException:
                        self.driver.get(url)
                        print('StaleElementReferenceException')
                        time.sleep(1)

                        title = self.driver.find_element_by_xpath(
                            '/html/body/center/table/tbody/tr[1]/td[1]/div[{}]/span[1]/a'.format(i)).text
                        title = re.compile('[^가-힣 ]').sub(' ', title)
                        print(title)
                        self.titles.append(title)

                        head = self.driver.find_element_by_xpath(
                            '/html/body/center/table/tbody/tr[1]/td[1]/div[{}]/a'.format(i)).text
                        head = re.compile('[^가-힣 ]').sub(' ', head)
                        print(head)
                        self.heads.append(head)

                        dt = self.driver.find_element_by_xpath(
                            '/html/body/center/table/tbody/tr[1]/td[1]/div[{}]/span[2]'.format(i)).text
                        dt = re.compile('[^0-9|: ]').sub(' ', dt)
                        dt = dt[-22:-3]
                        print(dt)
                        self.dts.append(dt)
            except:
                print('a')
                break

    def HK(self):
        for j in range(1, 5):
            try:
                url = 'https://search.hankyung.com/apps.frm/search.news?query=%EB%89%B4%EC%9A%95%EC%A6%9D%EC%8B%9C&sort=DATE%2FDESC%2CRANK%2FDESC&period=DATE&area=ALL&mediaid_clust=&sdate={1}.{2}.{3}&edate={1}.{2}.{3}&exact=&include=&except=&page={0}'.format(
                    j, self.Y, self.M, self.D)
                self.driver.get(url)
                for k in range(1, 11):
                    try:
                        title = self.driver.find_element_by_xpath(
                            '//*[@id="content"]/div[1]/div[2]/div[1]/div/ul/li[{}]/div/a/em'.format(k)).text
                        title = re.compile('[^가-힣 ]').sub(' ', title)
                        print(title)
                        self.titles.append(title)

                        head = self.driver.find_element_by_xpath(
                            '//*[@id="content"]/div[1]/div[2]/div[1]/div/ul/li[{}]/div/p[1]'.format(k)).text
                        head = re.compile('[^가-힣 ]').sub(' ', head)
                        print(head)
                        self.heads.append(head)

                        dt = self.driver.find_element_by_xpath(
                            '//*[@id="content"]/div[1]/div[2]/div[1]/div/ul/li[{}]/div/p[2]/span[2]'.format(k)).text
                        dt = re.compile('[^0-9|: ]').sub(' ', dt)
                        print(dt)
                        self.dts.append(dt)

                    except StaleElementReferenceException:
                        self.driver.get(url)
                        print('StaleElementReferenceException')
                        time.sleep(1)

                        title = self.driver.find_element_by_xpath(
                            '//*[@id="content"]/div[1]/div[2]/div[1]/div/ul/li[{}]/div/a/em'.format(k)).text
                        title = re.compile('[^가-힣 ]').sub(' ', title)
                        print(title)
                        self.titles.append(title)

                        head = self.driver.find_element_by_xpath(
                            '//*[@id="content"]/div[1]/div[2]/div[1]/div/ul/li[{}]/div/p[1]'.format(k)).text
                        head = re.compile('[^가-힣 ]').sub(' ', head)
                        print(head)
                        self.heads.append(head)

                        dt = self.driver.find_element_by_xpath(
                            '//*[@id="content"]/div[1]/div[2]/div[1]/div/ul/li[{}]/div/p[2]/span[2]'.format(k)).text
                        dt = re.compile('[^0-9|: ]').sub(' ', dt)
                        print(dt)
                        self.dts.append(dt)
            except:
                break

    def connectPreprocess(self):
        with open('encoder_0-8.pickle', 'rb') as f:
            encoder = pickle.load(f)
            label = encoder.classes_

        print(self.df['title_head'])
        self.X = self.df['title_head']
        print(self.X.iloc[0])
        okt = Okt()
        X1 = []
        for i in range(len(self.X)):
            self.X.iloc[i] = okt.morphs(self.X.iloc[i], stem=True)
            X1.append(self.X.iloc[i])
        stopwords = pd.read_csv('stopwords.csv', index_col=0)
        X = pd.Series(X1)
        words = []
        for j in range(len(X)):
            words = []
            for i in range(len(X[j])):
                if len(X[j][i]) > 1:
                    if X[j][i] not in list(stopwords['stopword']):
                        words.append(X[j][i])
            X[j] = ' '.join(words)
        with open('news_token_0_8.pickle', 'rb') as f:
            token = pickle.load(f)

        tokened_X = token.texts_to_sequences(X)

        X_pad = pad_sequences(tokened_X, 76)
        model = load_model('pi_for_fi_0-8_model_0.7442218661308289.h5')
        preds = model.predict(X_pad)
        predicts = []
        for pred in preds:
            predicts.append(label[np.argmax(pred)])
        print(type(predicts))
        print(type(predicts[0]))

        return predicts


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())

