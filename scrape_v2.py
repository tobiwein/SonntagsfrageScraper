"""
Main script to extract survey data.
"""

from scripts.v2 import survey_scrape
from scripts.v2 import database as db
from objects.urls import surveyers
import argparse
from dotenv import load_dotenv
import os
import logging

load_dotenv("var.env")
logging.basicConfig(level=logging.INFO)

url = os.getenv("SURVEY_URL")
file = './data/survey_data.txt'

def scrape_survey_data(args):
    surveyer_count = len(surveyers)
    logging.info(f"Extracting data from {surveyer_count} surveyers.")

    for index, surveyer in enumerate(surveyers):

        logging.info("-" * 50)
        surveyer_name = surveyer["name"]
        surveyer_file = surveyer["file"]
        current_count = f"[{index + 1}/{surveyer_count}]"

        logging.info(f"{current_count} Extracting data from {surveyer_name}.")
        surveyer_data = survey_scrape.extract_surveyer_data(surveyer["url"])
        logging.info(f"{current_count} Data extracted from {surveyer_name}.")

        logging.info(f"{current_count} Inserting data from {surveyer_name} into database.")
        #db.store_surveyer_data(surveyer_data, surveyer["file"])
        logging.info(f"{current_count} Data from {surveyer_name} inserted into database file '{surveyer_file}'.")

    logging.info("-" * 50)
    if args.combine:
        logging.info("Combining data from all surveyers.")
        db.combine_surveyer_data(surveyer_data, file)
        logging.info(f"Data combined and stored in database file '{file}'.")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Scrape and process survey data.")
    parser.add_argument("--combine", action="store_true", help="Combine data from multiple sources")
    args = parser.parse_args()
    
    try:
        scrape_survey_data(args)
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()        
