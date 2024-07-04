from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
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
for information, url in url_dict.items():

    driver = webdriver.Chrome(options=options)

    # Open the web page
    driver.get(url)

    # Wait for cookies button to appear
    accept_cookies_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'onetrust-accept-btn-handler'))
    )
    print("--SUCCESS-- Cookies button located.")


    # Accept cookies
    accept_cookies_button.click()
    print("--SUCCESS-- Cookies button clicked.")


    # # Find elements to iterate over
    items_listed = driver.find_elements(By.CLASS_NAME, "listing-product")
    print(f"Number of items listed: {len(items_listed)}")

    # Set up dictionary to store data
    product_data = []

    # Iterate through listed elements to scrape data
    for item in items_listed:
        name = item.find_element(By.CLASS_NAME, "listing-product-title").text
        price = item.find_element(By.CLASS_NAME, "price").text
        details = item.find_element(By.CLASS_NAME, "listing-key-selling-points").text
        
        product_data.append({
        "product_name": name,
        "product_price": price,
        "product_details": details
        })
        
    data_set["computer_parts"][information] = product_data
    # Exit
    driver.quit()

#Write to json format for storage
json_data = json.dumps(data_set)
with open("./data/product_details", "w") as f:
    f.write(json_data)

# #<--------------------------------------------------------------------------------------------------------------------------------------->


# Time Program End.
end_time = datetime.now()

# Format Time.
time = (end_time - start_time)
total_seconds = time.total_seconds()
milliseconds = time.microseconds / 1000000
formatted_duration = "{:.2f} seconds".format(total_seconds + milliseconds)
#Write test time to file.
with open("web-scraper/testing/testing_times/driver_time.txt", "a") as file:
    file.write(formatted_duration + "\n")