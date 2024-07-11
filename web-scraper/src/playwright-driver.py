from playwright.sync_api import sync_playwright
from datetime import datetime
import json

# Time Program Start
start_time = datetime.now()

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

# Function to iterate and store items.
def iterate_and_store_items(page, data_set, information, page_count):
    # Find elements to iterate over.
    items_listed = page.query_selector_all(".listing-product")
    print(f"Number of items listed on page {page_count}: {len(items_listed)}")

    # Set up dictionary to store data.
    product_data = []

    for item in items_listed:
        name = item.query_selector(".listing-product-title").inner_text()
        price_element = item.query_selector(".price")
        price = price_element.inner_text() if price_element else "Price not available"
        details_element = item.query_selector(".listing-key-selling-points")
        details = details_element.inner_text() if details_element else "Details not available"


        product_data.append({
            "product_name": name,
            "product_price": price,
            "product_details": details
        })

    if page_count == 1:
        data_set["computer_parts"][information] = product_data
    else:
        data_set["computer_parts"][information].extend(product_data)

# Iterate through each category in url_dict.
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    for information, url in url_dict.items():
        page_count = 1

        while True:
            page = browser.new_page()
            # Open the web page and check page count, append page count to url if > 1.
            if page_count == 1:
                page.goto(url)
            else:
                page.goto(f"{url}?page={page_count}")

            page.wait_for_timeout(1000)

            # Wait for cookies button to appear and click it.
            accept_cookies_button = page.wait_for_selector('#onetrust-accept-btn-handler', timeout=7000)
            print("--SUCCESS-- Cookies button located.")
            accept_cookies_button.click()
            print("--SUCCESS-- Cookies button clicked.")

            # Call function to iterate over and store items
            iterate_and_store_items(page, data_set, information, page_count)

            # Locate the next page button and pass through, add to page count.
            try:
                next_page_button = page.query_selector(".glyphicon-chevron-right")
                if next_page_button:
                    print(f"--SUCCESS-- Proceeding to page {page_count + 1}")
                    page_count += 1
                    page.close()
                else:
                    raise Exception("Next page button not found")
            except Exception as error:
                print(f"--ERROR-- No more pages found: Error: {error}")
                page.close()
                break

    browser.close()

# Write to json format for storage.
json_data = json.dumps(data_set, indent=4)
path = "./data/playwright_product_details.json"
with open(path, "w") as f:
    f.write(json_data)

# Time Program End.
end_time = datetime.now()

# Format Time.
time = (end_time - start_time)
total_seconds = time.total_seconds()
milliseconds = time.microseconds / 1000000
formatted_duration = "{:.2f} seconds".format(total_seconds + milliseconds)

# # Write test time to file.
# with open("web-scraper/testing/testing_times/driver_time.txt", "a") as file:
#     file.write(formatted_duration + "\n")
