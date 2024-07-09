import sqlite3
import streamlit as st
import pandas as pd

container = st.container(border=True)
container.write("""
    **Delete Operations:**
    
    The DELETE statement is used to remove existing records from a table. This operation is crucial for maintaining the integrity and relevance of your data by removing outdated or incorrect entries.

    **SQL Syntax:**
    ```sql
    DELETE FROM table_name
    WHERE condition;
    ```

    **Example:**
    ```sql
    DELETE FROM flipkart
    WHERE "Month" = Jan-21;
    ```

    - **Choose a table to delete from:** Select either 'flipkart' or 'amazon'.
    - **Choose a column to delete from:** Choose the column based on which the deletion will be performed.
    - **Value to delete:** Specify the value of the column for the rows you want to delete.

    Once you have provided these details, click the 'Delete' button to execute the delete operation.
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

# Function to delete data from a table
def delete_data(table, column, value):
    query = f"DELETE FROM {table} WHERE {column} = ?"
    cur = conn.cursor()
    cur.execute(query, (value,))
    conn.commit()
    cur.close()

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

    st.header("Delete Operations")
    table_to_delete = st.selectbox("Choose a table to delete from", ["flipkart", "amazon"], key="delete_table")
    column_to_delete = st.selectbox("Choose a column to delete from", [
        "Month", "Source", "Gross Transactions (Mn)", "Shipped Transactions (Mn)", "Checkout GMV (USD Mn)", "Shipped GMV (USD Mn)", 
        "Fulfilled GMV i.e. GMV post Return (USD Mn)", "Average Order Value per transaction (USD)", "ASP per item (USD)", 
        "Mobiles (USD Mn)", "Electronic Devices (USD Mn)", "Large & Small Appliances (USD Mn)", "% COD", "% Prepaid", 
        "Orders shipped per day Lacs", "% Returns(RTO+RVP)", "% share of Captive", "% share of 3PL", "% Metro", "% Tier-I", 
        "% Others", "Revenue from Operations (Take Rate + Delivery Charges ) (USD Mn)", "Other Revenue (USD Mn)", 
        "Total Revenue (USD Mn)", "Supply Chain Costs (Fixed and Variable Included) (USD Mn)", 
        "Payment Gateway Costs (Only on the Pre-paid orders) (USD Mn)", "Marketing Expediture (USD Mn)", 
        "Contribution Margin (as % of Fulfilled GMV)", "Tech & Admin/Employee Costs and other costs (USD Mn)", "Cash Burn (USD Mn)"
    ], key="delete_column")
    value_to_delete = st.text_input("Value to delete")

    if st.button("Click here to delete"):
        delete_data(table_to_delete, column_to_delete, value_to_delete)
        st.success("Data deleted successfully")
        result = view_data(table_to_delete)
        st.write(result)

if __name__ == '__main__':
    main()