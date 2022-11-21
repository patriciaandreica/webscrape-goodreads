import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
import datetime
import time

app = Flask(__name__)

#for db
app.secret_key = "secret key"

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Dictionary of Headers to send with the Request.
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

# Lists to pass to html
error = []
books_give = []
titles_give = []

# Defining at the module level
authors = ""
image = ""
ratings = ""
books = ""
giveaway_titles = ""
book_input = ""
genre = ""

def book_page(searchterms):
    """
    Load main page based on book title entered
    :param searchterms:
    :return: url of book page
    """
    searchterms = "+".join(searchterms.split())
    url =  f'https://www.goodreads.com/search?q={searchterms}'
    r = requests.get(url, headers={"Content-Type": "text"})
    soup = BeautifulSoup(r.content, 'html.parser')
    link = soup.find('a', class_='bookTitle').get('href')
    print(link)
    url = f'https://www.goodreads.com/{link}'
    return url

# Get author
def goodreads_author(soup):
    """
    Scrape author name of book
    :param soup:
    :return: author name as text
    """
    author = soup.find('span', class_='ContributorLink__name').get_text()

    print(author)
    return author

# Get book cover
def goodreads_book_image(soup):
    """
    Scrape book image of book
    :param soup:
    :return: the image source link
    """
    book_image = soup.find('img', class_="ResponsiveImage")
    return book_image['src']

def goodreads_ratings(soup):
    """
    Scrape average numeric rating of book
    :param soup:
    :return: rating as text
    """
    book_rating = soup.find('div', class_="RatingStatistics__rating").get_text()
    return book_rating

def goodreads_giveaway(soup) -> list:
    """
    Load page based on book genre of entered book, and scrape
    book cover
    :param soup:
    :return: image source links as a list
    """
    url = soup.find('a', class_="Button Button--tag-inline Button--small").get('href')
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    book = soup.find_all("img", class_="bookCover")
    if books_give:
        books_give.clear()
    for element in book:
        books_give.append(element.attrs['src'])
    return books_give

def goodreads_giveaway_title(soup) -> list:
    """
    Load page based on book genre of entered book, and scrape
    book titles
    :param soup:
    :return: book titles text as list
    """
    url = soup.find('a', class_="Button Button--tag-inline Button--small").get('href')
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    titles = soup.find_all(class_='bookTitle')
    if titles_give:
        titles_give.clear()
    for i in titles:
        titles_give.append(i.text)
    return titles_give

def get_genre(soup):
    time.sleep(2)
    genres = soup.find('a', class_="actionLinkLite bookPageGenreLink").get_text()
    return genres

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index', methods=["POST"])
def index2():
    global authors
    global image
    global ratings
    global books
    global giveaway_titles
    global book_input
    global genre
    if request.method == 'POST':
        try:
            book_input = request.form["book-name"]
            url = book_page(book_input)
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'html.parser')

            authors = goodreads_author(soup)
            print(authors)
            image = goodreads_book_image(soup)
            print(image)
            ratings = goodreads_ratings(soup)
            print(ratings)
            books = goodreads_giveaway(soup)
            print(books)
            giveaway_titles = goodreads_giveaway_title(soup)
            print(giveaway_titles)
            genre = get_genre(soup)
            print(genre)
            book_input = book_input.capitalize()
        except:
            error.append("Book not Found")
        if authors and image and book_input and genre:
            conn = get_db_connection()
            if book_input not in (conn.execute("Select Title from Book")):
                conn.execute('INSERT INTO book (Title, Author, Genre, Cover) VALUES (?, ?, ?, ?)',
                             (book_input, authors, genre, image))
                conn.commit()
                conn.close()
            else:
                print("In Book DB")
            return render_template("result.html", book_input=book_input, authors=authors, image=image, ratings=ratings,
                                   books=books, words=giveaway_titles)
        else:
            print(authors, book_input, genre)
            print("NOT FULLY LOADED")
    return render_template("result.html", book_input=book_input, authors=authors, image=image, ratings=ratings,
                           books=books, words=giveaway_titles)


#TBR
@app.route('/shelf', methods=('GET', 'POST'))
def shelf():
    conn = get_db_connection()
    users = conn.execute('Select * FROM user').fetchall()
    TBRs= conn.execute('Select * FROM TBR').fetchall()
    Books = conn.execute('Select * FROM book').fetchall()
    conn.close()
    #users = users, TBRs = TBRs,
    return render_template('shelf.html', Books=Books)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

