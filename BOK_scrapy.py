import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.signals import spider_closed
import pandas as pd
import time
import random


class QuotesSpider(scrapy.Spider):
    name = "getNaverNews"
    m_list = []
    datas=[]
    def start_requests(self):
        url_df=pd.read_csv("./sep_3_urls.csv")
        custom_header = {
            "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15"
        }
        
        for i in url_df["url"][144000:]:
            url = i
            time.sleep(random.randint(1,3)/10)
            yield scrapy.Request(url=url,headers=custom_header, callback=self.parse)
    
    def parse(self,response):
        try:
            date=response.css('span.media_end_head_info_datestamp_time::attr(data-date-time)').get()
            url=response.url
            title=response.css("h2 > span::text").get()
            article_text = response.css('article::text').getall()
            full_text = ' '.join(article_text).strip()
            self.datas.append([date,url,title,full_text])
        except:
            print("got error")

    def return_df_csv(self):
        df=pd.DataFrame(self.datas, columns=["date","url","title","full_text"])
        df.to_csv('./naver_news_urls_data2.csv')


    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.return_df_csv, signal=spider_closed)
        return spider


# 실행 코드

process = CrawlerProcess()
process.crawl(QuotesSpider)
process.start()