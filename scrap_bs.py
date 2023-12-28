import csv
import requests
from bs4 import BeautifulSoup as BS
import logging

def scrape_website(url):
    url = 'https://www.metro.ca/en/online-grocery/aisles/fruits-vegetables'
    response = requests.get(url)
    soup = BS(response.content, 'html.parser')

    # Get total page count
    page_count = soup.select_one('div.ppn--pagination').find_all('a')[-1].text
    next_button = soup.select_one('a.ppn--element.corner')
    print(f"total page count: {page_count}")

    # Get products info
    products = []

    for i in range(int(page_count)):
        print(f"Page number: {i+1}")
        try:
            product_brands = soup.select('span.head__brand')
            product_names = soup.select('div.head__title')
            product_units = soup.select('span.head__unit-details')
            product_prices = soup.select('div.pricing__sale-price')
            pricing_units = soup.select('div.pricing__unit-value')
            product_secondary_prices = soup.select('div.pricing__secondary-price')
            product_before_prices = soup.select('div.pricing__before-price')
            product_valid_dates = soup.select('div.pricing__until-date')

            for brand, name, product_unit, price, pricing_unit, secondary_price, before_price, date in zip(product_brands, product_names, product_units, product_prices,\
                    pricing_units, product_secondary_prices, product_before_prices, product_valid_dates):
                product_info = [brand.text, name.text, product_unit.text, price.text, pricing_unit.text, secondary_price.text, before_price.text, date.text]
                products.append(product_info)

        except Exception as e:
            logging.error(f"Error scraping page {i+1}: {e}")

        # Click the "Next" button.
        next_button_url = next_button['href']
        response = requests.get(next_button_url)
        soup = BS(response.content, 'html.parser')
        next_button = soup.select_one('a.ppn--element.corner')
        print("Next button clicked!")

    return products

def save_to_csv(self, products):
    with open('metro_products.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Brand', 'Product Name', 'Product Unit', 'Product Price', 'Pricing Unit', 'Secondary Price', 'Before Price', 'Valid Date'])
        writer.writerows(products)
