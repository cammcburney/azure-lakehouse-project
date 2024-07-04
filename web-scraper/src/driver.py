from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import time

# Time Program Start
start_time = datetime.now()

# Initialize the WebDriver
options = webdriver.ChromeOptions()
options.headless = False
options.add_argument("--disable-cookies")
options.add_argument('--disable-notifications')
driver = webdriver.Chrome(options=options)

url_dict = {"graphics_cards_amd": "https://www.ebuyer.com/store/Components/cat/Graphics-Cards-AMD",
            "graphics_cards_nvidia": "https://www.ebuyer.com/store/Components/cat/Graphics-Cards-Nvidia"}

data_set = {"computer_parts": {}}
for information, url in url_dict.items():
    time.sleep(1)
    # Open the Currys laptop page
    driver.get(url)
    time.sleep(2)

    # Wait for cookies button to appear
    accept_cookies_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'onetrust-accept-btn-handler'))
    )
    print("--SUCCESS-- Cookies button located.")
    time.sleep(1)

    # Accept cookies
    accept_cookies_button.click()
    print("--SUCCESS-- Cookies button clicked.")

    time.sleep(5)

    # # Find elements to iterate over
    items_listed = driver.find_elements(By.CLASS_NAME, "listing-product")
    print(f"Number of items listed: {len(items_listed)}")
    time.sleep(1)

    # Set up dictionary to store data
    product_data = []

    # Iterate through listed elements to scrape data
    for item in items_listed:
        title = item.find_element(By.CLASS_NAME, "listing-product-title").text
        price = item.find_element(By.CLASS_NAME, "price").text
        try:
            memory_size = driver.find_element(By.XPATH, "//span[contains(text(), 'Memory Size / Type')]/following-sibling::span").text
        except:
            memory_size = "N/A"
        
        try:
            clock_speed = driver.find_element(By.XPATH, "//span[contains(text(), 'Clock Speed')]/following-sibling::span").text
        except:
            clock_speed = "N/A"
        
        try:
            interface = driver.find_element(By.XPATH, "//span[contains(text(), 'Interface')]/following-sibling::span").text
        except:
            interface = "N/A"
        
        try:
            stream_processors = driver.find_element(By.XPATH, "//span[contains(text(), 'Stream Processors')]/following-sibling::span").text
        except:
            stream_processors = "N/A"
        
        try:
            bandwidth = driver.find_element(By.XPATH, "//span[contains(text(), 'Bandwidth')]/following-sibling::span").text
        except:
            bandwidth = "N/A"
        product_data.append({
        "title": title,
        "price": price,
        "memory_size": memory_size,
        "clock_speed": clock_speed,
        "interface": interface,
        "stream_processors": stream_processors,
        "bandwidth": bandwidth
        })
        
    data_set["computer_parts"][information] = product_data
    # Exit
    driver.quit()
    time.sleep(3)

print(data_set)

# #<--------------------------------------------------------------------------------------------------------------------------------------->

# # #Click through to laptop endpoint
# link = driver.find_element(By.LINK_TEXT, ("Laptops"))

# link.click()

# #<--------------------------------------------------------------------------------------------------------------------------------------->



# try:
#     #Wait until elements have loaded for 10 seconds.
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".thumbnail"))
#     )
# except:
#     driver.quit()

# #Find elements to inspect for data by thumbnail.
# laptop_list = driver.find_elements(By.CSS_SELECTOR, ".thumbnail")

# #Set up Dictionary to store data.
# laptop_info = {"Laptops_Listed": {}}

# #Iterate through elements in list to scrape information.
# for laptop in laptop_list:
    
#     # Test use class to find element
#     title = laptop.find_element(By.CLASS_NAME, "title").text

#     description = laptop.find_element(By.CSS_SELECTOR, ".description").text

#     #Test use CSS Selector to find element
#     price = laptop.find_element(By.CSS_SELECTOR, ".price").text
    
#     #Store data in dictionary
#     laptop_info["Laptops_Listed"][title] = {"Price": price,
#                                             "Description": description}

#<--------------------------------------------------------------------------------------------------------------------------------------->



# # Time Program End.
# end_time = datetime.now()

# # Format Time.
# time = (end_time - start_time)
# total_seconds = time.total_seconds()
# milliseconds = time.microseconds / 1000000
# formatted_duration = "{:.2f} seconds".format(total_seconds + milliseconds)

# #Write test time to file.
# with open("web-scraper/testing/testing_times/driver_test_time.txt", "a") as file:
#     file.write(formatted_duration + "\n")