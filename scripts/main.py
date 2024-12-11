
from collections import defaultdict
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

import survey_scrape

party_data = survey_scrape.extract_data()

# Extrahiere die Datumszeile und wandle in Datetime-Objekte
dates = [datetime.strptime(datum, "%d.%m.%Y") for datum in extracted_data[0]]

# Indizes der sortierten Daten bestimmen
sorted_indices = sorted(range(len(dates)), key=lambda i: dates[i])

# Sortiere die Daten entsprechend der Datumszeile
sorted_data = [[row[i] for i in sorted_indices] for row in extracted_data]

# Trenne Datum von den Daten
dates = sorted_data.pop(0)

# Füge Parteien als erste Spalte hinzu
def add_parties_to_data(data, parties):
    for i, party in enumerate(parties):
        data[i].insert(0, party)
# add_parties_to_data(sorted_data, parties)

# print(dates)
# # Ausgabe der sortierten Daten
# for row in sorted_data:
#     print(row)


# Daten in ein Dictionary organisieren
aggregated_data = defaultdict(lambda: defaultdict(list))
party_list = defaultdict(list)
for i, party in enumerate(parties):
    party_list[i] = party

def is_number(s):
    try:
        float(s)  # Versucht, den String in einen Float zu konvertieren
        return True
    except ValueError:
        return False

# Daten pro Partei pro Datum in das Dictionary einfügen
for i, date in enumerate(dates):
    for party_index, value in enumerate(extracted_data):
        value_cleaned = value[i].replace('%', '').replace('.', '').replace(',', '.').strip()
        if is_number(value_cleaned) and party_index != 0:
            aggregated_data[date][party_index].append(float(value_cleaned))

# Durchschnitt pro Partei pro Datum berechnen
calc_average = True
average_data = defaultdict(dict)
for date, party_data in aggregated_data.items():
    for party_index, values in party_data.items():
        average = 0
        if calc_average:
            average = sum(values) / len(values)
        else:
            if len(values) == 1:
                average = sum(values) / len(values)
            elif len(values) > 1:
                average = []
                for i, value in enumerate(values):
                    average.append(value)
        average_data[date][party_index-1] = average

print(party_list.items())
print(average_data.items())
# print(aggregated_data.items())
# Ausgabe: Datum mit den Werten aller Parteien
# for date, party_data in average_data.items():
#     print(date, party_data)

party_colors = {
    0: 'black',
    1: 'red',
    2: 'green',
    3: 'yellow',
    4: 'purple',
    5: 'blue',
    6: 'orange',
    7: 'brown'
}

def my_plot():
    for party_index, party in party_list.items():

        party_data = []
        for i, value in average_data.items():
            keys = np.array(list(value.keys()))
            vals = np.array(list(value.values()))

            for key_index, key in enumerate(keys):
                if key == party_index:
                    party_data.append(vals[key_index])
                    break
                if key_index == len(keys)-1:
                    party_data.append(0)

        plt.plot(list(average_data.keys()), party_data, label=party, color=party_colors.get(party_index, 'gray'))

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
            
