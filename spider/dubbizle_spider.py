# attempt at using scrapy, it worked but gets detetcted much quicker and blocked as a result. the empty csv is the output after being blocked. 
# however code is functional but incomplete


import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy import Request

class DubizzleSpider(scrapy.Spider):
    name = 'dubizzle'
    custom_settings = {
        'FEEDS': {'spider/dubizzle_properties.csv': {'format': 'csv', 'overwrite': True}},
        'DOWNLOAD_DELAY': 1.5,
        'RANDOMIZE_DOWNLOAD_DELAY': 1,
        'ROBOTSTXT_OBEY': False,
        'DUPEFILTER_DEBUG': True,
        'DEPTH_LIMIT': 100,
    }

    start_urls = ['https://www.dubizzle.com.om/en/properties/properties-for-rent/']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'
    }

    def parse(self, response):
        property_links = response.xpath('//a[contains(@href, "/ad/")]/@href').getall()
        self.logger.info(f"Found {len(property_links)} properties on page: {response.url}")

        for link in property_links:
            if link.startswith('/'):
                link = response.urljoin(link)

            yield Request(
                url=link,
                callback=self.parse_property,
                headers=self.headers,
                meta={'property_url': link}
            )

        # Pagination: go to next page until no more pages
        next_url = response.xpath('//a[div[@title="Next"]]/@href').get()
        if next_url:
            yield response.follow(next_url, callback=self.parse)

    def parse_property(self, response):
        title = response.xpath('//h1/text()').get()
        price = response.xpath('//span[@class="24469da7"]/text()').get()
        if not price:
            price = response.xpath('//span[contains(text(), "OMR")]/text()').get()


        location = response.xpath('//text()[not(ancestor::script) and not(ancestor::style)]').get()
        if not location:
            location = response.xpath('//span[contains(@class, "location")]/text()').get()


        bedrooms = response.xpath('//span[contains(text(), "Bedroom")]/following-sibling::span/text()').get()
        if not bedrooms:
            bedrooms = response.xpath('//span[@class="_82606f6c b7af14b4"]/text()').get()

        bathrooms = response.xpath('//span[contains(text(), "Bathroom")]/following-sibling::span/text()').get()
        area = response.xpath('//span[contains(text(), "Area")]/following-sibling::span/text()').get()
        if not area:
            area = response.xpath('//span[@class="a2b606bc b7af14b4"]/text()').get()

        property_type = response.xpath('//span[contains(text(), "Type")]/following-sibling::span/text()').get()
        furnished = response.xpath('//span[contains(text(), "Furnished")]/following-sibling::span/text()').get()

        description = response.xpath('//div[@aria-label="Description"]//p//text()').getall()
        if not description:
            description = response.css('p::text').getall()
        description = ' '.join([d.strip() for d in description if d.strip()]) if description else None

        amenities = response.xpath('//div[contains(@aria-label, "Amenities")]//text()').getall()
        if not amenities:
            amenities = response.xpath('//ul[contains(@class, "amenities")]//li//text()').getall()
        amenities = ', '.join([a.strip() for a in amenities if a.strip() and len(a.strip()) > 2]) if amenities else None

        agent_name = response.xpath('//div[contains(@class, "agent")]//text()').get()
        phone = response.xpath('//span[contains(@class, "phone") or contains(text(), "View phone")]//text()').get()

        parking = response.xpath('//span[contains(text(), "Parking")]/following-sibling::span/text()').get()
        floor = response.xpath('//span[contains(text(), "Floor")]/following-sibling::span/text()').get()
        building_age = response.xpath('//span[contains(text(), "Age")]/following-sibling::span/text()').get()
        property_id = response.url.split('/')[-1] if '/' in response.url else None

        yield {
            'property_id': property_id,
            'title': title.strip() if title else None,
            'price': price.strip() if price else None,
            'location': location.strip() if location else None,
            'bedrooms': bedrooms.strip() if bedrooms else None,
            'bathrooms': bathrooms.strip() if bathrooms else None,
            'area': area.strip() if area else None,
            'property_type': property_type.strip() if property_type else None,
            'furnished': furnished.strip() if furnished else None,
            'description': description,
            'amenities': amenities,
            'agent_name': agent_name.strip() if agent_name else None,
            'phone': phone.strip() if phone else None,
            'parking': parking.strip() if parking else None,
            'floor': floor.strip() if floor else None,
            'building_age': building_age.strip() if building_age else None,
            'url': response.meta['property_url']
        }

# Run the spider
if __name__ == "__main__":
    process = CrawlerProcess({
        'LOG_LEVEL': 'DEBUG',  # Use 'INFO' for less verbose output
    })
    process.crawl(DubizzleSpider)
    process.start()
