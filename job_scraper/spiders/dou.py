import scrapy
import sys
import os
from ..items import JobScraperItem

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))


class DouSpider(scrapy.Spider):
    name = "dou"
    start_urls = ['https://jobs.dou.ua/vacancies/']

    custom_settings = {
        'ITEM_PIPELINES': {
            'job_scraper.pipelines.DatabasePipeline': 300,
        }
    }

    def __init__(self):
        super(DouSpider, self).__init__()
        from app.common.database import SessionLocal
        self.session = SessionLocal()

    def parse(self, response):
        for job in response.css('li.l-vacancy.__hot'):
            job_title = job.css('div.title a::text').get()
            company_name = response.urljoin(job.css('a.company::attr(href)').get())
            job_location = job.css('span.cities::text').get()
            date_posted = job.css('div.date::text').get()
            job_link = response.urljoin(job.css('div.title a::attr(href)').get())
            
            company_name = company_name.strip() if company_name else None
            job_title = job_title.strip() if job_title else None
            date_posted = date_posted.strip() if date_posted else None
            job_location = job_location.strip() if job_location else None 

            item = JobScraperItem(
                title=job_title,
                company=company_name,
                date_posted=date_posted,
                url=job_link,
                location=job_location
            )
            yield item

        next_page = response.css('div.more-btn a::attr(href)').get()
        if next_page and next_page.startswith('http'):
            yield response.follow(next_page, self.parse)

    def closed(self, reason):
        self.session.close()