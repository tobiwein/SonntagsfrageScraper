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
    for attr, data in new_data.items():
        if attr in old_data:
            old_data[attr].update(data)
        else:
            old_data[attr] = data
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
        existing_data = load_surveyer_data(file)
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

def load_surveyer_data(file):
    """
    Loads party data from the database.

    Parameters:
    file (str): The path to the database file.

    Returns:
    dict: A dictionary of party data.
    """
    with open(file, "r") as f:
        data = f.read()

    # Split data by new line
    data = data.split("\n")

    # Initialize variables
    surveyer_data = {}
    current_date = None
    current_data = {}

    # Parse data
    for line in data:
        # Check if line is empty
        if not line:
            if current_date is not None:
                surveyer_data[current_date] = current_data
                current_data = {}
            continue

        # Split line by colon
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()

        # Check if key is a date
        if key == "dat" and re.match(r"\d{2}\.\d{2}\.\d{4}", value):
            current_date = value
            continue

        # Add data to current data
        current_data[key] = value

    return surveyer_data
