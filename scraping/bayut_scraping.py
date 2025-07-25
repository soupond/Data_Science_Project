import requests
from bs4 import BeautifulSoup
import pandas as pd
import re 
import time

# 1. Define the base URL of the website
base_url = "https://www.bayut.om/en/oman/properties-for-rent/"

# List to store all scraped property data
all_properties_data = []

print(f"Starting to scrape from: {base_url}")

# Set up headers to look like a real browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}  # try adding whatsapp user agent to bypass certain firewalls!! 

# Try pages automatically until no more properties found
page_num = 1
while True:
    if page_num == 1:
        page_url = "https://www.bayut.om/en/oman/properties-for-rent/"
    else:
        page_url = f"https://www.bayut.om/en/oman/properties-for-rent/?page={page_num}"
    
    print(f"\nScraping page {page_num}: {page_url}")
    
    try:
        # Add delays between pages to avoid being blocked
        if page_num > 1:
            print("Waiting 5 seconds before next page...")
            time.sleep(5)
            
        response = requests.get(page_url, headers=headers, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page {page_url}: {e}")
        break  # Stop if we can't access the page

    soup = BeautifulSoup(response.text, 'html.parser')
    
    property_articles = soup.select('article')
    
    if not property_articles:
        print(f"No property articles found on page {page_num}. End of scraping.")
        break  # No more properties, we've reached the end

    print(f"Found {len(property_articles)} properties on page {page_num}")

    # Extract data from each individual property page
    for property_item in property_articles:
        try:
            # Get the link to individual property page
            title_link = property_item.find('a')
            if not title_link or not title_link.get('href'):
                continue
                
            property_url = requests.compat.urljoin(base_url, title_link.get('href'))
            
            print(f"  Visiting property: {property_url}")
            
            # Visit individual property page
            try:
                property_response = requests.get(property_url, headers=headers, timeout=15)
                property_response.raise_for_status()
                property_soup = BeautifulSoup(property_response.text, 'html.parser')
                
                # Add small delay between property visits
                time.sleep(1)
                
            except requests.exceptions.RequestException as e:
                print(f"    Error fetching property {property_url}: {e}")
                continue
            
            # Extract title from property page
            title_elem = property_soup.find('h1')
            title = title_elem.text.strip() if title_elem else 'N/A'
            
            # Extract price from property page
            price = 'N/A'
            price_text = property_soup.get_text()
            price_match = re.search(r'OMR\s*[\d,]+', price_text)
            if price_match:
                price = price_match.group(0)
            
            # Extract bedrooms from property page text
            bedroom_match = re.search(r'(\d+)\s*Bed', price_text, re.I)
            bedrooms = bedroom_match.group(1) if bedroom_match else 'N/A'
            
            # Extract bathrooms from property page text
            bathroom_match = re.search(r'(\d+)\s*Bath', price_text, re.I)
            bathrooms = bathroom_match.group(1) if bathroom_match else 'N/A'
            
            # Extract area from property page text
            area_match = re.search(r'(\d+(?:,\d+)?)\s*Sq\.\s*M\.', price_text, re.I)
            area = area_match.group(1) + ' Sq. M.' if area_match else 'N/A'
            
            # Extract location from property page (targeting the exact highlighted location)
            location = 'N/A'
            
            # Method 1: Look for the location that appears right under the price
            # From your screenshots, this appears as a standalone text element
            h2_elements = property_soup.find_all('h2')
            for h2 in h2_elements:
                h2_text = h2.get_text(strip=True)
                # Check if it looks like a location (has comma, reasonable length)
                if ',' in h2_text and len(h2_text) < 30 and len(h2_text) > 8:
                    if 'Property' not in h2_text and 'Information' not in h2_text:
                        location = h2_text
                        break
            
            # Method 2: Look for specific location patterns in divs near price
            if location == 'N/A':
                # Look for divs that might contain the highlighted location
                all_divs = property_soup.find_all('div')
                for div in all_divs:
                    div_text = div.get_text(strip=True)
                    # Look for "City, Region" pattern that matches Oman locations
                    if (',' in div_text and len(div_text) < 25 and 
                        ('Muscat' in div_text or 'Al ' in div_text or 'Qantab' in div_text or 
                         'Salalah' in div_text or 'Dhofar' in div_text)):
                        if ('Property' not in div_text and 'Features' not in div_text and 
                            'Information' not in div_text):
                            location = div_text
                            break
            
            # Method 3: Extract from title as last resort
            if location == 'N/A' and title != 'N/A' and 'in ' in title:
                parts = title.split('in ', 1)
                if len(parts) > 1:
                    location = parts[1].strip()
                    
            print(f"    → Location found: {location}")  # Debug print
            
            # Determine property type from title
            property_type = 'Other'
            if title != 'N/A':
                if 'Villa' in title:
                    property_type = 'Villa'
                elif 'Apartment' in title:
                    property_type = 'Apartment'
                elif 'Townhouse' in title:
                    property_type = 'Townhouse'
            
            property_data = {
                'Title': title,
                'Price': price,
                'Bedrooms': bedrooms,
                'Bathrooms': bathrooms,
                'Area': area,
                'Location': location,
                'Property_Type': property_type,
                'URL': property_url,
                'Page': page_num
            }
            
            all_properties_data.append(property_data)
            
        except Exception as e:
            print(f"Error extracting property data: {e}")
            continue

    print(f"Extracted {len([p for p in all_properties_data if p['Page'] == page_num])} properties from page {page_num}")
    

    if page_num >= 100:  # Max 100 pages
        print("Reached maximum page limit (100). Stopping.")
        break
    
    page_num += 1

print(f"\nScraping completed! Total properties: {len(all_properties_data)}")

# Create DataFrame exactly like tutor
df = pd.DataFrame(all_properties_data)

# Save the data
df.to_csv('clean_data/cleanedDB.csv', index=False)
print("Data saved to 'Clean_data' folder ")

