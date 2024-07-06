import scrapy
import sys
import os
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
            company_name = job.css('div.job-list-item__pic a::text').get()
            job_title = job.css('a.job-list-item__link::text').get()
            job_link = response.urljoin(job.css('a.job-list-item__link::attr(href)').get())
            date_posted = job.css('span.text-muted span[title]::text').get().strip()
            job_location = job.css('span.location-text::text').get().strip()

            item = JobScraperItem(
                title=job_title,
                company=company_name,
                date_posted=date_posted,
                url=job_link,
                location=job_location
            )
            yield item
        next_page = response.css(
            'ul.pagination.pagination_with_numbers '
            'li.page-item a.page-link span.bi.bi-chevron-right.page-item--icon'
        ).xpath('../@href').get()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
    
    def closed(self, reason):
        self.session.close()