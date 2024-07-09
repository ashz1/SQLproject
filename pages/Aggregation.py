import sqlite3
import streamlit as st
import pandas as pd

container = st.container(border=True)
container.write("""
    **Aggregation Operations:**
    
    Aggregation functions are used to perform calculations on multiple rows of a single column of a table and return a single value. Common aggregation methods include SUM, AVG (average), COUNT, MAX (maximum), and MIN (minimum).

    **SQL Syntax:**
    ```sql
    SELECT AGGREGATION_FUNCTION(column_name)
    FROM table_name
    WHERE condition;
    ```

    **Example:**
    ```sql
    SELECT SUM("Gross Transactions (Mn)")
    FROM flipkart;
    ```

    - **Choose a table to aggregate:** Select either 'flipkart', 'amazon', or 'both'.
    - **Choose columns to aggregate:** Choose the columns you want to include in the aggregation.
    - **Choose an aggregation method:** Select the aggregation method (SUM, AVG, COUNT, MAX, MIN).

    Once you have provided these details, click the 'Aggregate' button to execute the aggregation operation.
""")

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

 # Function to aggregate data from a table
def aggregate_data(table, columns, method):
    agg_query = ", ".join([f'{method}("{col}") AS {method}_{col.replace(" ", "_").replace("(", "").replace(")", "")}' for col in columns])
    if table == 'both':
        query_flipkart = f'SELECT "Jan-21 to Mar-22" AS "Month", "Source", {agg_query} FROM flipkart'
        query_amazon = f'SELECT "Jan-21 to Mar-22" AS "Month", "Source", {agg_query} FROM amazon'
        result_flipkart = pd.read_sql(query_flipkart, conn)
        result_amazon = pd.read_sql(query_amazon, conn)
        return pd.concat([result_flipkart, result_amazon])
    else:
        query = f'SELECT "Jan-21 to Mar-22" AS "Month", "Source", {agg_query} FROM {table}'
        return pd.read_sql(query, conn)

def main():
    # Create database and insert data from CSV if not already created
    create_database()

    st.header("Aggregation Operations")
    table_to_aggregate = st.selectbox("Choose a table to aggregate", ["flipkart", "amazon", "both"], key="aggregate_table")
    columns_to_aggregate = st.multiselect("Choose columns to aggregate", [col for col in fdf.columns.tolist() if col not in ['Month', 'Source']])
    method = st.selectbox("Choose an aggregation method", ["SUM", "AVG", "COUNT", "MAX", "MIN"])

    if st.button("Click here to aggregate"):
        result = aggregate_data(table_to_aggregate, columns_to_aggregate, method)
        st.header(f"Aggregation Results in {table_to_aggregate.capitalize()} using '{method}':")
        st.write(result)

if __name__ == '__')__:
    main()