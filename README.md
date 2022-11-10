# webscrape-goodreads
# Overview
A flask web application that webscrapes [Goodreads](https://www.goodreads.com/) to find tags that contains information such as author, current giveaways for related genre, and ratings. The user enters the title of the book they want to search for, and the corresponding results are displayed. This software is being created using python, CSS, HTML, and SQL. 

<img width="400" alt="Screen Shot 2022-11-08 at 6 12 04 PM" src="https://user-images.githubusercontent.com/68759170/200696094-39c96f33-d714-4cf8-ad09-cdb3258e3880.png">

<img width="400" alt="Screen Shot 2022-11-08 at 6 12 33 PM" src="https://user-images.githubusercontent.com/68759170/200696105-3e04ac17-78e0-4ca6-aae8-b047484c58ae.png">       <img width="375" alt="Screen Shot 2022-11-08 at 6 12 44 PM" src="https://user-images.githubusercontent.com/68759170/200696113-641a516e-e230-4f6d-9646-ce84bfab1fdd.png">

# Purpose:
Allows user to search through Goodreads for book recommendations based off the book of their choosing. User will be able to add the books to their cart, where they can choose to export, as am xml file. This will provide the user with the list of books they want, along with the link to purchase the book at Barnes and Noble. 

# MVP Requirements:

1.	Create a backend with enough tables to hold shopping cart information for user – json, SQLite
2.	Have main page where user can search for book recommendations. Recommendations gathered from Goodreads. 
3.	Have “add to cart” button that will push information to backend and hold for shopping cart 
4.	Have “Download Shopping Cart” button for user to download xml of shopping cart information
5.	Aesthetically pleasing front end design
6.  Add error checking (eg user enters non-existing book title)

# Potential Features/Upgrades:

1.	Adding sorting (eg, sort books by author, genre, ratings)
2.	Create own recommendations using Affinity or Market Basket analysis 
3.	Incorporate better scrapping methods 
4.	Use Goodreads API to allow users to synch to their Goodreads account
5.	Use Product API to allows users to add to carts on Amazon
6.	STMP

