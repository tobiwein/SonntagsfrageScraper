"""
Main script to extract survey data and plot it.
"""

import survey_scrape
import my_plotter as plt
import logging

logging.basicConfig(level=logging.INFO)

def main():
    try:
        party_data, date_data = survey_scrape.extract_data()
        plt.plot_party_data(party_data)
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()        
