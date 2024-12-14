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
            average_percentage = (values[0] + values[1]) / 2
            uncertainty = abs(values[0] - values[1])
            transformed_data.append({"date": date, "party": party, "percentage": average_percentage, "uncertainty": uncertainty})

    # Convert the transformed data to a DataFrame
    df = pd.DataFrame(transformed_data)

    # Sort the DataFrame by date and get the last X unique dates
    df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y')
    unique_dates = df['date'].drop_duplicates().nlargest(DATA_POINTS)
    df = df[df['date'].isin(unique_dates)]
    df = df.sort_values(by='date')

    # Get the date of the last update
    last_update = datetime.now().strftime('%d.%m.%Y %H:%M:%S')

    # Get the latest percentage for each party
    latest_percentages = df.sort_values('date').groupby('party').last().reset_index()
    df = df.merge(latest_percentages[['party', 'percentage']], on='party', suffixes=('', '_latest'))
    df['party'] = df.apply(lambda row: f"{row['party']} ({row['percentage_latest']:.1f}%)", axis=1)

    # Create the plot
    fig = px.line(df, x='date', y='percentage', text='percentage', color='party', title=f'Sonntagsfrage (Last update: {last_update})',
                 labels={'date': 'Date', 'value': 'Percentage', 'party': 'Party'},
                 markers=True, error_y='uncertainty', textposition='top center')

    # Add red background below y = 5
    fig.add_shape(
        type="rect",
        x0=df["date"].min(),
        x1=df["date"].max(),
        y0=0,
        y1=5,
        fillcolor="red",
        opacity=0.2,
        layer="below"
    )
    fig.write_html('docs/index.html')
