# Task 1: Web Scraping (BeautifulSoup)

Target site: https://books.toscrape.com (scraping practice ke liye bana public site)

## Phase 1: Setup
```bash
python -m venv venv
venv\Scripts\activate        # Windows  (Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt
```

## Phase 2: Parser test (internet ke bina)
```bash
python tests/test_parser.py
```

## Phase 3: Scrape karo
```bash
python scraper.py --pages 3     # pehle chhota test
python scraper.py               # poora (50 pages, ~1000 books)
```
Output: `data/books.csv`, `data/books.json`

## Phase 4: Analysis + custom dataset
```bash
python analyze.py
```
Output: `data/top_rated_cheap_books.csv` (4-5 star aur £30 se kam)

## Task points kaise cover hue
| Requirement | Kahan |
|---|---|
| BeautifulSoup use | `parse_page()` in scraper.py |
| Public web pages se dataset | books.toscrape.com, ~1000 books |
| HTML structure + navigation | CSS selectors + 50-page pagination loop |
| Accurate data | price float, rating number, duplicates remove, retry/404 handling |
| Custom dataset | analyze.py ka filtered CSV |
# CodeAlpha_Web_Scraper
