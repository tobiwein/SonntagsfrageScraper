"""Extracts data from the website wahlrecht.de"""

import requests
from bs4 import BeautifulSoup

survey_url = "https://www.wahlrecht.de/umfragen/"

def get_soup(url):
    response = requests.get(url)
    if response.status_code == 200:
        print(f"Page retrieved successfully. Status code: {response.status_code}")
    else:
        print(f"Error: Could not retrieve page. Status code: {response.status_code}, Message: {response.reason}")
        exit()

    return BeautifulSoup(response.text, "html.parser")

def extract_rows(soup):
    target_div = soup.find_all('div')[1]
    if target_div is None:
        print("No div found")
        exit()

    data_table = target_div.find("table")
    if data_table is None:
        print("No table found")
        exit()

    return data_table.find('tbody').find_all('tr')

def extract_parties(data_rows):
    parties = []
    for row in data_rows:
        header = row.find("th")
        if header is not None:
            parties.append(header.get_text())
    parties.pop(0)
    return parties

def extract_data():
    soup = get_soup(survey_url)
    data_rows = extract_rows(soup)
    collection_method = data_rows.pop(-1)
    parties = extract_parties(data_rows)




