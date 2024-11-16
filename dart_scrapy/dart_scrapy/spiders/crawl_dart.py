from pathlib import Path
import pandas as pd
import scrapy
from bs4 import BeautifulSoup

class QuotesSpider(scrapy.Spider):
    name = "dart_scrapy"

    custom_settings = {
        'ROBOTSTXT_OBEY': False,  # Disable robots.txt restrictions
    }

    def start_requests(self):
        url = [
            "https://dart.fss.or.kr/dsab007/detailSearch.ax"
            # "https://dart.fss.or.kr/report/viewer.do?rcpNo=20241114001712&dcmNo=10183643&eleId=18&offset=157100&length=23043&dtd=dart4.xsd"
            ]
        data = {
        "currentPage": "1",
        "maxResults": "15",
        "maxLinks": "10",
        "sort": "date",
        "series": "desc",
        "textCrpCik": "00164779",
        "lateKeyword": "",
        "keyword": "",
        "reportNamePopYn": "",
        "textkeyword": "",
        "businessCode": "all",
        "autoSearch": "N",
        "option": "corp",
        "textCrpNm": "SK하이닉스",
        "reportName": "",
        "tocSrch": "",
        "textPresenterNm": "",
        "startDate": "20231117",
        "endDate": "20241117",
        "decadeType": "",
        "finalReport": "recent",
        "businessNm": "전체",
        "corporationType": "all",
        "closingAccountsMonth": "all",
        "reportName2": "",
        "tocSrch2": "",
        }
        
        for i in url:
            yield scrapy.FormRequest(
            url=i,
            formdata=data,
            callback=self.parse,
        )

    def parse(self, response):
        self.log(f"Response status: {response.status}")
        try:
            soup = BeautifulSoup(response.body, "html.parser")
            a_list=soup.find_all("a")
            for a in a_list:
                try:
                    i = a["href"]
                    if "rcpNo" in i:
                        self.log(f"response {i}")
                        self.log(f"response: {a.text}")
                except:
                    pass
            # dfs = pd.read_html(response.body)
            # filename = f"./dart_result.csv"
            # combined_df = pd.concat(dfs, ignore_index=True)                
            # combined_df.to_csv(filename, index=False)
            # self.log(f"Saved combined table to {filename}")

        except ValueError as e:
            self.log(f"Failed to parse HTML: {e}")
