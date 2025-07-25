#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def main():
    # 1. Launch Chrome with the matching driver
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install())
    )

    all_properties = []
    page = 1

    try:
        # 2. Keep going until there are no listings on the next page
        while True:
            print(f"Scraping page {page}...")
            driver.get(f"https://www.dubizzle.com.om/en/properties/?page={page}")
            time.sleep(3)  # wait for listings to load

            listings = driver.find_elements(By.XPATH, '//li[@aria-label="Listing"]')
            count = len(listings)
            print(f"  Found {count} listings")

            # 3. If no listings, we're done
            if count == 0:
                print("No more listings; stopping.")
                break

            # 4. Otherwise, extract each listing
            for listing in listings:
                prop = {}

                # title
                try:
                    prop['title'] = listing.find_element(By.TAG_NAME, 'h2').text
                except:
                    prop['title'] = ''

                # url
                try:
                    prop['url'] = listing.find_element(By.TAG_NAME, 'a').get_attribute('href')
                except:
                    prop['url'] = ''

                # price in OMR
                try:
                    price_txt = listing.find_element(
                        By.XPATH,
                        './/span[contains(@class,"ddc1b288")]'
                    ).text
                    prop['price_omr'] = float(
                        price_txt.replace('OMR', '').replace(',', '').strip()
                    )
                except:
                    prop['price_omr'] = None

                # bedrooms
                try:
                    beds = listing.find_element(
                        By.XPATH,
                        './/span[@aria-label="Beds"]/span'
                    ).text
                    prop['bedrooms'] = int(beds)
                except:
                    prop['bedrooms'] = None

                # bathrooms
                try:
                    baths = listing.find_element(
                        By.XPATH,
                        './/span[@aria-label="Bathrooms"]/span'
                    ).text
                    prop['bathrooms'] = int(baths)
                except:
                    prop['bathrooms'] = None

                # area (sqm)
                try:
                    area_txt = listing.find_element(
                        By.XPATH,
                        './/span[@aria-label="Area"]/span'
                    ).text
                    prop['size_sqm'] = float(area_txt.replace('sqm', '').strip())
                except:
                    prop['size_sqm'] = None

                # location/locality
                try:
                    loc = listing.find_element(
                        By.XPATH,
                        './/span[@aria-label="Location"]'
                    ).text
                    prop['locality'] = loc.split('•')[0].strip()
                except:
                    prop['locality'] = ''

                # listing date
                try:
                    prop['listing_date'] = listing.find_element(
                        By.XPATH,
                        './/span[@aria-label="Creation date"]'
                    ).text
                except:
                    prop['listing_date'] = ''

                # agency
                try:
                    prop['agency'] = listing.find_element(
                        By.CLASS_NAME,
                        '_8206696c'
                    ).text
                except:
                    prop['agency'] = ''

                all_properties.append(prop)

            # 5. Go to the next page
            page += 1

    finally:
        # 6. Save to CSV and quit browser
        df = pd.DataFrame(all_properties)
        df.to_csv('cleaned_data/dubclean.csv', index=False)
        print(f"\nSaved {len(df)} listings to clean_data folder")
        driver.quit()

if __name__ == "__main__":
    main()
