import csv
import time
import logging
import undetected_chromedriver as webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(
    level=logging.DEBUG,
    filename='Metro.log',
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

class Metro_Scraper:
    
    def run_browser(self, url):
        service = Service(executable_path=r'/Users/gibbo/.wdm/drivers/chromedriver/mac64/120.0.6099.109/chromedriver-mac-x64/chromedriver.exec')
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--use_subprocess")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.maximize_window()
        self.driver.get(url)

    def scrape_website(self):
        url = 'https://www.metro.ca/en/online-grocery/aisles/fruits-vegetables'
        self.run_browser(url)
        time.sleep(1)

        # Get total page count
        WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, "//div[@class='ppn--pagination']")))
        page_count = self.driver.find_elements(By.XPATH, "//a[@class='ppn--element']")[-1].text
        print(f"total page count: {page_count}")

        # Get products info
        products = []

        for i in range(int(page_count)):
            WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//div[@class="pt__content--wrap"]')))
            print(f"Page number: {i+1}")

            try:
                product_brands = self.driver.find_elements_by_xpath('//span[@class="head__brand"]')
                product_names = self.driver.find_elements_by_xpath('//div[@class="head__title"]')
                product_units = self.driver.find_elements_by_xpath('//span[@class="head__unit-details"]')
                product_prices = self.driver.find_elements_by_xpath('//div[@class="pricing__sale-price"]')
                pricing_units = self.driver.find_elements_by_xpath('//div[@class="pricing__unit-value"]')
                product_secondary_prices = self.driver.find_elements_by_xpath('//div[@class="pricing__secondary-price"]')
                product_before_prices = self.driver.find_elements_by_xpath('//div[@class="pricing__before-price"]')
                product_valid_dates = self.driver.find_elements_by_xpath('//div[@class="pricing__until-date"]')

                for brand, name, product_unit, price, pricing_unit, secondary_price, before_price, date in zip(
                    product_brands,
                    product_names,
                    product_units,
                    product_prices,
                    pricing_units,
                    product_secondary_prices,
                    product_before_prices,
                    product_valid_dates
                ):
                    print(f"product name: {name.text}")
                    product_info = [brand.text, name.text, product_unit.text, price.text, pricing_unit.text, secondary_price.text, before_price.text, date.text]
                    products.append(product_info)

            except:
                pass

            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//a[@class="ppn--element corner"]')))
            next_button = self.driver.find_element(By.XPATH, '//a[@class="ppn--element corner"]')
            self.driver.execute_script("arguments[0].click();", next_button)
            print("Next button clicked!")

            # Wait for the next page to be loaded.
            time.sleep(1)
            
            # Update the page count to get correct value for subsequent iterations
            page_count = self.driver.find_elements(By.XPATH, "//a[@class='ppn--element']")[-1].text

        return products
    
    def save_to_csv(self, products):
        with open('metro_products.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Brand', 'Product Name', 'Product Unit', 'Product Price', 'Pricing Unit', 'Secondary Price', 'Before Price', 'Valid Date'])
            writer.writerows(products)

if __name__ == "__main__":
    metro_scraper = Metro_Scraper()
    products = metro_scraper.scrape_website()
    metro_scraper.save_to_csv(products)