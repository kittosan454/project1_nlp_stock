import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
pd.set_option('display.unicode.east_asian_width', True)
df = pd.read_csv('./all_news_final.csv')
df['bi'].plot(kind='hist')
plt.show()
