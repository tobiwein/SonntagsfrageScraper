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

surveyers = [
    {"name": "Allensbach", "url": "https://www.wahlrecht.de/umfragen/allensbach.htm", "file": "./data/surveyer/allensbach.txt"},
    {"name": "Verian (Emnid)", "url": "https://www.wahlrecht.de/umfragen/emnid.htm", "file": "./data/surveyer/emnid.txt"},
    {"name": "Forsa", "url": "https://www.wahlrecht.de/umfragen/forsa.htm", "file": "./data/surveyer/forsa.txt"},
    {"name": "Forschungsgruppe Wahlen", "url": "https://www.wahlrecht.de/umfragen/politbarometer.htm", "file": "./data/surveyer/politbarometer.txt"},
    {"name": "GMS", "url": "https://www.wahlrecht.de/umfragen/gms.htm", "file": "./data/surveyer/gms.txt"},
    {"name": "Infratest dimap", "url": "https://www.wahlrecht.de/umfragen/dimap.htm", "file": "./data/surveyer/dimap.txt"},
    {"name": "INSA", "url": "https://www.wahlrecht.de/umfragen/insa.htm", "file": "./data/surveyer/insa.txt"},    
    {"name": "YouGov", "url": "https://www.wahlrecht.de/umfragen/yougov.htm", "file": "./data/surveyer/yougov.txt"},
]

def main():
    try:
        for surveyer in surveyers:
            surveyer_name = surveyer["name"]
            logging.info(f"Extracting data from {surveyer_name}...")
            surveyer_data = survey_scrape.extract_surveyer_data(surveyer["url"])
            print(surveyer_data)
            #db.store_surveyer_data(surveyer_data, surveyer["file"])
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()        
