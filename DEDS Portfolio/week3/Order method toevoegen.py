import sqlite3
import pandas as pd
import pyodbc

DB = {'servername' : r'Xanders-pc\SQLEXPRESS',
        'database' : 'TEST'}


export_conn = pyodbc.connect('DRIVER={SQL Server};SERVER=' +
                             DB['servername'] +
                             ';DATABASE=' +
                             DB['database'] +
                             ';Trusted_Connection=yes'
)
export_cursor = export_conn.cursor()

go_sales_conn = sqlite3.connect('..\\week1\\Data\\go_sales_train.sqlite')

# Data ophalen uit SQLite
df = pd.read_sql("SELECT * FROM ORDER_METHOD", go_sales_conn)

go_sales_conn.close()

# Zet de data van SQLite in SQL Server
def insert_data(df, table_name):
    cursor = export_conn.cursor()

    # Kolomnamen ophalen
    columns = ', '.join(df.columns)
    placeholders = ', '.join(['?'] * len(df.columns))  # Voor parameterized queries
    insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

    # Rijen één voor één invoegen
    for _, row in df.iterrows():
        cursor.execute(insert_query, tuple(row))

    export_conn.commit()
    cursor.close()

# Voer de functie uit voor je specifieke tabel
insert_data(df, 'ORDER_METHOD')

export_conn.close()