import sqlite3
import streamlit as st
import pandas as pd

def create_database(conn, fdf, adf):
    fdf.to_sql('flipkart', conn, if_exists="replace", index=False)
    adf.to_sql('amazon', conn, if_exists="replace", index=False)
    conn.commit()

def window_functions():
    conn = sqlite3.connect('ecom.db')

    query = """
    SELECT
        FLP_Month,
        FLP_Gross_Transactions (Mn) AS Gross_Transactions (Mn),
        AVG(FLP_Gross_Transactions (Mn)) OVER (PARTITION BY FLP_Month) AS Avg_Gross_Transactions (Mn)
    FROM flipkart
    """
    result = pd.read_sql(query, conn)
    conn.close()
    return result, query

def main():
    st.write("## Window Functions")
    st.write("""
    **Window Functions:** These functions perform a calculation across a set of table rows that are somehow related to the current row.
    """)
    
    result, query = window_functions()
    st.write("### SQL Query")
    st.code(query, language='sql')
    st.write("### Window Function Result")
    st.write(result)

if __name__ == '__main__':
    # Read CSV files
    fdf = pd.read_csv('data/1.csv')
    adf = pd.read_csv('data/2.csv')
    
    # Rename columns to avoid issues with spaces and special characters
    fdf.columns = [col.replace(' ', '_').replace('(', '').replace(')', '') for col in fdf.columns]
    adf.columns = [col.replace(' ', '_').replace('(', '').replace(')', '') for col in adf.columns]
    
    # Add prefixes to the columns of each table
    fdf_prefixed = fdf.add_prefix('FLP_')
    adf_prefixed = adf.add_prefix('AMZN_')
    
    # Merge the datasets
    conn = sqlite3.connect('ecom.db')
    create_database(conn, fdf_prefixed, adf_prefixed)
    
    main()