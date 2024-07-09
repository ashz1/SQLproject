import sqlite3
import streamlit as st
import pandas as pd

# Read CSV files
fdf = pd.read_csv('data/1.csv')
adf = pd.read_csv('data/2.csv')

# Add a new column to identify the source
fdf['Source'] = 'Flipkart'
adf['Source'] = 'Amazon'

# Reorder columns to place 'Source' after 'Month'
cols = fdf.columns.tolist()
cols.insert(cols.index('Month') + 1, cols.pop(cols.index('Source')))
fdf = fdf[cols]
adf = adf[cols]

# Connect to SQLite database
conn = sqlite3.connect('ecom.db')

# Function to create database and insert data from CSV
def create_database():
    fdf.to_sql('flipkart', conn, if_exists="replace", index=False)
    adf.to_sql('amazon', conn, if_exists="replace", index=False)
    conn.commit()

# Function to view all data in a table
def view_data(table):
    if table == 'both':
        query_flipkart = "SELECT * FROM flipkart"
        query_amazon = "SELECT * FROM amazon"
        result_flipkart = pd.read_sql(query_flipkart, conn)
        result_amazon = pd.read_sql(query_amazon, conn)
        return pd.concat([result_flipkart, result_amazon])
    else:
        query = f"SELECT * FROM {table}"
        return pd.read_sql(query, conn)

def main():
    # Create database and insert data from CSV if not already created
    create_database()

    st.write("### Select a table to view")
    table_to_view = st.selectbox("Choose a table to view", ["flipkart", "amazon", "both"], key="view_table")

    if st.button("Click here to view"):
        result = view_data(table_to_view)
        st.header(f"Data in {table_to_view.capitalize()} Table:")

        st.write("""
            ## SQL CREATE VIEW Statement
             
            In SQL, a view is a virtual table based on the result-set of an SQL statement.
            A view contains rows and columns, just like a real table. The fields in a view are fields from one or more real tables in the database.
            You can add SQL statements and functions to a view and present the data as if the data were coming from one single table.
            
            ### CREATE VIEW Syntax
            ```
            CREATE VIEW view_name AS
            SELECT column1, column2, ...
            FROM table_name
            WHERE condition;
            ```

            Note: A view always shows up-to-date data! The database engine recreates the view every time a user queries it.
        """)
        st.write(result)

        conn.close()

if __name__ == '__main__':
    main()