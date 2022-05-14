from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd

# Using Selenum to extract data job links from https://www.indeed.com/browsejobs/Title/D 
# filtered for Remote and Entry level positions with limit to 4 pages. 

# Init:
gecko_path = '/usr/local/bin/geckodriver'
ser = Service(gecko_path)
options = webdriver.firefox.options.Options()
options.headless = False
driver = webdriver.Firefox(options = options, service=ser)

url = 'https://www.indeed.com/browsejobs/Title/D'

dataJobLinks = [] #holding all data jobs category
paginationLinks = [] #holding 4 pages of each filtered data jobs category
jobLinks = [] #holding all data job links found for 4 pages of each filtered data jobs category

# Actual program:
driver.get(url)

time.sleep(2)

#Extracting data jobs category links from job title D category
dataJobs_link = driver.find_elements(By.XPATH, '//a[contains(@href, "q-Data")]')
for link in dataJobs_link:
    dataJobLinks.append(link.get_attribute('href'))

#Filtering for Remote and Entry Level data jobs in each data jobs category
for link in dataJobLinks:
    driver.get(link)
    time.sleep(2)
    data_remote = driver.find_element(By.XPATH, '//button[@id="filter-remotejob"]')
    data_remote.click()
    remote = driver.find_element(By.XPATH, '//div[text()="Remote"]/parent::button/following-sibling::ul//a[contains(text(),"Remote")]')
    remote.click()
    time.sleep(2)
    try:
        pop_over = driver.find_element(By.XPATH, '//div[@id="popover-x"]/button')
        pop_over.click()
    except:
        time.sleep(1)
    data_entry = driver.find_element(By.XPATH, '//button[@id="filter-explvl"]')
    data_entry.click()
    entry = driver.find_element(By.XPATH, '//div[text()="Experience Level"]/parent::button/following-sibling::ul//a[contains(text(),"Entry")]')
    new_link = entry.get_attribute('href')
    entry.click()
    #Extracting 4 pages of each filtered data jobs category
    for j in range(10,41,10):
        url = new_link + '&start=' + str(j)

        #Extracting data job links from 4 pages of each filtered data jobs category 
        driver.get(url)
        job_page = driver.find_elements(By.XPATH, '//a[contains(@id,"job_")]')
        for job in job_page:
            jobLinks.append(job.get_attribute('href'))

print(len(jobLinks)) #Number of data job links extracted 

#Extracting Job title, Company Name, Salary, Employment Type and url for each data job found
dataJobs = pd.DataFrame({'job_title':[], 'company_name':[], 'salary':[], 'employment_type':[],'url':[]})
for link in jobLinks:
    driver.get(link)
    
    title = driver.find_element(By.XPATH, '//h1')
    job_title = title.text
    
    try:
        com = driver.find_element(By.XPATH, '//div[contains(@class, "InlineCompany")]/div[2]/div')
        company_name = com.text
    except:
        com = driver.find_element(By.XPATH, '//div[contains(@class, "InlineCompany")]/div[2]/div/a')
        company_name = com.text
    
    try:
        sal = driver.find_element(By.XPATH, '//div[contains(@id, "salaryGuide")]/ul/li[2]')
        salary = sal.text
    except:
        try:
            sal = driver.find_element(By.XPATH, '//div[contains(@id, "jobDetails")]/div[2]/span')
            salary = sal.text
        except:
            salary = ""

    try:
        type = driver.find_element(By.XPATH, '//div[contains(@id, "jobDetails")]/div[3]/div[2]')
        employment_type = type.text
    except:
        try:
            type =driver.find_element(By.XPATH, '//div[contains(@id, "jobDetails")]/div[2]/div[2]')
            employment_type = type.text
        except:
            employment_type = ""

    url = link

    jobs = {'job_title':job_title, 'company_name':company_name, 'salary':salary, 'employment_type':employment_type,'url':url}
   
    dataJobs = dataJobs.append(jobs, ignore_index = True)

#Saving all extracted data job info (Job title, Company Name, 
#Salary, Employment Type and url) to CSV file. 
dataJobs.to_csv('dataJobs.csv')

time.sleep(10)

# Close browser:
driver.quit()
