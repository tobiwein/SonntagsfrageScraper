# Sonntagsfrage Scraper

This project scrapes survey data from the website [wahlrecht.de](https://www.wahlrecht.de/umfragen/) and visualizes it using matplotlib.

## Project Structure

- `scripts/main.py`: Main script to extract survey data and plot it.
- `scripts/my_plotter.py`: Contains functions for plotting party data.
- `scripts/survey_scrape.py`: Contains functions for scraping and processing survey data.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/tobiwein/SonntagsfrageScraper.git
    cd SonntagsfrageScraper/scripts
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

Run the main script to scrape the data and generate the plot:
```sh
python main.py
```

## Example Output

![Example Output](images/readme_example_output.png)

## Functions

### `survey_scrape.py`

- `get_soup(url)`: Fetches the HTML content from the given URL and returns a BeautifulSoup object.
- `extract_rows(soup)`: Extracts the rows from the target table in the BeautifulSoup object.
- `clean_percentages(percentages)`: Cleans and converts percentage strings to float values.
- `extract_parties(data_rows)`: Extracts party data from the rows.
- `extract_dates(data_rows)`: Extracts dates from the first row of the table.
- `combine_party_with_date(dates, party_data)`: Combines party data with corresponding dates.
- `sort_data(party_data)`: Sorts the party data by dates.
- `extract_min_max(party_data)`: Extracts the minimum and maximum values for each date in the party data.
- `transform_to_date_data(party_data)`: Transforms the party data to be indexed by dates.
- `extract_data()`: Extracts and processes the survey data from the website.

### `my_plotter.py`

- `plot_party_data(party_data)`: Plots the party data with filled areas, lines, and average lines.

## License

This project is licensed under the MIT License.
