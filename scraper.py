from bs4 import BeautifulSoup
import time

def scrape_details(driver, activity_id):
    url = f"https://www.osha.gov/ords/imis/establishment.inspection_detail?id={activity_id}"
    driver.get(url)
    print(f"Fetching data for ID: {activity_id}")
    time.sleep(3)  # Wait for the page to load

    details = {"Activity ID": activity_id}

    try:
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract details
        details['Inspection Nr'] = soup.find('strong', text='Inspection Nr').find_next_sibling(text=True).strip() if soup.find('strong', text='Inspection Nr') else "Not Found"
        details['Report ID'] = soup.find('strong', text='Report ID').find_next_sibling(text=True).strip() if soup.find('strong', text='Report ID') else "Not Found"
        details['Date Opened'] = soup.find('strong', text='Date Opened').find_next_sibling(text=True).strip() if soup.find('strong', text='Date Opened') else "Not Found"

        # Extract Site Address
        site_address_tag = soup.find('strong', text='Site Address')
        details['Site Address'] = "\n".join(
            line.strip() for line in site_address_tag.find_parent('p').stripped_strings if line not in ["Site Address", ":"]
        ) if site_address_tag else "Not Found"

        # Extract Mailing Address
        mailing_address_tag = soup.find('strong', text='Mailing Address')
        details['Mailing Address'] = "\n".join(
            line.strip() for line in mailing_address_tag.find_parent('p').stripped_strings if line not in ["Mailing Address", ":"]
        ) if mailing_address_tag else "Not Found"

        # Extract other fields
        fields = ['Union Status', 'NAICS', 'Inspection Type', 'Scope', 'Advanced Notice',
                  'Ownership', 'Safety/Health', 'Close Conference', 'Emphasis', 'Case Closed']
        for field in fields:
            try:
                details[field] = soup.find('strong', text=field).find_next_sibling(text=True).strip()
            except AttributeError:
                details[field] = "Not Found"

    except Exception as e:
        print(f"Error fetching data for ID {activity_id}: {e}")
        details['Error'] = str(e)

    return details
