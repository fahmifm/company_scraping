import requests
import json
import re
from lxml import html
from datetime import datetime
from scrape.worker import crawler


class StockScrape():
    '''Scrape vietnam stock market'''
    def __init__(self):
        '''Scrape vietnam stock market'''

        # main URL
        self.url = "http://stock.vietnammarkets.com/vietnam-stock-market.php"
        f = open("company_index.json", "w")
        f.write(json.dumps(list(dict())))
        f.close()

    def get_company(self):
        '''Get list company from first page'''
        # get raw page
        resp = requests.get(self.url)

        # parse response into html tree
        tree = html.fromstring(resp.text)

        # list company data
        list_company = tree.xpath(
            "//p[contains(., 'Vietnam Publicly Traded Companies')]/following-sibling::table/tr")

        # remove first title row
        del list_company[0]

        return list_company

    def company_parser(self, list_company):
        '''Parse company profile'''
        company_index = []
        task = []
        for i in list_company:
            ticker = i.xpath("td[1]/a")[0]
            ticker_symbol = ticker.text
            ticker_url = ticker.get("href")
            company = i.xpath("td[2]/text()")[0]
            bussiness = i.xpath("td[3]/text()")[0]
            listing_bourse = i.xpath("td[4]/text()")[0]
            date = datetime.strftime(datetime.now(), "%Y-%m-%d")
            company_data = {
                "ticker_symbol": ticker_symbol,
                "company_name": company,
                "url": ticker_url,
                "bussiness": bussiness,
                "crawled_at": date,
                "listing_bourse": listing_bourse
            }

            company_index.append(company_data)
            bg_task = crawler.delay(company_data)
            task.append(bg_task)

        f = open("company_index.json", "w")
        f.write(json.dumps(company_index, ensure_ascii=False))
        f.close()

        company_profile = []
        # Loop over task to get return data from worker
        for i in task:
            company_profile.append(i.get())

        f = open("company_profile.json", "w")
        f.write(json.dumps(company_profile, ensure_ascii=False))
        f.close()