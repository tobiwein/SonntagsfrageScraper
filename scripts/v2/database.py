"""
This module contains functions for interacting with the database.
"""

import re

from objects.html import attributes

def merge_party_data(old_data, new_data):
    """
    Merges new party data with the existing party data.

    Parameters:
    old_data (dict): The existing party data.
    new_data (dict): The new party data to be merged.

    Returns:
    dict: The merged party data.
    """
    for party, data in new_data.items():
        if party not in old_data:
            old_data[party] = data
        else:
            for date, values in data.items():
                old_data[party][date] = values
    return old_data

def store_surveyer_data(surveyer_data, file):
    """
    Stores party data in the database.

    Parameters:
    party_data (dict): A dictionary of party data.
    file (str): The path to the database file.
    """
    # Load existing data
    try:
        existing_data = load_party_data(file)
    except FileNotFoundError:
        existing_data = {}

    # Merge new data with existing data
    combined_data = surveyer_data
    #combined_data = merge_party_data(existing_data, surveyer_data)
    
    # Save combined data
    with open(file, "w") as f:
        for date, data in combined_data.items():
            for attribute, value in data.items():
                if attribute in attributes.values():
                    key = list(attributes.keys())[list(attributes.values()).index(attribute)]
                    f.write(f"{key}: {value}\n")
            f.write("\n")

    return combined_data

def load_party_data(file):
    """
    Loads and cleans party data from the database.

    Parameters:
    file (str): The path to the database file.

    Returns:
    dict: A dictionary of cleaned party data.
    """
    party_data = {}
    date_pattern = r"\d{2}\.\d{2}\.\d{4}"  # Regex for DD.MM.YYYY format
