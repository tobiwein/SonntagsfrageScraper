"""
Main script to extract survey data.
"""

from scripts import survey_scrape
from scripts.v2 import survey_scrape as survey_scrape_v2
from scripts import database as db
from dotenv import load_dotenv
import os
import logging

load_dotenv("var.env")
logging.basicConfig(level=logging.INFO)

url = os.getenv("SURVEY_URL")
file = os.getenv("DATABASE_FILE")

def main():
    try:
        survey_scrape_v2.extract_surveyer_data("https://www.wahlrecht.de/umfragen/forsa.htm")
        #party_data = survey_scrape.extract_data(url)
        #db.store_party_data(party_data, file)
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()        
