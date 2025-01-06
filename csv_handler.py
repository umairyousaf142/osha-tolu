import pandas as pd

def update_csv_with_new_ids(input_csv, new_ids):
    try:
        existing_df = pd.read_csv(input_csv)
        existing_ids = set(existing_df["Activity ID"].tolist())
    except FileNotFoundError:
        existing_ids = set()

    updated_ids = existing_ids.union(new_ids)
    updated_df = pd.DataFrame(list(updated_ids), columns=["Activity ID"])
    updated_df.to_csv(input_csv, index=False)
    print(f"Updated input CSV with {len(updated_ids)} IDs.")

def read_activity_ids(input_csv):
    try:
        df = pd.read_csv(input_csv)
        return df["Activity ID"].tolist()
    except FileNotFoundError:
        print(f"No input CSV found at {input_csv}. Starting fresh.")
        return []

from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

def save_scraped_data(output_google_sheet_id, scraped_data):
    # Google Sheets API setup
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = 'credentials.json' 

    credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)

    # Read existing data from the Google Sheet
    try:
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=output_google_sheet_id, range='A1:Z1000').execute()
        existing_data = result.get('values', [])

        # Convert existing data to DataFrame if not empty
        if existing_data:
            existing_df = pd.DataFrame(existing_data[1:], columns=existing_data[0])
        else:
            existing_df = pd.DataFrame()
    except Exception as e:
        print(f"Error reading data from Google Sheet: {e}")
        existing_df = pd.DataFrame()

    # Create a DataFrame from the new scraped data
    new_data_df = pd.DataFrame(scraped_data)

    # Concatenate new data on top of existing data, avoiding duplication
    if not existing_df.empty:
        combined_df = pd.concat([new_data_df, existing_df], ignore_index=True).drop_duplicates()
    else:
        combined_df = new_data_df

    # Prepare data for writing to Google Sheets
    if not combined_df.empty:
        values = [combined_df.columns.tolist()] + combined_df.astype(str).values.tolist()
    else:
        print("No data to write.")
        return

    # Write the combined data back to the Google Sheet
    try:
        body = {'values': values}
        sheet.values().update(
            spreadsheetId=output_google_sheet_id,
            range='A1',
            valueInputOption='RAW',
            body=body
        ).execute()
        print(f"Scraped data successfully saved to Google Sheet with ID {output_google_sheet_id}")
    except Exception as e:
        print(f"Error writing data to Google Sheet: {e}")