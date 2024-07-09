import sqlite3
import streamlit as st
import pandas as pd

container = st.container(border=True)
container.write("Update Operations")

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

# Function to update data in a table
def update_data(table, column, old_value, new_value):
    query = f"UPDATE {table} SET {column} = ? WHERE {column} = ?"
    cur = conn.cursor()
    cur.execute(query, (new_value, old_value))
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

    st.header("Update Operations")
    table_to_update = st.selectbox("Choose a table to update", ["flipkart", "amazon"], key="update_table")
    column_to_update = st.selectbox("Choose a column to update", [
        "Month", "Source", "Gross Transactions (Mn)", "Shipped Transactions (Mn)", "Checkout GMV (USD Mn)", "Shipped GMV (USD Mn)", 
        "Fulfilled GMV i.e. GMV post Return (USD Mn)", "Average Order Value per transaction (USD)", "ASP per item (USD)", 
        "Mobiles (USD Mn)", "Electronic Devices (USD Mn)", "Large & Small Appliances (USD Mn)", "% COD", "% Prepaid", 
        "Orders shipped per day Lacs", "% Returns(RTO+RVP)", "% share of Captive", "% share of 3PL", "% Metro", "% Tier-I", 
        "% Others", "Revenue from Operations (Take Rate + Delivery Charges ) (USD Mn)", "Other Revenue (USD Mn)", 
        "Total Revenue (USD Mn)", "Supply Chain Costs (Fixed and Variable Included) (USD Mn)", 
        "Payment Gateway Costs (Only on the Pre-paid orders) (USD Mn)", "Marketing Expediture (USD Mn)", 
        "Contribution Margin (as % of Fulfilled GMV)", "Tech & Admin/Employee Costs and other costs (USD Mn)", "Cash Burn (USD Mn)"
    ], key="update_column")
    old_value = st.text_input("Old value")
    new_value = st.text_input("New value")

    if st.button("Click here to update"):
        update_data(table_to_update, column_to_update, old_value, new_value)
        st.success("Data updated successfully")
        result = view_data(table_to_update)
        st.write(result)

if __name__ == '__main__':
    main()