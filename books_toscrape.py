import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import matplotlib.pyplot as plt

# Initial URL (first page)
url = "http://books.toscrape.com/"

# Open the CSV file to write data
with open('books_extended.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # Write the headers to the CSV file
    writer.writerow(['Book Title', 'Price', 'Rating', 'Author', 'Description', 'Category'])

    # Send a GET request to the first page
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all the books on the page
    books = soup.find_all('article', class_='product_pod')

    # Loop through each book
    for book in books:
        title = book.find('h3').find('a')['title']  # Book title
        price = book.find('p', class_='price_color').get_text()  # Price
        rating = book.find('p', class_='star-rating')['class'][1]  # Rating
        
        # Get the link to the book's detailed page
        book_link = book.find('h3').find('a')['href']
        book_url = f"http://books.toscrape.com/{book_link}"
        
        # Fetch more detailed data from the book's page
        book_response = requests.get(book_url)
        book_response.encoding = 'utf-8'
        book_soup = BeautifulSoup(book_response.text, 'html.parser')
        
        # Author and description of the book
        author = book_soup.find('span', class_='author').get_text() if book_soup.find('span', class_='author') else 'N/A'
        description = book_soup.find('meta', {'name': 'description'})['content'] if book_soup.find('meta', {'name': 'description'}) else 'N/A'
        
        # Category of the book
        category = book_soup.find('ul', class_='breadcrumb').find_all('li')[2].get_text().strip() if book_soup.find('ul', class_='breadcrumb') else 'N/A'
        
        # Write the extracted data to the CSV file
        writer.writerow([title, price, rating, author, description, category])

print("Data has been written to 'books_extended.csv'.")

# Read the CSV file
data = pd.read_csv('books_extended.csv')

# Remove the '£' symbol and convert price to float
data['Price'] = data['Price'].replace({'£': ''}, regex=True).astype(float)

# Visualize the distribution of book prices
plt.hist(data['Price'], bins=10, edgecolor='black')
plt.title('Distribution of Book Prices')
plt.xlabel('Price (£)')
plt.ylabel('Number of Books')
plt.show()
