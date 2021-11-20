import requests, json, sys
import pandas as pd
from datetime import date
from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta

def list_to_string_formatter(array):
    """
    Format a tags list on unique string.
    
    Parameters
    ----------
    array : list
        list of tags
    
    Returns
    ----------
    string : str
        list formatted to word.
    """
    string = ''
    for tag in array: 
        string += str(tag)
        
    return string

def set_type_list(type_list, full_content):
    """
    Set html content by type list required.
    
    Parameters
    ----------
    type_list : int
        number of type list
    full_content : Tag
        all tags inside journal-content-article's div

    Returns
    ----------
    html : Tag
        tags about type list required
    """
    
    customer = []
    for c in full_content:
        if str(c.text).strip() != '':
            if 'Públicas' in c.text:
                break
            else:
                customer.append(c)

    public = []
    for p in range(len(full_content)):
        try:
            if customer[p] == full_content[p]:
                pass
        except:
            public.append(full_content[p])
    
    if type_list == 1:
        return BeautifulSoup(list_to_string_formatter(customer), 'html.parser')
    elif type_list == 2:
        return BeautifulSoup(list_to_string_formatter(public), 'html.parser')
    else:
        print('wrong choice')
        sys.exit()

def get_month_name(month):
    """
    Get month's name by month's number.
    
    Parameters
    ----------
    month : str
        number of month

    Returns
    ----------
    month : str
        name of month
    """

    with open('months.json', 'r') as output:
        data = json.load(output)
        for i in data:
            if i == month:
                return data[i]

        output.close()

def input_formatter_month(date):
    """
    Split date input in month and year.
    
    Parameters
    ----------
    date : str
        date with month and year

    Returns
    ----------
    month : int
        month splitted 
    year : int
        year splitted
    """

    date = date.split("/")
    return int(date[0]), int(date[1])

def get_interval_months(start, end):
    """
    Get interval months by dates required.
    
    Parameters
    ----------
    start : str
        start date with month and year
    end : str
        end date with month and year

    Returns
    ----------
    interval_list : list
        list of all months inside interval required
    """
    
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

def download_file(url, path, filename, file_format):
    """
    Download file and save on local machine.
    
    Parameters
    ----------
    url : str
        url to download file
    path : str
        name of folder to save
    filename : str
        name of the file

    Returns
    ----------
    None
    """

    response = requests.get(url)
    with open(f'{path}/{filename}.{file_format}', 'wb') as output:
        output.write(response.content)
        output.close()