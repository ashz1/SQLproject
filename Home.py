import sqlite3
import streamlit as st
import pandas as pd
container = st.container(border=True)
container1 = st.container(border=True)
fdf = pd.read_csv('data/1.csv')
adf = pd.read_csv('data/2.csv')
conn = sqlite3.connect('ecom.db')
st.title("SQL Database Operations Demo by Aashay")
container.write("""Introduction:
I've created a simple CRUD SQL demo app using SQLite3 to demonstrate SQL queries. This data is based on my experience as a business and data analyst in India, although I've altered it significantly for demonstration purposes.

App Overview:
The app, built using Python's Streamlit library, allows users to perform basic CRUD (Create, Read, Update, Delete) operations on two datasets: one from Flipkart and one from Amazon. It provides an interactive interface for viewing, searching, updating, and deleting data, along with the SQL queries used. 
The code can be viewed on github, under the MIT license, feel free to use it for your own projects and please do not hesitate to drop me an email if you find any errors or have feedback, I'll appreciate it.
""")
# Add a new column to identify the source
fdf['Source'] = 'Flipkart'
adf['Source'] = 'Amazon'
# Reorder columns to place 'Source' after 'Month'
cols = fdf.columns.tolist()
cols.insert(cols.index('Month') + 1, cols.pop(cols.index('Source')))
fdf = fdf[cols]
adf = adf[cols]
# Function to create database and insert data from CSV
def create_database():
    fdf.to_sql('flipkart', conn, if_exists="replace", index=False)
    adf.to_sql('amazon', conn, if_exists="replace", index=False)
    conn.commit()

# Function to view all data in a table
def view_data(table):
    if table == 'both':
        query_flipkart = f"SELECT * FROM flipkart"
        query_amazon = f"SELECT * FROM amazon"
        result_flipkart = pd.read_sql(query_flipkart, conn)
        result_amazon = pd.read_sql(query_amazon, conn)
        return pd.concat([result_flipkart, result_amazon])
    else:
        query = f"SELECT * FROM {table}"
        return pd.read_sql(query, conn)

def main():
    

    # Create database and insert data from CSV if not already created
    create_database()

    # View operations
    st.sidebar.header("View Operations: 'SELECT * FROM {table}'")
    
    table_to_view = st.sidebar.selectbox("Choose a table to view", ["flipkart", "amazon", "both"], key="view_table")
    


    if st.sidebar.button("Click here to view"):
        result = view_data(table_to_view)
        st.header(f"Data in {table_to_view} Table:")
 
        container.write("""
            SQL CREATE VIEW Statement
             
                 In SQL, a view is a virtual table based on the result-set of an SQL statement.
                A view contains rows and columns, just like a real table. The fields in a view are fields from one or more real tables in the database.
                You can add SQL statements and functions to a view and present the data as if the data were coming from one single table. """)
        container1.write("""
            A view is created with the CREATE VIEW statement. 
                     CREATE VIEW Syntax
                    CREATE VIEW view_name AS
                    SELECT column1, column2, ...
                    FROM table_name
                    WHERE condition; """)
        container.write(""" 
                 Note: A view always shows up-to-date data! The database engine recreates the view, every time a user queries it.""")
        st.write(result)

    # Search operations
    st.sidebar.header("Search Operations: 'SELECT * FROM {table} WHERE {column} LIKE ?'")
    table = st.sidebar.selectbox("Choose a table", ["flipkart", "amazon", "both"])
    column = st.sidebar.selectbox("Choose a column", fdf.columns.tolist())
    value = st.sidebar.text_input("Search value")

    if st.sidebar.button("Click here to search"):
        result = search_data(table, column, value)
        st.header(f"Search Results in {table} for '{value}' in column '{column}':")
        st.write("""
            The SQL LIKE Operator
                     The LIKE operator is used in a WHERE clause to search for a specified pattern in a column.
                     There are two wildcards often used in conjunction with the LIKE operator: 
                     The percent sign % represents zero, one, or multiple characters. The underscore sign _ represents one, single character
            Syntax
                     SELECT column1, column2, ...
                     FROM table_name
                     WHERE columnN LIKE pattern;
            Contains
                     To return records that contains a specific letter or phrase, add the % both before and after the letter or phrase.
            Combine Wildcards
                     Any wildcard, like % and _ , can be used in combination with other wildcards.       
            Without Wildcard 
                     If no wildcard is specified, the phrase has to have an exact match to return a result.
                 """)
        st.write(result)
        conn.close()
    
if __name__ == '__main__':
    main()