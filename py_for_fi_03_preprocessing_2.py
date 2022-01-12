import pandas as pd

df_kospi = pd.read_csv("../team_project_1_stock/all_news_5.csv")
df_kospi['datetime'] = pd.to_datetime(df_kospi['datetime'])
# df_kospi['datetime'] = pd.to_datetime(df['datetime'])
# df_kospi['datetime'] = df_kospi['datetime'] + ' 15:00:00'
print(df_kospi.tail())
# df_kospi.to_csv('./all_news_5.csv', index=False)
df_kospi.info()
df = pd.read_csv("../team_project_1_stock/all_news_datetime.csv")
df['datetime'] = pd.to_datetime(df['datetime'])
df.drop_duplicates(subset=None, keep='first', inplace=True)
df.info()
print(df.tail())

df.sort_values(by='datetime', inplace = True)
print(df.tail())
df_kospi.sort_values(by='datetime', inplace = True)


print(df_kospi.tail())

df = pd.merge_asof(df,df_kospi, on='datetime')
df=df[(df["datetime"].apply(lambda x : x.hour)>00) & (df["datetime"].apply(lambda x : x.hour)<11)]
df.dropna(inplace=True)
df.to_csv('./all_news_merge.csv', index=False)

df.tail()

