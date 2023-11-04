import requests
from bs4 import BeautifulSoup
import csv
import os
import time

# Function to scrape data from a single URL
def scrape_url(url):
    if not url.startswith("https://kenh14.vn"):
        fix_url = "https://kenh14.vn" + url
    else:
        fix_url = url

    while True:  # Keep retrying indefinitely
        try:
            # Send an HTTP request to the URL
            response = requests.get(fix_url, timeout=10)
            response.raise_for_status()  # Raise an exception if the response status is not 200

            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')

            # Initialize variables
            id = None
            title = None
            author = None
            date = None
            categories = []

            # Check if the elements exist before accessing them
            title_element = soup.find('h1', class_='kbwc-title')
            if title_element:
                title = title_element.text.strip()

            author_element = soup.find('span', class_='kbwcm-author')
            if author_element:
                author = author_element.text.strip()

            date_element = soup.find('span', class_='kbwcm-time')
            if date_element:
                date = date_element['title']

            categories_elements = soup.find_all('li', class_='kmli active') + soup.find_all('li', class_='kbwsli active')
            for category_element in categories_elements:
                categories.append(category_element.text.strip())

            return {
                'id': id,
                'title': title,
                'author': author,
                'date': date,
                'categories': ', '.join(categories),
                'url': fix_url
            }
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching {url}")
            time.sleep(60)  # Wait for a moment before retrying
            
# Read the URLs from urls.csv and scrape each one
with open('urls.csv', 'r') as url_file, open('dataset.csv', 'w', newline='') as dataset_file:
    url_reader = csv.reader(url_file)
    dataset_writer = csv.DictWriter(dataset_file, fieldnames=['id', 'title', 'author', 'date', 'categories', 'url'])

    # Skip the header row
    next(url_reader)

    dataset_writer.writeheader()

    rows_scraped = 0  # Keep track of the number of rows scraped
    total_rows = sum(1 for _ in url_reader)  # Calculate the total number of rows

    url_file.seek(0)  # Reset the file pointer to read from the beginning (excluding the header)
    next(url_reader)  # Skip the header row again

    for row in url_reader:
        id, url = row
        data = scrape_url(url)

        if data:
            data['id'] = id
            dataset_writer.writerow(data)
            rows_scraped += 1

        # Clear the screen
        os.system('cls' if os.name == 'nt' else 'clear')
        # Calculate and display the percentage progress
        progress = (rows_scraped / total_rows) * 100
        print(f"Progress: {progress:.2f}%")

print("Scraping and saving completed.")