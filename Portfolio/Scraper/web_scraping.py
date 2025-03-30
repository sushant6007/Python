import requests
from bs4 import BeautifulSoup
import csv

url = "https://books.toscrape.com/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

books = []
for book in soup.select('article.product_pod')[:5]:
    title = book.select_one('h3 a').text.strip()
    price = book.select_one('.price_color').text.strip()
    books.append([title,price])

with open("books.csv", 'w', newline="", encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['title', 'price'])
    writer.writerows(books)

print ("Scrapping Complete Please Check books.csv")

