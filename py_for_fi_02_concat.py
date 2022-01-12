import pandas as pd
import glob
import re
import time


data_paths = glob.glob('./crawling/*')

print(data_paths)
df = pd.read_csv("./crawling/edaily_news_1-30.csv", index_col = 0)
print(df.head())


for data_path in data_paths:
    df_temp = pd.read_csv(data_path, index_col=0)
    print(data_path)
    df = pd.concat([df, df_temp])



df.info()
df.dropna(inplace=True)
df.reset_index(drop=True, inplace=True) #인덱스 재정렬

for i in range(28718):
    str_head = df['head'][i]
    head = re.compile('[^가-힣]').sub(' ', str_head)
    df['head'][i] = head
    print(df.head())

for i in range(28718):
    str_title = df['title'][i]
    title = re.compile('[^가-힣]').sub(' ', str_title)
    df['title'][i] = title
    print(df.head())

print(df.head())
print(df.tail())
print(df['title'].value_counts())
print(df.info())

df.to_csv('./all_news.csv', index=False)