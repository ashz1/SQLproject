import sqlite3
import streamlit as st
import pandas as pd
container = st.container(border=True)
container1 = st.container(border=True)
fdf = pd.read_csv('data/1.csv')
adf = pd.read_csv('data/2.csv')
conn = sqlite3.connect('ecom.db')
st.title("SQL Database Operations Demo by Aashay")
st.write("""Introduction:
I've created a simple CRUD SQL demo app using SQLite3 to demonstrate SQL queries. This data is based on my experience as a business and data analyst in India, although I've altered it significantly for demonstration purposes.

App Overview:
The app, built using Python's Streamlit library, allows users to perform basic CRUD (Create, Read, Update, Delete) operations on two datasets: one from Flipkart and one from Amazon. It provides an interactive interface for viewing, searching, updating, and deleting data, along with the SQL queries used. 
The code can be viewed on github, under the MIT license, feel free to use it for your own projects and please do not hesitate to drop me an email if you find any errors or have feedback, I'll appreciate it.
""")