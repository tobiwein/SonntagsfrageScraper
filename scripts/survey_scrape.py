"""Extracts data from the website wahlrecht.de and returns it in a structured format."""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)

survey_url = "https://www.wahlrecht.de/umfragen/"

def get_soup(url):
    """
    Fetches the HTML content from the given URL and returns a BeautifulSoup object.

    Parameters:
    url (str): The URL to fetch the HTML content from.

    Returns:
    BeautifulSoup: A BeautifulSoup object containing the parsed HTML content.
    """
    response = requests.get(url)
    if response.status_code != 200:
        logging.error(f"Error: Could not retrieve page. Status code: {response.status_code}, Message: {response.reason}")
        raise Exception(f"Error: Could not retrieve page. Status code: {response.status_code}, Message: {response.reason}")
    logging.info(f"Page retrieved successfully. Status code: {response.status_code}")
    return BeautifulSoup(response.text, "html.parser")

def extract_rows(soup):
    """
    Extracts the rows from the target table in the BeautifulSoup object.

    Parameters:
    soup (BeautifulSoup): The BeautifulSoup object containing the parsed HTML content.

    Returns:
    list: A list of rows (BeautifulSoup objects) from the target table.
    """
    target_div = soup.find_all('div')[1]
    if target_div is None:
        logging.error("No div found")
        raise Exception("No div found")

    data_table = target_div.find("table")
    if data_table is None:
        logging.error("No table found")
        raise Exception("No table found")

    return data_table.find('tbody').find_all('tr')

def clean_percentages(percentages):
    """
    Cleans and converts percentage strings to float values.

    Parameters:
    percentages (list): A list of BeautifulSoup objects containing percentage strings.

    Returns:
    list: A list of cleaned percentage float values.
    """
    cleaned_percentages = []
    for percentage in percentages:
        percentage_text = percentage.get_text()
        percentage_text = percentage_text.replace(",", ".").replace("%", "").strip()
        try:
            cleaned_percentage = float(percentage_text)
            cleaned_percentages.append(cleaned_percentage)
        except ValueError:
            logging.warning(f"Could not convert {percentage_text} to float")
            cleaned_percentages.append(0)
    return cleaned_percentages

def extract_parties(data_rows):
    """
    Extracts party data from the rows.

    Parameters:
    data_rows (list): A list of rows (BeautifulSoup objects) from the target table.

    Returns:
    tuple: A tuple containing a dictionary of party data and the collection method data.
    """
    party_data = data_rows.copy()
    party_data.pop(0)
    collection_method_data = party_data.pop(-1)
    parties = {}
    for row in party_data:
        header = row.find("th")
        if header is None:
            logging.warning("No header found")
            continue

        percentages = row.find_all("td")
        if percentages is None:
            logging.warning("No percentages found")
            continue

        percentages.pop(0)
        header_text = header.get_text()
        if header_text == "GRÜNE":
            header_text = "GRUENE"
        cleaned_percentage = clean_percentages(percentages)
        parties[header_text] = cleaned_percentage
            
    return parties, collection_method_data

def extract_dates(data_rows):
    """
    Extracts dates from the first row of the table.

    Parameters:
    data_rows (list): A list of rows (BeautifulSoup objects) from the target table.

    Returns:
    list: A list of date strings.
    """
    dates = data_rows[0].find_all("span")
    return [date.get_text() for date in dates]

def combine_party_with_date(dates, party_data):
    """
    Combines party data with corresponding dates.

    Parameters:
    dates (list): A list of date strings.
    party_data (dict): A dictionary of party data.

    Returns:
    dict: A dictionary combining party data with corresponding dates.
    """
    combined_data = {}
    for party, percentages in party_data.items():
        combined_data[party] = {}
        for i, date in enumerate(dates):
            if combined_data[party].get(date) is None:
                combined_data[party][date] = []
            combined_data[party][date].append(percentages[i])
        
    return combined_data

def sort_data(party_data):
    """
    Sorts the party data by dates.

    Parameters:
    party_data (dict): A dictionary of party data.

    Returns:
    dict: A dictionary of sorted party data.
    """
    for party, data in party_data.items():
        sorted_dates = sorted(data.items(), key=lambda x: datetime.strptime(x[0], "%d.%m.%Y"))
        sorted_data = {date: values for date, values in sorted_dates}
        party_data[party] = sorted_data
    return party_data

def extract_min_max(party_data):
    """
    Extracts the minimum and maximum values for each date in the party data.

    Parameters:
    party_data (dict): A dictionary of party data.

    Returns:
    dict: A dictionary of party data with minimum and maximum values for each date.
    """
    for party, data in party_data.items():
        for date, values in data.items():
            min_value = min(values)
            max_value = max(values)
            party_data[party][date] = (min_value, max_value)
    return party_data

def extract_data():
    """
    Extracts and processes the survey data from the website.

    Returns:
    dict: A dictionary containing the processed party data.
    """
    soup = get_soup(survey_url)
    data_rows = extract_rows(soup)
    dates = extract_dates(data_rows)
    party_data_raw, collection_method_data_raw = extract_parties(data_rows)
    party_data = combine_party_with_date(dates, party_data_raw)
    party_data = sort_data(party_data)
    party_data = extract_min_max(party_data)
    return party_data
