from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException 
from datetime import datetime
import time
import json

# Time Program Start
start_time = datetime.now()

# Initialize the WebDriver
options = webdriver.ChromeOptions()
options.headless = False
options.add_argument("--disable-cookies")
options.add_argument('--disable-notifications')


url_dict = {
            "cpu_intel": "https://www.ebuyer.com/store/Components/cat/Processors-Intel",
            "cpu_amd": "https://www.ebuyer.com/store/Components/cat/Processors-AMD",
            "graphics_cards_amd": "https://www.ebuyer.com/store/Components/cat/Graphics-Cards-AMD",
            "graphics_cards_nvidia": "https://www.ebuyer.com/store/Components/cat/Graphics-Cards-Nvidia",
            "memory_laptops": "https://www.ebuyer.com/store/Components/cat/Memory---Laptop",
            "memory_computers": "https://www.ebuyer.com/store/Components/cat/Memory---PC",
            "motherboards_amd": "https://www.ebuyer.com/store/Components/cat/Motherboards-AMD",
            "motherboards_intel": "https://www.ebuyer.com/store/Components/cat/Motherboards-Intel",
            "power_supplies": "https://www.ebuyer.com/store/Components/cat/Power-Supplies"
            }
data_set = {"computer_parts": {}}

# Function to iterate and store items
def iterate_and_store_items(driver, data_set, information, page_count):

    # Find elements to iterate over
    items_listed = driver.find_elements(By.CLASS_NAME, "listing-product")
    print(f"Number of items listed on page {page_count}: {len(items_listed)}")

    # Set up dictionary to store data
    product_data = []

    for item in items_listed:
        name = item.find_element(By.CLASS_NAME, "listing-product-title").text
        price = item.find_element(By.CLASS_NAME, "price").text
        details_element = item.find_elements(By.CLASS_NAME, "listing-key-selling-points")
        if details_element:
            details = details_element[0].text
        else:
            details = "Details not available"

        product_data.append({
            "product_name": name,
            "product_price": price,
            "product_details": details
        })

    if page_count == 1:
        data_set["computer_parts"][information] = product_data
    else:
        data_set["computer_parts"][information].extend(product_data)

# Iterate through each category in url_dict
for information, url in url_dict.items():

    page_count = 1

    while True:
        # Initialize WebDriver for each page
        driver = webdriver.Chrome(options=options)

        # Open the web page and check page count, append page count to url if > 1
        if page_count == 1:
            driver.get(url)
        else:
            driver.get(f"{url}?page={page_count}")

        time.sleep(1)

        # Wait for cookies button to appear and click it
        accept_cookies_button = WebDriverWait(driver, 7).until(
            EC.presence_of_element_located((By.ID, 'onetrust-accept-btn-handler'))
        )
        print("--SUCCESS-- Cookies button located.")

        accept_cookies_button.click()
        print("--SUCCESS-- Cookies button clicked.")

        # Call function to iterate over and store items
        iterate_and_store_items(driver, data_set, information, page_count)

        # Locate the next page button and pass through, add to page count
        try:
            next_page_button = driver.find_element(By.CLASS_NAME, "glyphicon-chevron-right")
            
            print(f"--SUCCESS-- Proceeding to page {page_count + 1}")
            page_count += 1
            driver.quit()
            
        except Exception as error:
            print(f"--ERROR-- No more pages found: Error: {error}")
            driver.quit()
            break

print(data_set)

# Write to json format for storage
json_data = json.dumps(data_set, indent=4)
path = "./data/product_details.json" 
with open(path, "w") as f:
    f.write(json_data)

# Time Program End.
end_time = datetime.now()

# Format Time.
time = (end_time - start_time)
total_seconds = time.total_seconds()
milliseconds = time.microseconds / 1000000
formatted_duration = "{:.2f} seconds".format(total_seconds + milliseconds)
# Write test time to file.
with open("web-scraper/testing/testing_times/driver_time.txt", "a") as file:
    file.write(formatted_duration + "\n")