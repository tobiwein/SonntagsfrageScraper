"""
This module contains functions for interacting with the database.
"""

def transform_to_date_data(party_data):
    """
    Transforms the party data to be indexed by dates.

    Parameters:
    party_data (dict): A dictionary of party data.

    Returns:
    dict: A dictionary of data indexed by dates.
    """
    date_data = {}
    for party, data in party_data.items():
        for date, values in data.items():
            if date_data.get(date) is None:
                date_data[date] = {}
            date_data[date][party] = values
    return date_data

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

def store_party_data(party_data, file):
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
    combined_data = merge_party_data(existing_data, party_data)

    # Transform data to be indexed by dates
    date_data = transform_to_date_data(combined_data)

    # Save combined data
    with open(file, "w") as f:
        for date, data in date_data.items():
            f.write(f"{date}\n")
            for party, values in data.items():
                f.write(f"{party}: {values}\n")

    return combined_data

def load_party_data(file):
    """
    Loads party data from the database.

    Parameters:
    file (str): The path to the database file.

    Returns:
    dict: A dictionary of party data.
    """
    party_data = {}
    with open(file, "r") as f:
        for line in f:
            if ":" in line:
                party, values = line.strip().split(": ")
                if party_data.get(party) is None:
                    party_data[party] = {}
                party_data[party][date] = eval(values)
            else:
                date = line.strip()
    return party_data
