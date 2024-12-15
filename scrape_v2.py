"""
Main script to extract survey data.
"""

from scripts.v2 import survey_scrape
from scripts.v2 import database as db
from dotenv import load_dotenv
import os
import logging

load_dotenv("var.env")
logging.basicConfig(level=logging.INFO)

url = os.getenv("SURVEY_URL")
file = os.getenv("DATABASE_FILE")

surveyer_urls = [
    {"name": "Allensbach", "url": "https://www.wahlrecht.de/umfragen/allensbach.htm"},
    {"name": "Verian (Emnid)", "url": "https://www.wahlrecht.de/umfragen/emnid.htm"},
    {"name": "Forsa", "url": "https://www.wahlrecht.de/umfragen/forsa.htm"},
    {"name": "Forschungsgruppe Wahlen", "url": "https://www.wahlrecht.de/umfragen/politbarometer.htm"},
    {"name": "GMS", "url": "https://www.wahlrecht.de/umfragen/gms.htm"},
    {"name": "Infratest dimap", "url": "https://www.wahlrecht.de/umfragen/dimap.htm"},
    {"name": "INSA", "url": "https://www.wahlrecht.de/umfragen/insa.htm"},    
    {"name": "YouGov", "url": "https://www.wahlrecht.de/umfragen/yougov.htm"},
]

def main():
    try:
        for surveyer in surveyer_urls:
            surveyer_name = surveyer["name"]
            logging.info(f"Extracting data from {surveyer_name}...")
            surveyer_data = survey_scrape.extract_surveyer_data(surveyer["url"])
            print(surveyer_data)
            #db.store_surveyer_data(surveyer_data, f"./data/v2/{surveyer_name}.txt")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()        
