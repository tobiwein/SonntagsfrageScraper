"""
Main script to plot the extracted survey data.
"""

from scripts.v2 import database as db
from scripts.v2 import survey_plotter as plt
from objects.urls import surveyers
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
        surveyer_data = db.load_surveyer_data(surveyers[0]["file"])
        plt.plot_surveyer_data(surveyer_data, party_colors)
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()        
