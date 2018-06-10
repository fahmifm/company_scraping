from celery import Celery
from lxml import html
import json
import requests
import re

app = Celery('worker', backend='rpc://', broker='amqp://')


@app.task
def crawler(data):
    '''Request and parse data from company URL'''
    # Get raw page from url
    resp = requests.get(data['url'])
    resp.encoding = 'utf-8'

    # Parse element from raw page
    tree = html.fromstring(resp.text)
    text = tree.xpath("//p/strong[contains(text(), {})]/../following-sibling::table/tr".format(data['ticker_symbol']))
    clean_text = [i.replace("\n", "").replace("\t", "") for i in text[0].xpath("td[1]/text()")]
    name = clean_text[0]
    address = clean_text[1]
    phone1 = clean_text[2]
    international_phone1 = phone_num_parser(phone1)
    phone2 = clean_text[3]
    international_phone2 = phone_num_parser(phone2)
    email = clean_text[4]
    website = clean_text[5]
    business = clean_text[6].replace("Business: ", "")

    # Parse financial summary data
    financial_summary = {}
    summ = text[0].xpath("td[2]/table/tr")
    for i in summ:
        key = i.xpath('td[1]/strong/text()')[0].replace(":", "").lower()
        try:
            val = i.xpath('td[2]/text()')[0]
        except:
            val = ""
        financial_summary.update({key: val})

    # Parse bussines summary data
    bs = str(text[1].xpath("td")[0].text_content())
    bs = bs.replace("\t", "").replace(u"\xa0", "")
    business_summary = re.search(r"Business Summary:\n(.*?)\n", bs).group(1)

    result = re.findall(r"Auditing Company:\n(.*?)Add|Auditing Company:\n(.*?)Địa|Auditing Company:\n(.*?)\n", bs)
    auditing_company = get_val(result)     

    result = re.findall(r"Address: (.*?)Tel|Địa chỉ: (.*?)Điện|Address: (.*?)\n|Địa chỉ: (.*?)\n", bs)
    auditing_company_address = get_val(result)

    result = re.findall(r"Tel: (.*?) -|Tel: (.*?) Fax|Điện thoại:(.*?) -|Điện thoại: (.*?) -|Điện thoại: (.*?) Fax|Điện thoại:(.*?) Fax", bs)
    auditing_company_phone = get_val(result)

    result = re.findall(r"Fax: (.*?) W|Fax: (.*?)W|Fax: (.*?)\n", bs)
    auditing_company_fax = get_val(result)

    result = re.findall(r"Website: (.*?) -|Website: (.*?)\n", bs)
    auditing_company_web = get_val(result)

    result = re.findall(r"Email: (.*?)\n", bs)
    auditing_company_email = result[0] if result else ""

    result = re.findall(r"Established License: (.*?)\n", bs)
    established_license = result[0] if result else ""

    result = re.findall(r"Business License: (.*?)\n", bs)
    business_license = result[0] if result else ""

    # Create company profile dict
    company_profile = {
        "company name": data["company_name"],
        "company_url": data["url"],
        "ticker_symbol": data["ticker_symbol"],
        "company street address": address,
        "country": "Vietnam",
        "company description": business_summary,
        "company phone number": [phone1, phone2],
        "business": business,
        "company website": website,
        "company email": email,
        "financial summary": financial_summary,
        "business registration": {
            "established licence": established_license, 
            "business license": business_license
        },
        "auditing company": {
            "company_name": auditing_company, 
            "address": auditing_company_address, 
            "phone_number": auditing_company_phone,
            "email": auditing_company_email,
            "website": auditing_company_web
        }
    }

    return company_profile


def get_val(result):
    '''get value from findall result'''
    val = ''
    if result:
        for i in result[0]:
            if i:
                val = i

    return val


def phone_num_parser(number):
    '''parse phone number international'''
    list_number = re.findall(r"\d+", number)
    clean_number = "".join(list_number)
    parsed_number = re.sub(r'^\0|84', '+84', clean_number, 1)
    return parsed_number
