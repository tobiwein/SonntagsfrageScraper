"""
Main script to extract survey data.
"""

from scripts.v2 import survey_scrape
from scripts.v2 import database as db
from objects.urls import surveyers
from dotenv import load_dotenv
import os
import logging

load_dotenv("var.env")
logging.basicConfig(level=logging.INFO)

url = os.getenv("SURVEY_URL")
file = os.getenv("DATABASE_FILE")

def main():
    try:
        for surveyer in surveyers:
            surveyer_name = surveyer["name"]
            logging.info(f"Extracting data from {surveyer_name}...")
            surveyer_data = survey_scrape.extract_surveyer_data(surveyer["url"])
            db.store_surveyer_data(surveyer_data, surveyer["file"])
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()        
