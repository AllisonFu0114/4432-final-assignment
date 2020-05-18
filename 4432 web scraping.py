#!/usr/bin/env python
# coding: utf-8

# In[1]:


from datetime import timedelta
from bs4 import BeautifulSoup
import pandas as pd
import requests
import requests_cache


# In[2]:


requests_cache.install_cache(
    'cache',
    expire_after=timedelta(hours=24),
    allowable_methods=('GET', 'POST')
)


# In[3]:


url='https://report.boonecountymo.org/mrcjava/servlet/RMS01_MP.I00030s?max_rows=10000'


# In[4]:


r=requests.post(url,
params={'rls_lastname':'C0'},
headers={'user-agent':"4432 assignment"})


# In[5]:


soup= BeautifulSoup(r.text)


# In[6]:


table= soup.find('table', class_='collapse data-table shadow responsive')


# In[7]:


th_all =table.find('thead').find_all('tr')[1].find_all('th')


# In[8]:


for th in th_all:
    print(th.text)


# In[9]:


headers =[ ]


# In[10]:


for th in th_all:
    header = th.text.strip().replace(' ', '_').lower()
    headers.append(header)


# In[11]:


headers


# In[12]:


tr_all= table.find_all('tr')[2:199]


# In[13]:


for tr in tr_all:
    for td in tr.find_all('td'):
        print(td.text.strip())
    print('---------------')


# In[14]:


def clean_row(tds):
    return tds


# In[15]:


for tr in tr_all:
    print('--------------')
    tds = tr.find_all('td')
    row = clean_row(tds)
    print(row)


# In[16]:


def clean_row(tds): 
    row = { 'details_url': tds[9].find('a').attrs['href'], 'last_name': tds[0].text.strip(), 'first_name': tds[1].text.strip(), 'middle_name': tds[2].text.strip(), 'suffix': tds[3].text.strip(), 'sex': tds[4].text.strip(), 'race': tds[5].text.strip(), 'age': int(tds[6].text.strip()), 'city': tds[7].text.strip(), 'state': tds[8].text.strip() } 
    return row


# In[17]:


rows=[]


# In[18]:


for tr in tr_all:
    tds = tr.find_all('td')
    row = clean_row(tds)
    rows.append(row)


# In[19]:


import csv


# In[20]:


rows[0].keys()


# In[21]:


with open('detainees.csv', 'w', newline='') as f:
    writer = csv.DictWriter(
        f, fieldnames=rows[0].keys()
    )
    
    writer.writeheader()
    for row in rows:
        writer.writerow(row)


# In[22]:


url1 = "https://report.boonecountymo.org/mrcjava/servlet/RMS01_MP.R00040s?run=2&R001=&R002=&ID=1946&hover_redir=&width=950"
resp = requests.get(url1)
html = resp.text


# In[23]:


with open("1.html", "r", encoding="utf-8") as f:
    html = f.read()


# In[24]:


soup = BeautifulSoup(html, "html.parser")


# In[25]:


divs = soup.find_all("div", attrs={"class": "mugshotDiv"})


# In[26]:


items = []


# In[27]:


for div in divs:

    name = div.find("div", attrs={"class": "inmateName"}).string

    chargesContainerTag = div.find("div", attrs={"class": "chargesContainer"})

    chargesContainerBody = chargesContainerTag.find("tbody", attrs={"id": "mrc_main_table"})
    for tr in chargesContainerBody.find_all("tr"):
        if len(tr.find_all("td")) != 8:
            continue
       
        items.append({
            "Name": name,
            "Case #": tr.find('td', attrs={"data-th": "Case #"}).string,
            'Charge Description': tr.find('td', attrs={"data-th": "Charge Description"}).string,
            'Charge Status': tr.find('td', attrs={"data-th": "Charge Status"}).string,
            'Bail Amount': tr.find('td', attrs={"data-th": "Bail Amount"}).string,
            'Bond Type': tr.find('td', attrs={"data-th": "Bond Type"}).string,
            'Court Date': tr.find('td', attrs={"data-th": "Court Date"}).string,
            'Court Time': tr.find('td', attrs={"data-th": "Court Time"}).string,
            'Court of Jurisdiction': tr.find('td', attrs={"data-th": "Court of Jurisdiction"}).string
        })


# In[28]:


df = pd.DataFrame(items)


# In[29]:


df.to_csv("boonecountymo.csv", index=False)


# In[ ]:




