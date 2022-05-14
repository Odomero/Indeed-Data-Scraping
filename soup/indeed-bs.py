import pandas as pd
from urllib import request  # Odomero
# import requests
from bs4 import BeautifulSoup as beaut
import ssl  # Odomero
import re
import csv

url = 'https://www.indeed.com/browsejobs/Title/D'
html = request.urlopen(url)
bs = beaut(html.read(), 'html.parser')

tags = bs.find_all('a', {'title':re.compile('Data.*')})


links = ['https://www.indeed.com' + tag['href'] for tag in tags]

################################################################################
# This part prepares  links
################################################################################
Data_jobs = []

for link in links:
    #print(link)
    html = request.urlopen(link)
    bs = beaut(html.read(), 'html.parser')
    tag = bs.find('ul', {'id': 'filter-remotejob-menu'}).find_all('li')[0].find('a')
    Data_jobs.append('https://www.indeed.com' + tag['href'])
## The above code extracts the remote jobs only from each Data related jobs. Temporarily remote jobs were excluded.
data_entry = []
for link in Data_jobs[1:5]:
    y = request.urlopen(link)

    soup = beaut(y.read(), 'html.parser')
    try:
        tag = soup.find('ul', {'id': 'filter-explvl-menu'}).find_all('li')[1].find('a')
        if "Entry" in tag.text:
            tag = soup.find('ul', {'id': 'filter-explvl-menu'}).find_all('li')[1].find('a')
        else:
            tag = soup.find('ul', {'id': 'filter-explvl-menu'}).find_all('li')[2].find('a')
    except:
        tag = soup.find('ul', {'id': 'filter-explvl-menu'}).find_all('li')[0].find('a')

## The above code extract the Entry level position from each Data related jobs.
# The if else statement ensures that only 'Entry level' jobs are extracted from pages where the criteria is not the 2nd element on the list.

    data_entry.append('https://www.indeed.com' + tag['href'])

joblink =[]
for link in data_entry :
    for j in range(10,41,10) :
        y = request.urlopen(link + '&start=' + str(j))
        bs = beaut(y.read(), 'html.parser')
        tags = bs.find_all('a', {'id': re.compile('job_.*')})

        for tag in tags :
            joblink.append('http://indeed.com' + tag['href'])


d = pd.DataFrame({'company': [], 'salary': [], 'title': [], 'type': [], 'url': []})

for Link in joblink :
    html = request.urlopen(Link)
    bs = beaut(html.read(), 'html.parser')
    try:
        title= bs.find('h1').text
    except:
        title = ''
    try:
        salary = bs.find('div', string = 'Salary').next_sibling.text
    except:
        salary = ''

    try:
        company = bs.find('div', {'class': 'jobsearch-JobDescriptionSection'}).find('a').text
    except:
        company = ''
    try:
        type = bs.find('div', string = 'Job Type').find('div').text
    except:
        type = ''
    url = Link


    Datajoblist = {'title': title, 'salary': salary, 'company': company, 'url': url}

    d = d.append(Datajoblist, ignore_index = True)
    #print(d)

################################################################################
# This part saves data to csv.
################################################################################
d.to_csv('Datajoblist.csv')