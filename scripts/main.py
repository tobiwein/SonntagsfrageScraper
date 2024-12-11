"""
Main script to extract survey data and plot it.
"""

import survey_scrape
import my_plotter as plt
import database as db
import logging

logging.basicConfig(level=logging.INFO)

file = "./data/date_data.txt"

def main():
    try:
        party_data = survey_scrape.extract_data()
        db.store_party_data(party_data, file)
        party_data = db.load_party_data(file)
        plt.plot_party_data(party_data)
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()        
