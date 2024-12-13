"""

"""

import pandas as pd
import plotly.express as px
from scripts import database as db
from dotenv import load_dotenv
import os

load_dotenv("var.env")
DATA_POINTS = int(os.getenv("DATA_POINTS", 10))

def create_html_from_data(file):
    party_data = db.load_party_data(file)
    
    # Transform the party_data to a format suitable for plotting
    transformed_data = []
    for party, date_data in party_data.items():
        for date, values in date_data.items():
            transformed_data.append({"date": date, "party": party, "min": values[0], "max": values[1]})

    # Convert the transformed data to a DataFrame
    df = pd.DataFrame(transformed_data)

    # Sort the DataFrame by date and get the last X data points
    df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y')
    df = df.sort_values(by='date').tail(DATA_POINTS)

    # Create the plot
    fig = px.line(df, x='date', y=['min', 'max'], color='party', title='Sonntagsfrage Trends')
    fig.write_html('public/index.html')
