import requests
from bs4 import BeautifulSoup
import urllib.parse
import random
import time
from dotenv import load_dotenv
import os

load_dotenv()

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
]

PROXY = os.getenv("PROXY")

def scrape_bing(query, retries=5):
    # Set up headers to mimic a browser
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.bing.com/"
    }

    # URL-encode the query string
    encoded_query = urllib.parse.quote(query)

    # Bing search URL with the encoded query
    url = f"https://www.bing.com/search?q={encoded_query}"

    proxies = {
        "http": PROXY,
        "https": PROXY
    } if PROXY else None

    results_list = []
    for attempt in range(retries):
        try:
            # Make the request
            response = requests.get(url, headers=headers, proxies=proxies, timeout=10)

            # Check the response status
            if response.status_code == 200:
                # Parse the HTML content
                soup = BeautifulSoup(response.text, 'html.parser')
                results = soup.select('.b_algo')  # Bing's class for search results

                # Iterate over results and collect title, link, and description
                for result in results:
                    try:
                        title = result.select_one('h2').text
                        link_tag = result.select_one('a')
                        link = link_tag['href'] if link_tag and 'href' in link_tag.attrs else "Not available"
                        description = result.select_one('.b_caption p')  # Select description
                        description_text = description.text if description else "Not available"
                        
                        results_list.append({
                            "title": title,
                            "link": link,
                            "description": description_text
                        })
                    except AttributeError:
                        # Handle cases where the expected elements are not found
                        continue

                return results_list
            elif response.status_code == 429:
                # Too many requests, wait and retry
                wait_time = 2 ** attempt
                print(f"Rate limited. Waiting for {wait_time} seconds before retrying...")
                time.sleep(wait_time)
            else:
                print(f"Failed to fetch results. Status Code: {response.status_code}")
                return {"error": f"Failed to fetch results. Status Code: {response.status_code}"}
        except (requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout):
            print(f"Request failed. Retrying...")

    return {"error": "All retries failed. Unable to fetch results."}
