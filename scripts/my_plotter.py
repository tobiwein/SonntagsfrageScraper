"""
This module contains functions for plotting party data.
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime

# Define party colors
party_colors = {
    "CDU/CSU": "black",
    "SPD": "red",
    "AfD": "blue",
    "FDP": "yellow",
    "DIE LINKE": "purple",
    "GRÜNE": "green",
    "Sonstige": "gray",
    "BSW": "orange",
    "FW": "brown",
}    

def plot_party_data(party_data):
    """
    Plots the party data with filled areas, lines, and average lines.

    Parameters:
    party_data (dict): A dictionary containing party data with dates and percentage ranges.
    """
    plt.figure(figsize=(12, 8))
    plt.title("Sonntagsumfrage")
    plt.xlabel("Datum")
    plt.ylabel("Umfrageergebnis in %")
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.subplots_adjust(left=0.1, bottom=0.2, right=0.9, top=0.9)
    plt.xticks(rotation=45)
    plt.axhspan(0, 5, color='red', alpha=0.2)

    all_dates = set()
    all_percentages = []

    for party, date_data in party_data.items():
        party_color = party_colors.get(party, "gray")
        dates = [datetime.strptime(date, "%d.%m.%Y") for date in date_data.keys()]
        all_dates.update(dates)
        min_percentage = []
        max_percentage = []
        avg_percentage = []

        for date, percentage_range in date_data.items():
            min_percentage.append(min(percentage_range))
            max_percentage.append(max(percentage_range))
            avg_percentage.append(np.mean(percentage_range))
            all_percentages.extend(percentage_range)

        latest_percentage = list(date_data.values())[-1]
        if (latest_percentage[0] == latest_percentage[1]):
            latest_percentage = latest_percentage[0]
        
        label = f"{party} ({latest_percentage}%)"

        plt.fill_between(dates, min_percentage, max_percentage, color=party_color, alpha=0.3, zorder=2)
        plt.plot(dates, min_percentage, color=party_color, alpha=1.0, linewidth=1, marker='o', markersize=4, zorder=3)
        plt.plot(dates, max_percentage, color=party_color, alpha=1.0, linewidth=1, marker='o', markersize=4, label=label, zorder=3)
        plt.plot(dates, avg_percentage, color=party_color, alpha=1.0, linewidth=1, linestyle='--', marker='x', markersize=4, zorder=3)

    sorted_dates = sorted(all_dates)
    plt.xlim(sorted_dates[0], sorted_dates[-1])
    plt.ylim(0, max(all_percentages) + 5)

    # Add horizontal dashed lines at every integer step on the y-axis
    for y in range(1, int(max(all_percentages)) + 5):
        linewidth = 0.5
        if y % 10 == 0:
            linewidth = 1.5
        elif y % 5 == 0:
            linewidth = 1
        plt.axhline(y=y, color='gray', linestyle='--', linewidth=linewidth, zorder=1)

    # Add vertical lines for each date where data is available
    for date in sorted_dates:
        plt.axvline(x=date, color='gray', linestyle='--', linewidth=0.5, zorder=1)

    # Format the x-axis to show dates nicely
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    plt.gca().xaxis.set_minor_locator(mdates.WeekdayLocator())
    plt.gca().xaxis.set_minor_formatter(mdates.DateFormatter('%d'))

    # Ensure that the x-axis ticks are set correctly
    plt.gca().set_xticks(sorted_dates)
    plt.gca().set_xticklabels([date.strftime('%d.%m.%Y') for date in sorted_dates], rotation=45)

    plt.legend(loc='upper left', bbox_to_anchor=(1, 1), borderaxespad=0.)
    plt.tight_layout()
    plt.show()
