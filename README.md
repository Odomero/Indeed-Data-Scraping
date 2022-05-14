# Indeed.com Data Jobs Scraping

The aim of our project was to scrape data from Indeed.com useful 
to recent graduates in the data science and analysis field. 
We scraped using Beautiful Soup, Scrapy and Selenium.

Indeed is an American worldwide employment website for job listings launched in November 2004. 
The website provides a wide search engine for different types of jobs from all over the world.

### Beautiful Soup
Pre-requisites:
pip install bs4
pip install urllib

cd into soup
python3 indeed-bs.py

### Scrapy
Pre-requisites:
pip install scrapy

cd into scrapy
scrapy crawl dataJobs_link -O dataJobs_link.csv
scrapy crawl dataJobs -O dataJobs.csv

### Selenium
Pre-requisites:
pip install Selenium

cd into selenium
python3 indeed_Selenium.py
