
# coding: utf-8

# In[4]:


# -*- coding: cp950 -*-  
import requests
from bs4 import BeautifulSoup
import os

# Request HTML information
a = input('For retrieving ex-right & ex-dividend information, enter the stock number in 4 digits: ')

session = requests.Session()
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"}
url = "https://goodinfo.tw/StockInfo/StockDividendSchedule.asp?STOCK_ID={}".format(a)
req = session.get(url, headers=headers)
req.encoding = 'utf-8'

# Pull data out of HTML
soup = BeautifulSoup(req.text, 'html.parser')
stock_title = soup.select("title")[0].text

if not soup.select("#divDetail"):
    print("The stock you entered has no such information.")

else:
    tabledatasaved = ""
    for data in soup.select("#divDetail"):
        for data_tr in data.find_all('tr'):
            tabledata = ""
            for data_td in data_tr.find_all('td'):
                tabledata = tabledata + "," + data_td.text
            tabledatasaved = tabledatasaved + "\n" + tabledata[1:]
    
    # Write to a csv file
    with open(os.path.expanduser("{}.csv").format(stock_title[:10]),"wb") as file:
        file.write(bytes(tabledatasaved[120:], encoding='utf-8', errors='ignore'))
    
    print("Exported csv successfully!".format(stock_title[:10]))
    
input("\nPress any key to exit...")

