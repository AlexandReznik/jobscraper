from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from job_scraper.spiders.djinni import DjinniSpider
from job_scraper.spiders.dou import DouSpider
from job_scraper.spiders.lhh import LhhSpider


process = CrawlerProcess(settings=get_project_settings())
process.crawl(DjinniSpider)
process.crawl(DouSpider)
process.crawl(LhhSpider)
process.start()
# from scrapy.crawler import CrawlerProcess
# from .app.job_scraper.spiders.djinni import DjinniSpider
# from .app.job_scraper.spiders.dou import DouSpider
# from .app.job_scraper.spiders.lhh import LhhSpider
# from .app.job_scraper import settings as scraper_settings


# def run_scrapers():
#     process = CrawlerProcess(settings={
#         **scraper_settings,
#         'LOG_LEVEL': 'INFO',
#     })
    
#     process.crawl(DjinniSpider)
#     process.crawl(DouSpider)
#     process.crawl(LhhSpider)
#     process.start()


# if __name__ == '__main__':
#     run_scrapers()