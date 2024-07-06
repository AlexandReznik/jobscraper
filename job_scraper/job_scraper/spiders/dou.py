import scrapy


class DouSpider(scrapy.Spider):
    name = "dou"
    start_urls = ['https://jobs.dou.ua/vacancies/']

    def parse(self, response):
        for job in response.css('div.vacancy'):
            yield {
                'title': job.css('div.title a::text').get(),
                'company': job.css('a.company::text').get(),
                'location': job.css('span.cities::text').get(),
                'description': job.css('div.sh-info::text').get(),
                'url': job.css('div.title a::attr(href)').get(),
            }

        next_page = response.css('a.next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

