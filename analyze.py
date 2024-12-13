"""
Main script to plot the extracted survey data.
"""

from scripts import database as db
from scripts import my_plotter as plt
from dotenv import load_dotenv
import os
import logging

load_dotenv("var.env")
logging.basicConfig(level=logging.INFO)

file = os.getenv("DATABASE_FILE")
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
        party_data = db.load_party_data(file)
        plt.plot_party_data(party_data, party_colors)
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()        
