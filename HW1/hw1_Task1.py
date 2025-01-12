from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

class BingSearchScraper:
    def __init__(self):
        self.driver = self.initialize_driver()

    def initialize_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        return driver

    def search_query(self, query):
        # Navigate to Bing search page with the query
        search_url = f"https://www.bing.com/search?q={'+'.join(query.split())}&count=30"

        print("Processing Query:"+str(search_url)+"...")

        self.driver.get(search_url)
        time.sleep(2)  # Sleep to allow the page to load
        
        # Collect search results
        search_results = self.scrape_search_results()
        
        return search_results
    
    def scrape_search_results(self):
        results = []
        
        # Find all search result elements by the Bing search result selector: 'li.b_algo'
        search_items = self.driver.find_elements(By.XPATH, '//li[@class="b_algo"]')
        
        for item in search_items[:10]:  # Limit to 10 results
            try:
                # Extract the specific <a> tag with class 'tilk' and get the href attribute
                link_element = item.find_element(By.XPATH, './/a[@class="tilk"]')
                link = link_element.get_attribute('href')
                
                if link:  # Ensure the link is valid
                    results.append(link)
            except Exception as e:
                print(f"Error extracting link: {e}")
        
        return results

    def close_driver(self):
        self.driver.quit()

############## Main Script ##############
if __name__ == "__main__":
    # Initialize the Bing Search Scraper
    scraper = BingSearchScraper()

    # Initialize an empty dictionary to store results for all queries
    all_results = {}

    # Open the text file containing the queries
    with open("100QueriesSet1.txt", "r") as file:
        queries = file.readlines()

    query_threshold = 200
    count = 0
    # Loop through each query, strip it of extra whitespace, and fetch results
    for query in queries:
        count += 1

        if count <= query_threshold:
            query = query.strip()  # Remove any leading/trailing whitespace or newlines
            if query:  # Ensure the query is not empty
                search_results = scraper.search_query(query)
                
                # Store the results for the current query
                all_results[query] = search_results
        else:
            break

    # Close the Selenium driver after scraping
    scraper.close_driver()

    # Write all results to a JSON file named Bing_Result1.json
    with open("hw1.json", "w") as json_file:
        json.dump(all_results, json_file, indent=4)  # Save the entire dictionary in JSON format

    print(f"Results for all queries saved to hw1.json")