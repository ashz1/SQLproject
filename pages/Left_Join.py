import sqlite3
import streamlit as st
import pandas as pd

def join_data():
    # Connect to SQLite database
    conn = sqlite3.connect('ecom.db')

    # Read CSV files
    fdf = pd.read_csv('data/1.csv')
    adf = pd.read_csv('data/2.csv')

    # Add prefixes to the columns of each table
    fdf_prefixed = fdf.add_prefix('FLP_')
    adf_prefixed = adf.add_prefix('AMZN_')

    # Merge the datasets
    fdf_prefixed.to_sql('flipkart_prefixed', conn, if_exists="replace", index=False)
    adf_prefixed.to_sql('amazon_prefixed', conn, if_exists="replace", index=False)

    join_query = """
    SELECT flipkart_prefixed.FLP_Month as Month, flipkart_prefixed.*, amazon_prefixed.AMZN_Month, amazon_prefixed.*
    FROM flipkart_prefixed
    LEFT JOIN amazon_prefixed
    ON flipkart_prefixed.FLP_Month = amazon_prefixed.AMZN_Month
    """
    
    result = pd.read_sql(join_query, conn)
    
    # Remove duplicate 'Month' columns and 'Source' columns
    result = result.loc[:, ~result.columns.duplicated()]
    result = result.drop(columns=['FLP_Source', 'AMZN_Source'], errors='ignore')
    
    conn.close()
    return result, join_query

def main():
    st.write("## Left Join")
    st.write("""
    **Left Join:** A LEFT JOIN returns all records from the left table, and the matched records from the right table.
    """)
    
    result, join_query = join_data()
    st.write("### SQL Query")
    st.code(join_query, language='sql')
    st.write("### Join Result")
    st.write(result)

if __name__ == '__main__':
    main()