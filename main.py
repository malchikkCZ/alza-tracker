from engine import UrlScraper, PriceTracker


CHROMEDRIVER = "/snap/bin/chromium.chromedriver"
URL = "https://www.alza.cz/gaming/hry-pro-nintendo-switch/18860898.htm"


def main():
    scraper = UrlScraper(URL, CHROMEDRIVER)
    tracker = PriceTracker()

    urls = scraper.get_urls()
    updates = tracker.get_updates(urls)

    print("New items:")
    for item in updates["new"]:
        print(item["name"], "\t", item["price"])
    print("\nPricedrops:")
    for item in updates["sale"]:
        print(item["name"], "\t", item["price"])


if __name__ == "__main__":
    main()
