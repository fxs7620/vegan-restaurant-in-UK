# Extract vegan restaurants number 
import random
import requests
import pandas as pd
from lxml import etree
import re

users =['Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24',
 'Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6',
 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3',
 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20',
 'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)',
 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1',
 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6',
 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3']


def get_data(url):
    for n in range(5):
        try:
            #携带UA和cookie
            headers = {'User-Agent':random.choice(users),}
            datas = requests.get(url,headers = headers,timeout = 10).text
        except Exception:
            pass
        else:
            break
    return datas


url = 'https://www.tripadvisor.co.uk/Restaurants-g186216-United_Kingdom.html'
data = get_data(url)
html = etree.HTML(data)

# get city link 
links = html.xpath('//div[@class="geo_name"]/a/@href')
cities = html.xpath('//div[@class="geo_name"]/a/text()')

# get city id
ids = [l.split('-')[1].replace('g','') for l in links]

# re formula to extract number 
r1 = 'listResultCount&quot;:(.*?),&quot'
re1 = re.compile(r1)
counts = []
for i in range(len(ids)):
    id_ = ids[i]
    link = 'https://www.tripadvisor.co.uk/RestaurantSearch?Action=FILTER&ajax=1&availSearchEnabled=false&sortOrder=relevance&geo='+str(id_)+'&itags=10591&zfz=10697'
    df = get_data(link)
    HTML = etree.HTML(df)
    count = ''.join(re1.findall(df))
    counts.append(count)
    print(cities[i],count)

#print('all',sum([int(c) for c in counts]))
counts.append(sum([int(c) for c in counts]))

# save to df
df = pd.DataFrame()
df['city'] = cities
df['count'] = [int(c) for c in counts]

df.to_excel('data.xlsx',index =None)