
from collections import defaultdict
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

import survey_scrape

party_data = survey_scrape.extract_data()



party_data = []
latest_percentage_points = {}  # Dictionary to store the latest percentage points for each party

for i, value in average_data.items():
    keys = np.array(list(value.keys()))
    vals = np.array(list(value.values()))

    for key_index, key in enumerate(keys):
        if key == party_index:
            party_data.append(vals[key_index])
            latest_percentage_points[party] = vals[key_index]  # Store the latest percentage point
            break
        if key_index == len(keys)-1:
            party_data.append(0)
            latest_percentage_points[party] = 0  # Store 0 if no data is found

    plt.plot(list(average_data.keys()), party_data, label=party, color=party_colors.get(party_index, 'gray'))

# Add text annotations for the latest percentage points
for party, percentage in latest_percentage_points.items():
    plt.text(dates[-1], percentage, f'{percentage:.1f}%', fontsize=9, verticalalignment='bottom')



plt.figure(figsize=(10, 6))
plt.grid(True)
plt.xlim(dates[0], dates[-1])
plt.ylim(0)
plt.subplots_adjust(left=0.1, bottom=0.2, right=0.8, top=0.9)
plt.title("Sonntagsumfrage")
plt.xlabel("Datum")
plt.ylabel("Umfrageergebnis in %")
plt.xticks(rotation=45)
# Bereich unter 5 % rot einfärben
plt.axhspan(0, 5, color='red', alpha=0.2)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
plt.show()
            
