"""

"""

import plotly.express as px
import database as db

df = db.load_party_data('./data/date_data.txt')

fig = px.line(df, x='x', y='y', title='Sonntagsfrage Trends')
fig.write_html('index.html')

print(fig.to_html())
