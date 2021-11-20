import requests, json, sys
import pandas as pd
from datetime import date
from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta

def list_to_string_formatter(s):
    str1 = ''
    for ele in s: 
        str1 += str(ele)
        
    return str1

def set_type_list(type_list, full_content):
    customer = []
    for c in full_content:
        if str(c.text).strip() != '':
            if 'Públicas' in c.text:
                break
            else:
                customer.append(c)

    public = []
    for i in range(len(full_content)):
        try:
            if customer[i] == full_content[i]:
                pass
        except:
            public.append(full_content[i])
    
    if type_list == 1:
        return BeautifulSoup(list_to_string_formatter(customer), 'html.parser')
    elif type_list == 2:
        return BeautifulSoup(list_to_string_formatter(public), 'html.parser')
    else:
        print('wrong choice')
        sys.exit()

def get_month_name(month):
    with open('months.json', 'r') as output:
        data = json.load(output)
        for i in data:
            if i == month:
                return data[i]

        output.close()

def input_formatter_month(month):
    month = month.split("/")
    return int(month[0]), int(month[1])

def get_interval_months(start, end):
    m, y = input_formatter_month(start)
    start_date = date(int(f"20{y}"), m, 1)
    m, y = input_formatter_month(end)
    end_date = date(int(f"20{y}"), m, 1)

    interval_list = []
    interval = pd.date_range(start_date, end_date + relativedelta(months=1), freq="M")
    for month in interval:
        str_month = str(month.strftime("%Y/%m")).split("/")
        interval_list.append(f"{get_month_name(str_month[1])}/{str(str_month[0])[-2:]}")
    
    return interval_list

def download_file(url, path, filename):
    response = requests.get(url)
    with open(f'{path}/{filename}.xls', 'wb') as output:
        output.write(response.content)
        output.close()