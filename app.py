import sys
import json


import requests
import re
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, redirect, url_for,Response
from requests.exceptions import HTTPError

app = Flask(__name__)

words = []
error = []
books = []
author = []


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/index',methods=["POST"])
def index():
    if request.method == 'POST':
        try:
            genre = request.form["genre"]
            url = f"https://www.goodreads.com/genres/{genre}"
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'html.parser')
            # m = soup.find("div", {"class": "giveawayList"})
            m = soup.find_all(class_='bookTitle')

            #authors = soup.find("div", {"id": "bookAuthors"})
           # for j in authors:
              #  author.append(j.text)
            #book = soup.a.img.find_all(class_='bookCover').src

            book = soup.find_all("img", class_="bookCover")
            if books:
                books.clear()
            for element in book:
                books.append(element.attrs['src'])

            #final = json.dumps(books)
            print(books)
            #print(final)
            #book = soup.a.img['src']
            # if dictionary not empty, clear
            if words or error:
                words.clear()
                error.clear()
            # append text to dictionary
            for i in m:
                words.append(i.text)
            # error with input genre
        except:
            error.append("Genre not found")

    return render_template("index.html", words=words, error=error, books=books, len=len(books), author=author)


@app.route('/result', methods=["POST"])
def result():
    words = request.form.get("words")
    return render_template('result.html', words=words)


if __name__ == '__main__':
    app.run(debug=True, port=5000)