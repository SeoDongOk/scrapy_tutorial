from scrapy.crawler import CrawlerProcess

class ExampleSpider(scrapy.Spider):
    name = "example_spider"
    start_urls = ['https://www.example.com']

    def parse(self, response):
        self.log('Visited %s' % response.url)
        page_title = response.css('title::text').extract_first().strip()
        yield {'Title': page_title}

# Run the spider programmatically
if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(ExampleSpider)
    process.start()  # the script will block here until the crawling is finished
