from ids_scrape import scrape_activity_ids  
from driver_setup import setup_driver
from scraper import scrape_details
from csv_handler import read_activity_ids, save_scraped_data, update_csv_with_new_ids

def process_and_update_csv(input_csv, output_excel):
    activity_ids = read_activity_ids(input_csv)

    driver = setup_driver()
    scraped_data = []

    try:
        for activity_id in activity_ids:
            details = scrape_details(driver, activity_id)
            scraped_data.append(details)
        update_csv_with_new_ids(input_csv, [])
    finally:
        driver.quit()

    save_scraped_data(output_excel, scraped_data)

def process_and_update_csv(input_csv, output_google_sheet_id):
    # Read the activity IDs from the input CSV file
    activity_ids = read_activity_ids(input_csv)

    driver = setup_driver()
    scraped_data = []

    try:
        # Loop through each activity ID and scrape its details
        for activity_id in activity_ids:
            details = scrape_details(driver, activity_id)
            scraped_data.append(details)
        
        # Clear the existing CSV data since it's now processed
        update_csv_with_new_ids(input_csv, [])

    finally:
        driver.quit()

    # Call save_scraped_data with only two arguments (Google Sheet ID and scraped data)
    save_scraped_data(output_google_sheet_id, scraped_data)



def process_all_naics_codes():
    naics_codes = [
        {"code": "3321", "filename": "forging_and_stamping.csv"},
        {"code": "3322", "filename": "cutlery_and_handtool.csv"},
        {"code": "3323", "filename": "architectural_and_structural_metals.csv"},
        {"code": "3324", "filename": "boiler_tank_and_shipping_container.csv"},
        {"code": "3325", "filename": "hardware_manufacturing.csv"},
        {"code": "3326", "filename": "spring_and_wire_product.csv"},
        {"code": "3327", "filename": "machine_shops_and_fasteners.csv"},
        {"code": "3328", "filename": "coating_and_heat_treating.csv"},
        {"code": "3329", "filename": "other_fabricated_metal.csv"},
    ]

    # Start scraping for each NAICS code
    print("Starting the scraping process for multiple NAICS codes...")
    for entry in naics_codes:
        try:
            naics_code = entry["code"]
            filename = entry["filename"]
            print(f"Scraping data for NAICS code {naics_code}...")
            scrape_activity_ids(naics_code=naics_code, filename=filename)  # Scrape IDs first
            print(f"Scraping completed for NAICS code {naics_code}. Data saved to {filename}.")

            # Now process each CSV file and update corresponding Google Sheets
            input_csv = filename
            output_google_sheet_id = "1CDSVQlU513yYt-LEPpkII4iJAiuuua1zxcZ01ew7PMY"  # Your Google Sheet ID
            print(f"Processing and updating Google Sheet for {filename}...")
            process_and_update_csv(input_csv, output_google_sheet_id)

        except Exception as e:
            print(f"An error occurred for NAICS code {naics_code}: {e}")

    print("All scraping processes completed.")

if __name__ == "__main__":
    process_all_naics_codes()
