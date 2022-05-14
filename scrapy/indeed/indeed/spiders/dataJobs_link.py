import scrapy

# Using Scrapy to extract data job links from https://www.indeed.com/browsejobs/Title/D 
# filtered for Remote and Entry level positions with limit to 4 pages. 

class Link(scrapy.Item):
    link = scrapy.Field()

class LinksSpider(scrapy.Spider):
    name = 'dataJobs_link'
    allowed_domains = ['https://www.indeed.com/']
    
    start_urls = ['https://www.indeed.com/browsejobs/Title/D']

    def parse(self, response):
        '''
        This function finds all data jobs category in job title D 
        category. It further calls the parse_remote function for 
        each data job category found.
        '''
        xpath = '//a[contains(@href, "q-Data")]/@href'
        selection = response.xpath(xpath)
        for s in selection:
            url = 'https://www.indeed.com' + s.get()
            yield scrapy.Request(url, callback=self.parse_remote, dont_filter=True)

    def parse_remote(self, response):
        '''
        This function filters for remote data jobs in data jobs 
        category. It further calls the parse_experience function 
        for each data job category filtered by Remote.
        '''
        xpath = '//div[text()="Remote"]/parent::button/following-sibling::ul//a[contains(text(),"Remote")]/@href'
        selection = response.xpath(xpath)
        for s in selection:
            url = 'https://www.indeed.com' + s.get()
            yield scrapy.Request(url, callback=self.parse_experience, dont_filter=True)

    def parse_experience(self, response):
        '''
        This function further filters for entry level data jobs in 
        data jobs category. It further calls the parse_pagination 
        function for each data job category filtered by Experience Level.
        '''
        xpath = '//div[text()="Experience Level"]/parent::button/following-sibling::ul//a[contains(text(),"Entry")]/@href'
        selection = response.xpath(xpath)
        for s in selection:
            for j in range(10,41,10):
                url = 'https://www.indeed.com' + s.get() + '&start=' + str(j)
                yield scrapy.Request(url, callback=self.parse_jobsLink, dont_filter=True)

    def parse_jobsLink(self, response):
        '''
        This function further extract data job links from the 4 pages of 
        filtered data jobs category.
        '''
        xpath = "//a[contains(@id,'job_')]/@href"
        selection = response.xpath(xpath)
        for s in selection:
            l = Link()
            l['link'] = 'https://www.indeed.com' + s.get()
            yield l
            
