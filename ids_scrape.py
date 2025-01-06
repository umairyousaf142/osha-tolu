from driver_setup import setup_driver
from csv_handler import save_scraped_data
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime

import pandas as pd

def scrape_activity_ids(naics_code, filename="activity_ids.csv"):
    """Scrape all activity IDs for a given NAICS code on the current date and save them to a CSV."""
    driver = setup_driver()
    all_activity_ids = []

    # Get the current date in the format matching the website (e.g., MM/DD/YYYY)
    current_date = datetime.now().strftime("%m/%d/%Y")
    # current_date = "12/18/2024"

    try:
        driver.get("https://www.osha.gov/pls/imis/industry.html")
        print("Opened OSHA website.")

        # Input NAICS code and submit
        search_box = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "naics"))
        )
        search_box.send_keys(naics_code)
        search_box.send_keys("\n")
        time.sleep(3)

        # Scrape IDs across pages
        while True:
            try:
                rows = driver.find_elements(By.XPATH, "//tbody/tr")
                for row in rows:
                    try:
                        date_cell = row.find_element(By.XPATH, ".//td[4]").text.strip()  # Assuming date is in the 3rd column
                        activity_id = row.find_element(By.XPATH, ".//td/a[@title]").get_attribute("title")

                        if date_cell == current_date:
                            if "." in activity_id and activity_id.replace(".", "").isdigit():
                                all_activity_ids.append(activity_id)
                    except Exception as e:
                        continue
            except Exception as e:
                print(f"Error scraping page: {e}")

            # Navigate to the next page if available
            try:
                next_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[@title='Next Page']"))
                )
                next_button.click()
                time.sleep(3)
            except Exception:
                print("No more pages to scrape.")
                break

        # Save scraped IDs to a CSV file
        pd.DataFrame([{"Activity ID": id} for id in all_activity_ids]).to_csv(
            filename, index=False
        )
        print(f"Scraped {len(all_activity_ids)} IDs. Data saved to {filename}.")

    finally:
        driver.quit()
