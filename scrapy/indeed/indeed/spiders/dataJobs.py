import scrapy

class Jobs(scrapy.Item):
    url = scrapy.Field()
    job_title = scrapy.Field()
    company = scrapy.Field()
    salary = scrapy.Field()
    type = scrapy.Field()

class LinksSpider(scrapy.Spider):
    name = 'dataJobs'
    allowed_domains = ['https://www.indeed.com/']
    try:
        with open("dataJobs_link.csv", "rt") as f:
            start_urls = [url.strip() for url in f.readlines()][1:]
    except:
        start_urls = []

    def parse(self, response):
        '''
        This function extracts Job title, Company Name, 
        Salary, Employment Type and url from all data 
        jobs found from dataJobs_link.py (saved in dataJobs_link.csv).
        '''
        job = Jobs()

        title_xpath = '//h1/text()'
        company_nolink_xpath = "//div[contains(@class, 'InlineCompany')]/div[2]/div/text()"
        company_link_xpath = "//div[contains(@class, 'InlineCompany')]/div[2]/div/a/text()"
        salary_guide_xpath = "//div[contains(@id, 'salaryGuide')]/ul/li[2]/text()"
        salary_xpath = "//div[contains(@id, 'jobDetails')]/div[2]/span/text()"
        type_xpath = "//div[contains(@id, 'jobDetails')]/div[3]/div[2]/text()"
        type_alt_xpath = "//div[contains(@id, 'jobDetails')]/div[2]/div[2]/text()"
        
        
        job['url'] = response.url
        job['job_title'] = response.xpath(title_xpath).extract()

        if response.xpath(company_link_xpath) == []:
            job['company'] = response.xpath(company_nolink_xpath).extract()
        else:
            job['company'] = response.xpath(company_link_xpath).extract()

        if response.xpath(salary_xpath) == []:
            job['salary'] = response.xpath(salary_guide_xpath).extract()
        else:
            job['salary'] = response.xpath(salary_xpath).get()
        if response.xpath(type_xpath) == []:
            job['type'] = response.xpath(type_alt_xpath).get()
        else:
            job['type'] = response.xpath(type_xpath).get()

        yield job