"""Offline test: sample HTML par parse_page() check karta hai (internet nahi chahiye)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scraper import parse_page

SAMPLE = """
<article class="product_pod">
  <p class="star-rating Three"></p>
  <h3><a href="a-light-in-the-attic_1000/index.html" title="A Light in the Attic">A Light in ...</a></h3>
  <div class="product_price"><p class="price_color">£51.77</p>
  <p class="instock availability"><i class="icon-ok"></i> In stock </p></div>
</article>
<article class="product_pod">
  <p class="star-rating Five"></p>
  <h3><a href="tipping-the-velvet_999/index.html" title="Tipping the Velvet">Tipping ...</a></h3>
  <div class="product_price"><p class="price_color">£53.74</p>
  <p class="instock availability">Out of stock</p></div>
</article>
"""

books = parse_page(SAMPLE, "https://books.toscrape.com/catalogue/page-1.html")
assert len(books) == 2
assert books[0] == {"title": "A Light in the Attic", "price_gbp": 51.77, "rating": 3,
                    "in_stock": True,
                    "url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"}
assert books[1]["rating"] == 5 and books[1]["in_stock"] is False
print("All parser tests passed")
