import os
import sys

import scrapy

from ..items import JobScraperItem


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))


class DjinniSpider(scrapy.Spider):
    name = 'djinni'
    allowed_domains = ['djinni.co']
    start_urls = ['https://djinni.co/jobs/']

    custom_settings = {
        'ITEM_PIPELINES': {
            'job_scraper.pipelines.DatabasePipeline': 300,
        }
    }

    def __init__(self):
        super(DjinniSpider, self).__init__()
        from app.common.database import SessionLocal
        self.session = SessionLocal()

    def parse(self, response):
        job_items = response.css('li.list-jobs__item.job-list__item')
        
        for job in job_items:
            company_name = response.urljoin(job.css('div.job-list-item__pic a::attr(href)').get())
            job_title = job.css('a.job-list-item__link::text').get()
            job_link = response.urljoin(job.css('a.job-list-item__link::attr(href)').get())
            date_posted = job.css('span.mr-2.nobr::attr(data-original-title)').get()
            job_location = job.css('div.job-list-item__job-info::text').get()

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
        next_page = response.css('li.page-item a.page-link::attr(href)').get()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
    
    def closed(self, reason):
        self.session.close()