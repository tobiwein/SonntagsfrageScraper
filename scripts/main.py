"""
Main script to extract survey data and plot it.
"""

import survey_scrape
import my_plotter as plt
import database as db
import logging

logging.basicConfig(level=logging.INFO)

url = "https://www.wahlrecht.de/umfragen/"
file = "./data/date_data.txt"
party_colors = {
    "CDU/CSU": "black",
    "SPD": "red",
    "AfD": "blue",
    "FDP": "yellow",
    "DIE LINKE": "purple",
    "GRUENE": "green",
    "Sonstige": "gray",
    "BSW": "orange",
    "FW": "brown"
} 

def main():
    try:
        party_data = survey_scrape.extract_data(url)
        party_data = db.store_party_data(party_data, file)
        plt.plot_party_data(party_data, party_colors)
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()        
