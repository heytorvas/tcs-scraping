import requests, unicodedata, os
from bs4 import BeautifulSoup
from scraping import get_interval_months, download_file, set_type_list

type_list = 3
start_month = '01/21'
end_month = '02/21'
path = 'downloads'

response = requests.get('https://www.gov.br/anvisa/pt-br/assuntos/medicamentos/cmed/precos/anos-anteriores/anos-anteriores').text
soup = BeautifulSoup(response, 'html.parser')
content = soup.find('div', {'class': 'journal-content-article'})
full_content = content.find_all(['h3', 'p'])

type_list_content = set_type_list(type_list, full_content)
tag_p = type_list_content.find_all('p')

interval = get_interval_months(start_month, end_month)
name_path = interval[0].replace('/', '-') + '_' + interval[len(interval)-1].replace('/', '-') + '_' + str(type_list)

if not os.path.exists(path):
    os.mkdir(path)
if not os.path.exists(f'{path}/{name_path}'):
    os.mkdir(f'{path}/{name_path}')

for month in interval:
    for p in tag_p:
        if str(p.text).strip() != '':
            p_clean = unicodedata.normalize('NFKD', str(p))
            if f'{month} (' in p_clean or f'{month}20 (' in p_clean:
                try:
                    initial = str(p_clean).split(f'{month} (')
                    final = initial[1].split(')')
                except:
                    initial = str(p_clean).split(f'{month}20 (')
                    final = initial[1].split(')')

                html = BeautifulSoup(final[0], 'html.parser')
                tag_a = html.find_all('a')
                
                for a in tag_a:
                    if a.text.strip() == 'XLS':
                        print(a.get('href'))
                        filename = month.replace('/', '-') + '_' + str(type_list)
                        download_file(a.get('href'), f'{path}/{name_path}', filename)