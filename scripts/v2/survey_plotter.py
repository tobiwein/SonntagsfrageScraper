"""
This module contains functions for plotting surveyer data.
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dotenv import load_dotenv
from datetime import datetime
import numpy as np
import os

load_dotenv("var.env")
title = os.getenv("PLOT_TITLE")
xlabel = os.getenv("PLOT_X_LABEL")
ylabel = os.getenv("PLOT_Y_LABEL")

def plot_surveyer_data(surveyer_data, party_colors):
    
    plt.figure(figsize=(12, 8))
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.subplots_adjust(left=0.1, bottom=0.2, right=0.9, top=0.9)
    plt.xticks(rotation=45)
    plt.axhspan(0, 5, color='red', alpha=0.2)

    for date, data in surveyer_data.items():
        for party, value in data.items():
            if party in party_colors:
                plt.plot(date, value, 'o', color=party_colors[party], label=party)


    plt.legend(loc='upper left', bbox_to_anchor=(1, 1), borderaxespad=0.3)
    plt.tight_layout()
    plt.show()
