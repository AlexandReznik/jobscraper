import scrapy
import sys
import os
from ..items import JobScraperItem

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))


class LhhSpider(scrapy.Spider):
    name = "lhh"
    allowed_domains = ['lhh.com']
    start_urls = ['https://www.lhh.com/us/en/search-jobs/?s=date-reverse/']

    custom_settings = {
        'ITEM_PIPELINES': {
            'job_scraper.pipelines.DatabasePipeline': 300,
        }
    }

    def __init__(self):
        super(LhhSpider, self).__init__()
        from app.common.database import SessionLocal
        self.session = SessionLocal()

    def parse(self, response):
        for job in response.css('li.c-job-listing-card'):
            job_title = job.css('p.c-job-listing-card__header::text').get()
            company_name = job.css(
                'div.c-job-listing-card__details p.c-job-listing-card__category span::text').get()
            job_location = job.css('p.c-job-listing-card__category::text').get()
            date_posted = job.css('div.cta-container span::text').get()
            job_link = response.urljoin(job.css('div.c-job-search-item-url a::attr(href)').get())
            
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

        next_page = response.css(
            'ul.pagination-container div li.a.c-job-listing-left__right-arrow::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def closed(self, reason):
        self.session.close()