from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from datetime import datetime

# Time Program Start
start_time = datetime.now()

# Use Headless Mode for optimised performance.
options = Options()
options.headless = True  
options.add_argument("--window-size=1920,1200")

# Set Webdriver (Chrome in this case), include options kwarg to enable headless mode.
driver = webdriver.Chrome(options=options)

#Scrape entire page for text
# print(driver.page_source)



#<--------------------------------------------------------------------------------------------------------------------------------------->

#Choose website url to scrape.
driver.get("https://webscraper.io/test-sites/e-commerce/static/computers/tablets")

try:
    #Wait until elements have loaded for 10 seconds.
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-wrapper"))
    )
except:
    driver.quit()

#Find elements to inspect for data by thumbnail.
tablet_list = driver.find_elements(By.CSS_SELECTOR, ".product-wrapper")

#<--------------------------------------------------------------------------------------------------------------------------------------->



#Set up Dictionary to store data.
tablet_info = {"Tablets_Listed": {}}

#Iterate through elements in list to scrape information.
for tablet in tablet_list:
    
    # Test use class to find element
    title = tablet.find_element(By.CLASS_NAME, "title").text

    description = tablet.find_element(By.CSS_SELECTOR, ".description").text

    #Test use CSS Selector to find element
    price = tablet.find_element(By.CSS_SELECTOR, ".price").text
    
    #Store data in dictionary
    tablet_info["Tablets_Listed"][title] = {"Price": price,
                                            "Description": description}



#<--------------------------------------------------------------------------------------------------------------------------------------->

# #Click through to laptop endpoint
link = driver.find_element(By.LINK_TEXT, ("Laptops"))

link.click()

#<--------------------------------------------------------------------------------------------------------------------------------------->



try:
    #Wait until elements have loaded for 10 seconds.
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".thumbnail"))
    )
except:
    driver.quit()

#Find elements to inspect for data by thumbnail.
laptop_list = driver.find_elements(By.CSS_SELECTOR, ".thumbnail")

#Set up Dictionary to store data.
laptop_info = {"Laptops_Listed": {}}

#Iterate through elements in list to scrape information.
for laptop in laptop_list:
    
    # Test use class to find element
    title = laptop.find_element(By.CLASS_NAME, "title").text

    description = laptop.find_element(By.CSS_SELECTOR, ".description").text

    #Test use CSS Selector to find element
    price = laptop.find_element(By.CSS_SELECTOR, ".price").text
    
    #Store data in dictionary
    laptop_info["Laptops_Listed"][title] = {"Price": price,
                                            "Description": description}

#<--------------------------------------------------------------------------------------------------------------------------------------->



# Time Program End.
end_time = datetime.now()

# Format Time.
time = (end_time - start_time)
total_seconds = time.total_seconds()
milliseconds = time.microseconds / 1000000
formatted_duration = "{:.2f} seconds".format(total_seconds + milliseconds)

#Write test time to file.
with open("web-scraper/testing/testing_times/driver_test_time.txt", "a") as file:
    file.write(formatted_duration + "\n")