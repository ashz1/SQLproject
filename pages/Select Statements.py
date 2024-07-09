import sqlite3
import streamlit as st
import pandas as pd
container = st.container()
container.write("The SELECT statement is used to select data from a database.", border=True)
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
        
        if table_to_view == "both":
            sql_statement = "SELECT * FROM flipkart UNION SELECT * FROM amazon;"
        else:
            sql_statement = f"SELECT * FROM {table_to_view};"

        st.write(f"### SQL SELECT Statement for {table_to_view.capitalize()} Table")
        st.code(sql_statement, language='sql')
        
        st.write(result)

        conn.close()

if __name__ == '__main__':
    main()