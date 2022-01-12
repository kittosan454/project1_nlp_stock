import pandas as pd
import time
import numpy as np
from datetime import *
df = pd.read_csv("../team_project_1_stock/all_news.csv")
df['date'] = df['date'].str.replace('년', '-', regex=True)
df['date'] = df['date'].str.replace('월', '-', regex=True)
df['date'] = df['date'].str.replace('일', '-', regex=True)
df['date'] = df['date'].str.replace('.', '-', regex=True)
cols = ['date', 'time']
df['datetime'] =df[cols].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
df.info()

df['datetime'] = pd.to_datetime(df['datetime'])
df.drop('date', axis=1, inplace=True)
df.drop('time', axis=1, inplace=True)
df.rename(columns = {'old_nm' : 'new_nm'}, inplace = True)


cols = ['title', 'head']
df['title1'] = df[cols].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)


df.drop('title', axis=1, inplace=True)
df.drop('head', axis=1, inplace=True)
df.rename(columns = {'title1' : 'title'}, inplace = True)


# for i in range(28718):
#     if len(df['time']) > 5:
#         df['time'][i] = df['time'][i][0:4]
# print(df['time'])
# df.info()
# df['time'] = df['time'].astype('datetime64[ns]')
# df.info()

# dup = df.duplicated(['title'])
# print(dup)
# df.drop_duplicates(['title'], keep = 'first')
# df.info()
# # for i in (df.shape(4)):
# for i in range(28718):
#     if len(df['time'][i]) < 6:
#         df['time'][i] = df['time'][i] + ':00'
# df['time'] = df['time'].str.replace(' ', '0', regex=True)
# # for i in range(28718):
#     if ' ' in df['time'][i]:
#         df['time'][i] = '0'+df['time'][i]
print(df.tail())
# df.to_csv('./all_news.csv', index=False)


# print(df['time'])
# for i in range(28718):
#     date_time_str=df['time'][i]
#     df['time'][i] = datetime.strptime(date_time_str, '%H:%M:%S').date()



print(df.tail())
df.info()
df.to_csv('./all_news_datetime.csv', index=False)

df_kospi = pd.read_csv("../team_project_1_stock/all_news_5.csv")

# df_kospi['datetime'] = pd.to_datetime(df['datetime'])
# df_kospi['datetime'] = df_kospi['datetime'] + ' 15:00:00'

# df_kospi.to_csv('./all_news_5.csv', index=False)
df_kospi.info()
#
#
# df.sort_values(by='datetime', inplace = True)
#
# df_kospi.sort_values(by='datetime', inplace = True)
# # df.to_csv('./all_news_4.csv', index=False)
#
# df_2 = pd.merge_asof(df,df_kospi, on='datetime')
# df_2.to_csv('./all_news_6.csv', index=False)
# df_2.tail()

