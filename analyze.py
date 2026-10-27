"""Scraped dataset par basic analysis. Pehle scraper.py chalao."""
import pandas as pd

df = pd.read_csv("data/books.csv")
print("Total books      :", len(df))
print("Average price    : £%.2f" % df.price_gbp.mean())
print("Cheapest book    :", df.loc[df.price_gbp.idxmin(), "title"])
print("Costliest book   :", df.loc[df.price_gbp.idxmax(), "title"])
print("In stock         :", int(df.in_stock.sum()))
print("\nRating distribution:")
print(df.rating.value_counts().sort_index())
print("\nAverage price by rating:")
print(df.groupby("rating").price_gbp.mean().round(2))

# Custom dataset: sirf 4-5 star aur £30 se sasti books
custom = df[(df.rating >= 4) & (df.price_gbp < 30)]
custom.to_csv("data/top_rated_cheap_books.csv", index=False)
print(f"\nCustom dataset: {len(custom)} books -> data/top_rated_cheap_books.csv")
