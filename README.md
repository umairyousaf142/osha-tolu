# Osha-Government-Scrapping

## Overview

This project is designed to scrape activity IDs and details from the OSHA website for various NAICS codes and save the data to Google Sheets. The project uses Selenium for web scraping and the Google Sheets API for data storage.

## Files Description

### `credentials.json`

Contains the Google service account credentials required for accessing the Google Sheets API.

### `csv_handler.py`

Handles reading and updating CSV files with activity IDs and saving scraped data to Google Sheets.

- `update_csv_with_new_ids(input_csv, new_ids)`: Updates the CSV file with new activity IDs.
- `read_activity_ids(input_csv)`: Reads activity IDs from the CSV file.
- `save_scraped_data(output_google_sheet_id, scraped_data)`: Saves the scraped data to a Google Sheet.

### `daily.py`

Runs the `main.py` script at a specified interval using a scheduler.

- `run_main_script()`: Runs the `main.py` script.
- `start_scheduler(interval_minutes)`: Starts the scheduler to run the script at the specified interval.

### `driver_setup.py`

Sets up the Selenium WebDriver with the required options.

- `setup_driver()`: Configures and returns a Selenium WebDriver instance.

### `ids_scrape.py`

Scrapes activity IDs for a given NAICS code from the OSHA website and saves them to a CSV file.

- `scrape_activity_ids(naics_code, filename="activity_ids.csv")`: Scrapes activity IDs and saves them to a CSV file.

### `main.py`

Main script that orchestrates the scraping and data saving process.

- `process_and_update_csv(input_csv, output_google_sheet_id)`: Processes the CSV file and updates the Google Sheet with scraped data.
- `process_all_naics_codes()`: Scrapes activity IDs and details for multiple NAICS codes and updates the corresponding Google Sheets.

### `scraper.py`

Scrapes detailed information for each activity ID from the OSHA website.

- `scrape_details(driver, activity_id)`: Scrapes details for a given activity ID.

## Usage

1. **Setup Google Sheets API Credentials**:

   - Ensure `credentials.json` is correctly configured with your Google service account credentials.

2. **Install Dependencies**:

   - Install the required Python packages using `pip`:
     ```sh
     pip install selenium pandas google-api-python-client google-auth-httplib2 google-auth-oauthlib webdriver-manager beautifulsoup4
     ```

3. **Run the Scheduler**:

   - Execute the [daily.py](http://_vscodecontentref_/8) script to start the scheduler:
     ```sh
     python daily.py
     ```

4. **Manual Execution**:
   - You can manually run the [main.py](http://_vscodecontentref_/9) script to start the scraping process:
     ```sh
     python main.py
     ```

## License

This project is licensed under the MIT License.
