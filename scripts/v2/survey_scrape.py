"""
This module contains functions to scrape survey data from the website https://www.wahlrecht.de/umfragen/.
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging

from objects.html import attributes

logging.basicConfig(level=logging.INFO)

# Mapping of party names to attribute names

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

def extract_surveyer_data_table(soup):
    """
    Extracts the table head and body from the surveyer data table.

    Parameters:
    soup (BeautifulSoup): The BeautifulSoup object containing the parsed HTML content.

    Returns:
    tuple: A tuple containing the table head and body (BeautifulSoup objects).
    """
    data_table = soup.find("table")
    if data_table is None:
        logging.error("No table found")
        raise Exception("No table found")

    data_table_head = soup.find("thead")
    if data_table_head is None:
        logging.error("No table head found")
        raise Exception("No table head found")

    data_table_body = soup.find("tbody")
    if data_table_body is None:
        logging.error("No table body found")
        raise Exception("No table body found")

    return data_table_head, data_table_body

def extract_surveyer_data_from_header(table_head):
    """
    Extracts the attribute list from the table head.

    Parameters:
    table_head (BeautifulSoup): The table head (BeautifulSoup object).

    Returns:
    list: A list of attribute strings.
    """
    headers = table_head.find_all("th")
    if headers is None:
        logging.error("No headers found")
        raise Exception("No headers found")
    

    attribute_list = []
    for header in headers:
        header_classes = header.attrs.get("class")
        if header_classes is None:
            if header.find("a") is not None:
                party_name = header.find("a").get_text()
                attribute_list.append(attributes[party_name])
            else:
                logging.warning("No header class found")
                attribute_list.append("unknown")
        else:
            header_class = header_classes[0]
            if header_class == "part":
                party_name = header.get_text()
                attribute_list.append(attributes[party_name])
                continue

            attribute = attributes[header_class]
            if attribute is None:
                logging.warning(f"Unknown header class: {header_class}")
                attribute_list.append("unknown")
            else:
                if header_class == "dat2" and header.get_text() != "Zeitraum":
                    attribute = attributes["non"]
                attribute_list.append(attribute)

    return attribute_list

def extract_surveyer_data_from_body(table_body, header_data):
    """
    Extracts the surveyer data from the table body.

    Parameters:
    table_body (BeautifulSoup): The table body (BeautifulSoup object).
    header_data (list): A list of attribute strings.

    Returns:
    dict: A dictionary containing the surveyer data.
    """
    body_rows = table_body.find_all("tr")
    body_data = {}
    for body_row in body_rows:
        cells = body_row.find_all("td")
        row_data = {}
        if len(cells) != len(header_data):
            logging.warning("Number of cells does not match number of headers")
            continue

        for index, cell in enumerate(cells):
            attribute = header_data[index]
            cell_text = cell.get_text()
            if attribute == "publication_date":
                try:
                    datetime.strptime(cell_text, "%d.%m.%Y")
                    row_data[attribute] = cell_text
                except ValueError:
                    logging.warning(f"Invalid date format: {cell_text}")
                    break

            elif attribute.startswith("party-") or attribute == "non":
                cell_text = cell_text.replace(",", ".").replace("%", "").strip()
                if cell_text == "–" or cell_text == "":
                    cell_text = "0"
                try:
                    percentage = float(cell_text)
                    row_data[attribute] = percentage
                except ValueError:
                    logging.warning(f"Could not convert {cell_text} to float")
                    row_data[attribute] = 0

            elif attribute == "surveyed_count":
                survey_type = "standard"
                if cell.find("a") is not None:
                    cell_a_tag = cell.find("a")
                    cell_a_tag_text = cell_a_tag.get_text()
                    if cell_a_tag_text  == "O":
                        survey_type = "online"
                        cell_text = cell_text.replace("O", "").replace("•", "").strip()
                    elif cell_a_tag_text == "T":
                        survey_type = "telephone"
                        cell_text = cell_text.replace("T", "").replace("•", "").strip()
                    elif cell_a_tag_text == "P":
                        survey_type = "personal"
                        cell_text = cell_text.replace("P", "").replace("•", "").strip()
                    elif cell_a_tag_text == "TOM":
                        survey_type = "telephone_online_mix"
                        cell_text = cell_text.replace("TOM", "").replace("•", "").strip()
                        
                try:
                    surveyed_count = int(cell_text.replace(".", "").strip())
                    row_data[attribute] = {"count": surveyed_count, "type": survey_type}
                except ValueError:
                    logging.warning(f"Could not convert {cell_text} to int")
                    row_data[attribute] = 0

            elif attribute == "collection_period":
                try:
                    start_date, end_date = cell_text.split("–")
                except ValueError:
                    start_date = end_date = cell_text

                try:
                    start_date = datetime.strptime(start_date.strip(), "%d.%m.")
                    end_date = datetime.strptime(end_date.strip(), "%d.%m.")
                    average_date = start_date + (end_date - start_date) / 2
                    row_data[attribute] = {"start": start_date, "end": end_date, "average": average_date}
                except ValueError:
                    logging.warning(f"Invalid date format: {cell_text}")
                    row_data[attribute] = {"start": None, "end": None, "average": None}

        body_data[row_data["publication_date"]] = row_data

    # Sort body_data by publication_date which is in format dd.mm.yyyy
    body_data = dict(sorted(body_data.items(), key=lambda x: datetime.strptime(x[0], "%d.%m.%Y"), reverse=True))
    return body_data

def extract_surveyer_data(url):
    """
    Extracts surveyer data from the given URL.

    Parameters:
    url (str): The URL to fetch the surveyer data from.

    Returns:
    dict: A dictionary containing the surveyer data.
    """
    soup = get_soup(url)
    table_head, table_body = extract_surveyer_data_table(soup)
    header_data = extract_surveyer_data_from_header(table_head)
    body_data = extract_surveyer_data_from_body(table_body, header_data)
    return body_data
