import requests, unicodedata, os
from bs4 import BeautifulSoup
from scraping import get_interval_months, download_file, set_type_list

# set variables
type_list = 1 # 1 - Preços de Medicamentos (Preço Fábrica e Preço Máximo ao Consumidor) | 2 - Preços de Medicamentos para Compras Públicas
start_month = '01/21' # 'mm/YY'
end_month = '07/21' # 'mm/YY'
path = 'downloads'

# get html from website
response = requests.get('https://www.gov.br/anvisa/pt-br/assuntos/medicamentos/cmed/precos/anos-anteriores/anos-anteriores').text
soup = BeautifulSoup(response, 'html.parser')
content = soup.find('div', {'class': 'journal-content-article'})
full_content = content.find_all(['h3', 'p'])

# separate html content by type list
type_list_content = set_type_list(type_list, full_content)
tag_p = type_list_content.find_all('p')

# set interval dates by start and end dates.
interval = get_interval_months(start_month, end_month)

# set path's name to save files
name_path = interval[0].replace('/', '-') + '_' + interval[len(interval)-1].replace('/', '-') + '_' + str(type_list)

# check if folder exists
if not os.path.exists(path):
    os.mkdir(path)
if not os.path.exists(f'{path}/{name_path}'):
    os.mkdir(f'{path}/{name_path}')

# loop by month of interval
for month in interval:
    for p in tag_p:
        # check empty string
        if str(p.text).strip() != '':
            # normalize content tag and compare at same codification
            p_clean = unicodedata.normalize('NFKD', str(p))
            month_clean = unicodedata.normalize('NFKD', str(month))
            if f'{month_clean} (' in p_clean or f'{month_clean}20 (' in p_clean:
                try:
                    initial = str(p_clean).split(f'{month_clean} (')
                    final = initial[1].split(')')
                except:
                    initial = str(p_clean).split(f'{month_clean}20 (')
                    final = initial[1].split(')')

                html = BeautifulSoup(final[0], 'html.parser')
                tag_a = html.find_all('a')
                
                for a in tag_a:
                    if a.text.strip() == 'XLS':
                        print(a.get('href'))
                        filename = month.replace('/', '-') + '_' + str(type_list)
                        download_file(a.get('href'), f'{path}/{name_path}', filename)