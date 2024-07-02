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


# Open the Currys laptop page
driver.get("https://www.argos.co.uk/")
time.sleep(2)

# Wait for cookies button to appear
accept_cookies_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'explicit-consent-prompt-accept'))
)
print("--SUCCESS-- Cookies button located.")
time.sleep(1)

# Accept cookies
accept_cookies_button.click()
print("--SUCCESS-- Cookies button clicked.")

#Search for laptops (Expand this into a for loop for items)
search = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CLASS_NAME, "_1Rz0y"))
)
print("--SUCCESS-- Search bar found.")

search.send_keys("laptops")
search.send_keys(Keys.RETURN)
print("--SUCCESS-- Search returned.")


#<--------------------------------------------------------------------------------------------------------------------------------------->
#Let search load (IMPORTANT)
time.sleep(5)

# Find elements to iterate over
items_listed = driver.find_elements(By.CLASS_NAME, "ProductCardstyles__Wrapper-h52kot-1")
print(f"Number of items listed: {len(items_listed)}")
time.sleep(1)

# Set up dictionary to store data
laptop_data = {"laptop_list": {}}

# Iterate through listed elements to scrape data
for laptop in items_listed:
    title = laptop.find_element(By.CLASS_NAME, "ProductCardstyles__Title-h52kot-12").text
    print(title)
        

# Exit
driver.quit()


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