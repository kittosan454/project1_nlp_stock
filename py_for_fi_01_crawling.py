from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time

options = webdriver.ChromeOptions()
options.add_argument('lang=ko_KR')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('disable-gpu')
driver = webdriver.Chrome('./chromedriver',
                          options=options)

url = 'https://www.edaily.co.kr/search/news/?source=total&keyword=%EB%89%B4%EC%9A%95%EC%A6%9D%EC%8B%9C&include=&exclude=&jname=&start=20181001&end=20211118&sort=latest&date=pick&exact=false'
driver.get(url)




titles = []
heads = []
dates = []
times = []

for j in range(31, 257):
    try:
        url = 'https://www.edaily.co.kr/search/news/?source=total&keyword=%EB%89%B4%EC%9A%95%EC%A6%9D%EC%8B%9C&include=&exclude=&jname=&start=20181001&end=20211118&sort=latest&date=pick&exact=fals&page={}'.format(j)
        driver.get(url)
        for i in range(1, 10):
            title = driver.find_element_by_xpath('//*[@id="newsList"]/div[{}]/a/ul/li[1]'.format(i)).text
            title = re.compile('[^가-힣|a-z|A-Z|0-9|.%]').sub(' ', title)
            print(title)
            titles.append(title)

            head = driver.find_element_by_xpath('//*[@id="newsList"]/div[{}]/a/ul/li[2]'.format(i)).text
            head = re.compile('[^가-힣|a-z|A-Z|0-9|.%]').sub(' ', head)
            heads.append(head)

            driver.find_element_by_xpath('//*[@id="newsList"]/div[{}]/a/ul/li[1]'.format(i)).click()

            date_time = driver.find_element_by_xpath(
                '//*[@id="contents"]/section[1]/section[1]/div[1]/div[1]/div/div/ul/li[1]/p[1]').text
            dates.append(date_time[2:13])

            times.append(date_time[-8:])
            print(date_time)

            driver.back()

    except :
        print('error')

    if j % 10 == 0:
        df_section_titles = pd.DataFrame(titles, columns=['title'])
        df_section_titles['head'] = heads
        df_section_titles['date'] = dates
        df_section_titles['time'] = times
        df_section_titles.to_csv(
            './crawling/edaily_news_{}-{}.csv'.format(j - 9, j),
            index=True)
        titles = []
        heads = []
        dates = []
        times = []

df_section_titles = pd.DataFrame(titles, columns=['title'])
df_section_titles['head'] = heads
df_section_titles['date'] = dates
df_section_titles['time'] = times

driver.close()


#df_section_titles = pd.DataFrame(titles, columns=['title'])
# df_section_titles['date'] = dates
pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 20)
print(df_section_titles)

df_section_titles.to_csv('./crawling/edaily_news_remain'
                         '.csv')