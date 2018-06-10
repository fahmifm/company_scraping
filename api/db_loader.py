from api.app import db
from api.config import app_config
from api.models import CompanyProfile, FinancialSummary
from datetime import datetime
import json
import re


class DBLoader():
    def loader(self, filepath):
        f = open(filepath, 'r')
        scrape_data = json.load(f)
        f.close()

        for i in scrape_data:
            company_profile = CompanyProfile(
                company_url=i['company_url'],
                company_name=i['company name'],
                company_email=i['company email'],
                company_website=i['company website'],
                company_street_address=i['company street address'],
                company_description=i['company description'],
                industry=i['business'],
                country=i['country'],
                company_phone_number=i['company phone number']
            )
            financial_summary = FinancialSummary(
                capital_currency=i['financial summary']['capital currency'],
                market_cap=self.to_int(i['financial summary']['market cap']),
                par_value=self.to_int(i['financial summary']['par value']),
                equity=self.to_int(i['financial summary']['equity']),
                listing_volume=self.to_int(i['financial summary']['listing volume']),
                listed_date=self.date_parser(i['financial summary']['listed date']),
                initial_listed_price=self.to_int(
                    i['financial summary']['initial listed price']),
                company=company_profile
            )

            db.session.add(company_profile)
            db.session.add(financial_summary)
            db.session.commit()

    def date_parser(self, date):
        if date != '00-00-0000':
            date = datetime.strptime(date, '%m-%d-%Y')
        else:
            date = None

        return date

    def to_int(self, number):
        number = "".join(re.findall(r"\d+", number))
        return int(number)
