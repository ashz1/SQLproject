import sqlite3
import streamlit as st
import pandas as pd

def create_database(conn, fdf, adf):
    fdf.to_sql('flipkart', conn, if_exists="replace", index=False)
    adf.to_sql('amazon', conn, if_exists="replace", index=False)
    conn.commit()

def join_tables(conn):
    query = """
    SELECT * FROM flipkart INNER JOIN amazon
    ON flipkart.`common_column` = amazon.`common_column`
    """
    return pd.read_sql(query, conn)

def main():
    st.write("## Inner Join")

    container = st.container()
    container.write("""
    **Inner Join:**

    An INNER JOIN returns records that have matching values in both tables.
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
    create_database(conn, fdf, adf)

    result = join_tables(conn)
    st.write(result)

    conn.close()

if __name__ == '__main__':
    main()