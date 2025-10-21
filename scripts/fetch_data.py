import pandas as pd
import time
import requests

def fetch_data(season):
    BASE_URL = "https://www.football-data.co.uk/mmz4281/"
    url = BASE_URL + season + "/E0.csv"

    # Add headers to avoid connection issues
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Retry logic
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print("Downloading season", season, "data from " + url)

            # Use requests to download with headers, then pass to pandas
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()  # Raise error for bad status codes

            # Save the content to a file
            with open("../data/epl_" + season + ".csv", 'wb') as f:
                f.write(response.content)

            # Verify by reading it back
            data = pd.read_csv("../data/epl_" + season + ".csv")
            print(f"Successfully downloaded {len(data)} rows of data")
            break

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print("All retry attempts failed")
                raise

seasons = ["2324", "2425", "2526"]
for s in seasons:
    fetch_data(s)