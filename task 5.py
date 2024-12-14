import requests
from bs4 import BeautifulSoup
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox

def scrape_data():
    url = url_entry.get()
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

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

    df = pd.DataFrame(products, columns=['Name', 'Price', 'Rating'])
    df.to_csv('products.csv', index=False)
    messagebox.showinfo("Success", "Product information has been saved to products.csv")
    
    # Clear previous data in the Treeview
    for row in tree.get_children():
        tree.delete(row)
    
    # Insert new data into the Treeview
    for product in products:
        tree.insert('', 'end', values=product)

# Create the main window
root = tk.Tk()
root.title("Web Scraper")

# Create and place the URL entry field
url_label = ttk.Label(root, text="Enter URL:")
url_label.grid(row=0, column=0, padx=10, pady=10)
url_entry = ttk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=10)

# Pre-fill the entry with the eBay URL
url_entry.insert(0, 'https://www.ebay.com/sch/i.html?_nkw=laptop')

# Create and place the scrape button
scrape_button = ttk.Button(root, text="Scrape", command=scrape_data)
scrape_button.grid(row=1, columnspan=2, padx=10, pady=10)

# Create and place the Treeview
columns = ('Name', 'Price', 'Rating')
tree = ttk.Treeview(root, columns=columns, show='headings')
tree.heading('Name', text='Name')
tree.heading('Price', text='Price')
tree.heading('Rating', text='Rating')
tree.grid(row=2, columnspan=2, padx=10, pady=10)

# Run the application
root.mainloop()
