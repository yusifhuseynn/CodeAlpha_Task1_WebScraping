import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import matplotlib.pyplot as plt

# Başlanğıc URL (ilk səhifə)
url = "http://books.toscrape.com/"

# CSV faylına məlumat yazmaq üçün açırıq
with open('books_extended.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # CSV faylında başlıqları yazırıq
    writer.writerow(['Kitab adı', 'Qiymət', 'İcmal', 'Yazar', 'Təsvir', 'Kateqoriya'])

    # İlk səhifəni sorğulamaq
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    # Kitabların olduğu bölməni tapırıq
    books = soup.find_all('article', class_='product_pod')

    # Hər bir kitabı dövr edirik
    for book in books:
        title = book.find('h3').find('a')['title']  # Kitab adı
        price = book.find('p', class_='price_color').get_text()  # Qiymət
        rating = book.find('p', class_='star-rating')['class'][1]  # İcmal (rating)
        
        # Kitaba klikləyərək səhifəyə daxil olmaq üçün linki alırıq
        book_link = book.find('h3').find('a')['href']
        book_url = f"http://books.toscrape.com/{book_link}"
        
        # Kitabın səhifəsindən daha ətraflı məlumatı çəkirik
        book_response = requests.get(book_url)
        book_response.encoding = 'utf-8'
        book_soup = BeautifulSoup(book_response.text, 'html.parser')
        
        # Kitabın müəllifi (yazarı) və təsviri
        author = book_soup.find('span', class_='author').get_text() if book_soup.find('span', class_='author') else 'N/A'
        description = book_soup.find('meta', {'name': 'description'})['content'] if book_soup.find('meta', {'name': 'description'}) else 'N/A'
        
        # Kitabın kateqoriyası
        category = book_soup.find('ul', class_='breadcrumb').find_all('li')[2].get_text().strip() if book_soup.find('ul', class_='breadcrumb') else 'N/A'
        
        # Verilənləri CSV faylına yazırıq
        writer.writerow([title, price, rating, author, description, category])

print("Məlumatlar 'books_extended.csv' faylına yazıldı.")

# CSV faylını oxuyuruq
data = pd.read_csv('books_extended.csv')

# Qiymətlərə görə kitab sayısını vizuallaşdırmaq
data['Qiymət'] = data['Qiymət'].replace({'£': ''}, regex=True).astype(float)

# Qiymətlərin paylanmasını göstəririk
plt.hist(data['Qiymət'], bins=10, edgecolor='black')
plt.title('Kitab Qiymətlərinin Paylanması')
plt.xlabel('Qiymət (£)')
plt.ylabel('Kitab Sayı')
plt.show()
