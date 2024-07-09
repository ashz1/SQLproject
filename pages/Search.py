import sqlite3
import streamlit as st
import pandas as pd
container = st.container(border=True)
container.write("""
                
        **Filtering Results with WHERE:**
                
        The WHERE clause is used to filter records and return only those that meet specific conditions. This is useful for narrowing down the dataset to the relevant records you need for your analysis.
               
                
       
                
 **Pattern Matching with LIKE:**
                
      The LIKE operator is used to search for a specified pattern in a column. It supports wildcards like % for any sequence of characters and _ for a single character. This is particularly useful for searching within text fields.

**% matches zero or more characters.
_ matches exactly one character.**
                

Combining Conditions with AND, OR, and NOT
You can combine multiple conditions in a WHERE clause using AND, OR, and NOT to create more complex queries.

AND requires both conditions to be true.
OR requires at least one condition to be true.
NOT negates a condition.""")
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

# Function to search data in a table
def search_data(table, column, value):
    if table == 'both':
        query_flipkart = f"SELECT * FROM flipkart WHERE {column} LIKE ?"
        query_amazon = f"SELECT * FROM amazon WHERE {column} LIKE ?"
        result_flipkart = pd.read_sql(query_flipkart, conn, params=[f'%{value}%'])
        result_amazon = pd.read_sql(query_amazon, conn, params=[f'%{value}%'])
        result = pd.concat([result_flipkart, result_amazon])
    else:
        query = f"SELECT * FROM {table} WHERE {column} LIKE ?"
        result = pd.read_sql(query, conn, params=[f'%{value}%'])
    return result[['Month', 'Source'] + [col for col in result.columns if col not in ['Month', 'Source']]]

def main():
    # Create database and insert data from CSV if not already created
    create_database()

    st.write("### Select a table to search")
    table_to_search = st.selectbox("Choose a table to search", ["flipkart", "amazon", "both"], key="search_table")
    column_to_search = st.text_input("Enter the column to search")
    value_to_search = st.text_input("Enter the value to search for")

    if st.button("Search"):
        result = search_data(table_to_search, column_to_search, value_to_search)
        st.header(f"Search Results in {table_to_search.capitalize()} Table:")

        if table_to_search == "both":
            sql_statement = f"SELECT * FROM flipkart WHERE {column_to_search} LIKE '%{value_to_search}%' UNION SELECT * FROM amazon WHERE {column_to_search} LIKE '%{value_to_search}%';"
        else:
            sql_statement = f"SELECT * FROM {table_to_search} WHERE {column_to_search} LIKE '%{value_to_search}%';"

        st.write(f"### SQL SELECT Statement for {table_to_search.capitalize()} Table")
        st.code(sql_statement, language='sql')
        
        st.write(result)

        conn.close()

if __name__ == '__main__':
    main()