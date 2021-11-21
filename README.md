# Web Scraping for TCS

## Installation
1. Clone this repository:
```
git clone https://github.com/heytorvas/tcs-scraping.git
```
2. Change to repository:
```
cd tcs-scraping
```
3. Install libraries required for this repository.
```bash
pip install -r requirements.txt
```

## Execution
1. Set search parameters in main.py
* type_list -> set which list will be save by algorithm, e.g.: 1
* start_month -> start date of search on 'mm/YY' format, e.g.: '01/19'
* end_month -> end date of search on 'mm/YY' format, e.g.: '01/21'
* file_format -> file format to save, e.g.: 'xls'
* path -> folder where files will be save, e.g.: 'downloads'

2. Run script
```bash
python3 main.py
```

## Notes
* type_list parameter:
```
1 - Preços de Medicamentos (Preço Fábrica e Preço Máximo ao Consumidor)
2 - Preços de Medicamentos para Compras Públicas
```
* Colab Notebook: https://colab.research.google.com/drive/1oQPyea3sxjYc4mrspBfBwMFx-uRM9kvl?usp=sharing