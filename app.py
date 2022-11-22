import urllib.request
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
#headers = {
 #   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
  #                'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Accept-Language': 'en-US,en;q=0.5'
}

# Defining at the module level
books = ""
giveaway_titles = ""

# Lists to pass to html
error = []
books_give = []
titles_give = []

def book_page(searchterms):
    """
    Load main page based on book title entered
    :param searchterms:
    :return: url of book page
    """
    searchterms = "+".join(searchterms.split())
    url =  f'https://www.goodreads.com/search?q={searchterms}'
    r = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(r, 'html.parser')
    link = soup.find('a', class_='bookTitle').get('href')
    url = f'https://www.goodreads.com/{link}'
    return url

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index', methods=["POST"])
def index2():
    if request.method == 'POST':
        try:
            book_input = request.form["book-name"]
            url = book_page(book_input)
            r = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(r, 'html.parser')

            titleNauthor = (soup.title.contents[0]).split('by')  # can consistently get title and author from this
            author = titleNauthor[1].strip() #author name

            # ------------- generate smaller subsets of html to look through ------------ #
            b_tag = soup.body
            span_tag = soup.body.span
            a_tag = soup.body.a
            # ------------------------ get genre -------------------------------- #
            for b in b_tag.children:
                try:
                    genre = soup.find('a', class_="actionLinkLite bookPageGenreLink").get_text()
                except AttributeError as err:
                    genre = soup.find('span', class_="u-visuallyHidden").get_text()
                # get rating
            # ------------------------ get rating -------------------------------- #
            for s in span_tag.children:
                rating = soup.find('span', {'itemprop': 'ratingValue'}).text.strip()
                # get cover
            # ------------------------ get cover -------------------------------- #
            for a in a_tag:
                image = soup.find('img', {'id': 'coverImage'})
                cover = image['src']
            # ------------------ get Giveaway titles-----------------------------#
            for b in b_tag.children:
                u = soup.find('a', class_="actionLinkLite bookPageGenreLink").get('href')
            page = urllib.request.urlopen(f'https://www.goodreads.com/{u}').read()
            poup = BeautifulSoup(page, 'html.parser')  # poup, not to be mistaken with their prettier sister, soup who is the html of the first page

            titles = poup.find_all('a', class_='bookTitle')
            for i in titles:
                titles_give.append(i.get_text())

            #----------------- Get giveaway covers start ---------------------------#

            book = poup.find_all("img", class_="bookCover")
            for element in book:
                books_give.append(element.attrs['src'])
            # ----------------- Get giveaway covers start ---------------------------#
        except:
            error.append("Book not Found")

        conn = get_db_connection()
        if book_input not in (conn.execute("Select Title from Book")):
            conn.execute('INSERT INTO book (Title, Author, Genre, Cover) VALUES (?, ?, ?, ?)',
                         (book_input, author, genre, cover))
            conn.commit()
            conn.close()
        else:
            print("In Book DB")
        return render_template("result.html", book_input=book_input, authors=author, image=cover, ratings=rating, books=books_give, words=titles_give)

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


