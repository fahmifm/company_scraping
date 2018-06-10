from scrape.app import StockScrape

stock = StockScrape()

if __name__ == '__main__':
    list_company = stock.get_company()
    stock.company_parser(list_company)
