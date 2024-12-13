"""
Main script to transform the data into html for the GitHub page.
"""

from scripts import gh_page as gp
from dotenv import load_dotenv
import os
import logging

load_dotenv("var.env")
logging.basicConfig(level=logging.INFO)

file = os.getenv("DATABASE_FILE")

def main():
    try:
        gp.create_html_from_data(file)
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()        