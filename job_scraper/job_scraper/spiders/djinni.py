import scrapy
import sys
import os
from ..items import JobScraperItem

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from app.common.database import SessionLocal


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
        self.session = SessionLocal()

    def parse(self, response):
        job_items = response.css('li.list-jobs__item.job-list__item')
        
        for job in job_items:
            # job_id = int(job.css('li::attr(id)').extract_first().split('-')[-1])
            company_name = job.css('div.job-list-item__pic a::text').get()
            job_title = job.css('a.job-list-item__link::text').get()
            job_link = response.urljoin(job.css('a.job-list-item__link::attr(href)').get())
            date_posted = job.css('span.text-muted span[title]::text').get().strip()
            job_location = job.css('span.location-text::text').get().strip()

            item = JobScraperItem(
                title=job_title,
                company=company_name,
                location=job_location,
                date_posted=date_posted,
                url=job_link
            )
            yield item
        next_page = response.css('a[data-test="pagination-next"]::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
    
    def closed(self, reason):
        self.session.close()
        # next_page = response.css('a.page-link.next-page::attr(href)').get()
        # if next_page:
        #     yield Request(url=response.urljoin(next_page), callback=self.parse)
    # def parse(self, response):
    #     for job in response.css('li.list-jobs__item'):
    #         yield {
    #             'title': job.css('div.list-jobs__title a::text').get(),
    #             'company': job.css('div.list-jobs__details__info a::text').get(),
    #             'location': job.css('div.list-jobs__details__info span::text').get(),
    #             'description': job.css('div.list-jobs__description::text').get(),
    #             'url': job.css('div.list-jobs__title a::attr(href)').get(),
    #         }

    #     next_page = response.css('a.next::attr(href)').get()
    #     if next_page is not None:
    #         yield response.follow(next_page, self.parse)
