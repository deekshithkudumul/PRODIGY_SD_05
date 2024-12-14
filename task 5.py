import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the eBay website's product listings page
url = 'https://www.ebay.com/sch/i.html?_nkw=laptop'

# Send a request to fetch the HTML content
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extract product details
products = []
for product in soup.find_all('div', class_='s-item__info'):
    try:
        name = product.find('h3', class_='s-item__title').text.strip()
    except AttributeError:
        name = 'No name'
    
    try:
        price = product.find('span', class_='s-item__price').text.strip()
    except AttributeError:
        price = 'No price'
    
    rating = product.find('div', class_='x-star-rating')
    if rating:
        rating = rating.find('span', class_='clipped').text.strip()
    else:
        rating = 'No rating'
    
    products.append([name, price, rating])

# Create a DataFrame and save to CSV
df = pd.DataFrame(products, columns=['Name', 'Price', 'Rating'])
df.to_csv('ebay_products.csv', index=False)

print("Product information has been saved to ebay_products.csv")
