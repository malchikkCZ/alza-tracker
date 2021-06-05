import requests
import time
from bs4 import BeautifulSoup
from manager import FileManager
from selenium import webdriver


class UrlScraper:
    
    def __init__(self, url, driver):
        self.url = url
        self.driver = webdriver.Chrome(driver)

    def get_urls(self):
        print("Fetching list of all items.")
        t = time.time()
        urls = []
        self.driver.get(self.url)
        time.sleep(5)
        while True:
            try:
                self.driver.find_element_by_css_selector(".moreblock a").click()
                time.sleep(5)
            except Exception as e:
                print(e)
                break
        time.sleep(5)
        links = self.driver.find_elements_by_css_selector(".fb a")
        for link in links:
            try:
                url = link.get_attribute("href")
                if url not in urls:
                    urls.append(url)
            except AttributeError:
                continue
        self.driver.quit()
        t = time.time() - t
        print(f"Done in {t:.2f} seconds.")
        return urls


class PriceTracker:

    def __init__(self):
        self.database = FileManager()

    def get_details(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        try:
            price_as_list = soup.find(name="span", class_="price_withVat").getText()[:-2].split()
            item_name = soup.find(name="h1", itemprop="name").getText().strip()
        except AttributeError:
            return None
        item_price = 0
        multiplyer = 1
        for part in price_as_list[::-1]:
            item_price += int(part) * multiplyer
            multiplyer *= 1000
        item = {
            "name": item_name,
            "url": url,
            "price": item_price,
        }
        return item
    
    def get_updates(self, urls):
        print("Diving deep to get details of all items.")
        t = time.time()
        items = []
        for url in urls:
            item = self.get_details(url)
            if item is not None:
                items.append(item)
        t = time.time() - t
        print(f"Done in {t:.2f} seconds")
        print("Comparing prices with saved data.")
        t = time.time()
        data = self.database.load()
        new_items = []
        pricedrops = []
        for item in items:
            for entry in data:
                if item["url"] == entry["url"]:
                    if item["price"] < entry["price"]:
                        pricedrops.append(item)
                    entry["price"] = item["price"]
                    break
            if item not in data:
                data.append(item)
                new_items.append(item)
        self.database.save(data)
        t = time.time() - t
        print(f"Done in {t:.2f} seconds.")
        return {"new": new_items, "sale": pricedrops}
