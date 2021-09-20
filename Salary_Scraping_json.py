#!/usr/bin/env python
# coding: utf-8

# ## Scraped By : Shuaib Alamrity (Data analyst and Data scraper)
# 

# In[55]:


# import librariess
import time , re , csv , json
from bs4 import BeautifulSoup
import requests
import pandas as pd


# In[56]:


# create template for url can use for any jobs or city
template = 'https://www.salary.com/research/salary/alternate/{}-salary/{}'


# ### Scraping salary data for 'Senior Accountant' on 'chicago-il'

# In[32]:


position = 'senior-accountant'
city = 'chicago-il'
url = template.format(position , city)


# In[57]:


# useing requests library to import source code for page  
src = requests.get(url).text
soup = BeautifulSoup(src , 'lxml')
soup;


# In[58]:


# find json script for salary data
pattern = re.compile(r'Occupation')
script = soup.find('script',{'type':'application/ld+json'},text=pattern)
script;


# In[59]:


json_row = script.contents[0]
json_row


# In[36]:


json_data = json.loads(json_row)
json_data;


# In[60]:


# scraping title and other data
title = json_data['name']
location = json_data['occupationLocation'][0]['name']
description = json_data['description']
ntile10 = json_data['estimatedSalary'][0]['percentile10']
ntile25 = json_data['estimatedSalary'][0]['percentile25']
ntile50 = json_data['estimatedSalary'][0]['median']
ntile75 = json_data['estimatedSalary'][0]['percentile75']
ntile90 = json_data['estimatedSalary'][0]['percentile90']


# In[61]:


salary_data =(title , location ,description,ntile10 , ntile25 , ntile50 , ntile75 , ntile90)
salary_data


# ### Create function for scraping data salary on largest cities

# In[62]:


def extract_salary_info(job_title , job_city):
    """Extract and return satary data information """
    template = 'https://www.salary.com/research/salary/alternate/{}-salary/{}'
    url = template.format(position , city)
    try :
        response = requests.get(url)
        if response.status_code != 200 :
            return None
    except requests.exceptions.RequestException :
        return None
    soup = BeautifulSoup(response.text  , 'lxml')
    battern = re.compile(r'Occupation')
    script = soup.find('script',{'type':'application/ld+json'},text=pattern)
    json_row = script.contents[0]
    json_data = json.loads(json_row)
    title = json_data['name']
    location = json_data['occupationLocation'][0]['name']
    description = json_data['description']
    ntile10 = json_data['estimatedSalary'][0]['percentile10']
    ntile25 = json_data['estimatedSalary'][0]['percentile25']
    ntile50 = json_data['estimatedSalary'][0]['median']
    ntile75 = json_data['estimatedSalary'][0]['percentile75']
    ntile90 = json_data['estimatedSalary'][0]['percentile90']
    salary_data =(title , location ,description,ntile10 , ntile25 , ntile50 , ntile75 , ntile90)
    return salary_data


# In[63]:


# import largest cities 
with open ('largest_cities.csv' , newline='') as f :
    reader = csv.reader(f)
    cities = [city for row in reader for city in row]


# In[64]:


# scraping salary data from 10 cities
salary_data = []
for city in cities[:10]:
    result = extract_salary_info(position , city)
    if result :
        salary_data.append(result)
        time.sleep(0.5)


# In[65]:


for row in salary_data :
    print(row)


# In[66]:


# storing salary data on csv file 
with open('salary_result.csv' , 'w',newline='',encoding='utf-8') as f :
    writer = csv.writer(f)
    writer.writerow(['title' , 'location' , 'description' , 'ntile10' , 'ntile25' , 'ntile50' , 'ntile75' , 'ntile90'])
    writer.writerows(salary_data)


# In[ ]:





# In[ ]:




