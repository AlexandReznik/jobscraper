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