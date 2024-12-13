"""
This script is responsible for creating the HTML file that is used to display the data on the GitHub page.
"""

import pandas as pd
import plotly.express as px
from scripts import database as db
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv("var.env")
DATA_POINTS = int(os.getenv("DATA_POINTS", 10))

def create_html_from_data(file):
    party_data = db.load_party_data(file)
    
    # Transform the party_data to a format suitable for plotting
    transformed_data = []
    for party, date_data in party_data.items():
        for date, values in date_data.items():
            transformed_data.append({"date": date, "party": party, "percentage": (values[0] + values[1]) / 2})

    # Convert the transformed data to a DataFrame
    df = pd.DataFrame(transformed_data)

    # Sort the DataFrame by date and get the last X unique dates
    df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y')
    unique_dates = df['date'].drop_duplicates().nlargest(DATA_POINTS)
    df = df[df['date'].isin(unique_dates)]
    df = df.sort_values(by='date')

    # Get the date of the last update
    last_update = datetime.now().strftime('%d.%m.%Y %H:%M:%S')

    # Create the plot
    fig = px.line(df, x='date', y='percentage', color='party', title=f'Sonntagsfrage trends (Last update: {last_update})',
                 labels={'date': 'Date', 'value': 'Percentage', 'party': 'Party'},)
    fig.write_html('docs/index.html')
