"""
Task 1: Web Scraping
Target  : https://books.toscrape.com  (public sandbox site, scraping ke liye legal/allowed)
Output  : data/books.csv  and  data/books.json
Run     : python scraper.py            (saare 50 pages)
          python scraper.py --pages 3  (sirf pehle 3 pages, testing ke liye)
"""
import argparse
import json
import time
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
HEADERS = {"User-Agent": "Mozilla/5.0 (educational scraper - Himanshu SVSU task)"}
RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def fetch(url, retries=3):
    """Page download karo, fail ho toh retry karo."""
    for attempt in range(1, retries + 1):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            if resp.status_code == 404:
                return None  # pages khatam
            resp.raise_for_status()
            resp.encoding = "utf-8"
            return resp.text
        except requests.RequestException as err:
            print(f"  [retry {attempt}/{retries}] {err}")
            time.sleep(2 * attempt)
    return None


def parse_page(html, page_url):
    """Ek listing page se saari books ka data nikalo (HTML structure handle karna)."""
    soup = BeautifulSoup(html, "html.parser")
    books = []
    for card in soup.select("article.product_pod"):
        link = card.h3.a
        rating_word = card.select_one("p.star-rating")["class"][1]
        price_text = card.select_one("p.price_color").get_text(strip=True)
        books.append({
            "title": link["title"],
            "price_gbp": float(price_text.replace("£", "").replace("Â", "")),
            "rating": RATING_MAP.get(rating_word, 0),
            "in_stock": "In stock" in card.select_one("p.availability").get_text(),
            "url": urljoin(page_url, link["href"]),
        })
    return books


def scrape(max_pages):
    all_books = []
    for page in range(1, max_pages + 1):
        url = BASE_URL.format(page)
        print(f"Scraping page {page}: {url}")
        html = fetch(url)
        if html is None:
            print("Aur pages nahi mile, stop.")
            break
        all_books.extend(parse_page(html, url))
        time.sleep(1)  # server par load na pade (polite scraping)
    return all_books


def clean_and_save(books):
    df = pd.DataFrame(books).drop_duplicates(subset="url").reset_index(drop=True)
    df.to_csv("data/books.csv", index=False, encoding="utf-8")
    with open("data/books.json", "w", encoding="utf-8") as f:
        json.dump(df.to_dict(orient="records"), f, indent=2, ensure_ascii=False)
    print(f"\nDone! {len(df)} books saved -> data/books.csv, data/books.json")
    return df


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", type=int, default=50)
    args = ap.parse_args()
    clean_and_save(scrape(args.pages))
