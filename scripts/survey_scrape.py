"""Extracts data from the website wahlrecht.de and returns it in a structured format."""

import requests
from bs4 import BeautifulSoup
from datetime import datetime

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

def clean_percentages(percentages):
    clean_percentages = []
    for percentage in enumerate(percentages):
        percentage = percentage[1].get_text()
        percentage = percentage.replace(",", ".").replace("%", "").strip()
        try:
            clean_percentage = float(percentage)
            clean_percentages.append(clean_percentage)
        except ValueError:
            print(f"Could not convert {percentage} to float")
            clean_percentages.append(0)
    return clean_percentages

def extract_parties(data_rows):
    party_data = data_rows.copy()
    party_data.pop(0)
    collection_method_data = party_data.pop(-1)
    parties = {}
    for row in party_data:
        header = row.find("th")
        if header is None:
            print("No header found")
            continue

        percentages = row.find_all("td")
        if percentages is None:
            print("No percentages found")
            continue

        percentages.pop(0)
        cleaned_percentage = clean_percentages(percentages)
        parties[header.get_text()] = cleaned_percentage
            
    return parties, collection_method_data

def extract_dates(data_rows):
    dates = data_rows[0].find_all("span")
    dates = [date.get_text() for date in dates]
    return dates

def combine_party_with_date(dates, party_data):
    combined_data = {}
    for party, percentages in party_data.items():
        combined_data[party] = {}
        for i, date in enumerate(dates):
            if combined_data[party].get(date) is None:
                combined_data[party][date] = []
            combined_data[party][date].append(percentages[i])
        
    return combined_data

def sort_data(party_data):
    for party, data in party_data.items():
        sorted_dates = sorted(data.items(), key=lambda x: datetime.strptime(x[0], "%d.%m.%Y"))
        sorted_data = {date: values for date, values in sorted_dates}
        party_data[party] = sorted_data
    return party_data

def extract_min_max(party_data):
    for party, data in party_data.items():
        for date, values in data.items():
            min_value = min(values)
            max_value = max(values)
            party_data[party][date] = (min_value, max_value)
    return party_data

def extract_data():
    soup = get_soup(survey_url)
    data_rows = extract_rows(soup)
    dates = extract_dates(data_rows)
    party_data_raw, collection_method_data_raw = extract_parties(data_rows)
    party_data = combine_party_with_date(dates, party_data_raw)
    party_data = sort_data(party_data)
    party_data = extract_min_max(party_data)
    return party_data
