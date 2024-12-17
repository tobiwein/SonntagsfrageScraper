"""
Main script to extract survey data.
"""

from scripts.v1 import survey_scrape
from scripts.v1 import database as db
from dotenv import load_dotenv
import os
import logging

load_dotenv("var.env")
logging.basicConfig(level=logging.INFO)

url = os.getenv("SURVEY_URL")
file = os.getenv("DATABASE_FILE")

def main():
    try:
        party_data = survey_scrape.extract_data(url)
        db.store_party_data(party_data, file)
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()        
