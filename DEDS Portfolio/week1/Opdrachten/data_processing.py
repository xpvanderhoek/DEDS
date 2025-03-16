import pandas as pd
import sqlite3


def get_database_connection():
    conn = sqlite3.connect("C:\\Users\\xande\\PycharmProjects\\DEDS\\DEDS Portfolio\\week1\\Data\\go_sales_train.sqlite")
    return conn

def load_tables(tabel_naam):
    conn = get_database_connection()
    tables_query = "SELECT name FROM sqlite_master WHERE type='table'"
    tables = pd.read_sql(tables_query, conn)

    df = {}

    for table_name in tables['name']:
        query = f"SELECT * FROM {table_name}"
        df[table_name] = pd.read_sql(query, conn)

    table = df[tabel_naam]

    return table

def vraag5(retailer_site):
    adresVerkoop = ((retailer_site['ADDRESS2'].notna()) & (retailer_site['REGION'].notna()))
    return retailer_site.loc[adresVerkoop, ['ADDRESS1', 'CITY']].head(7)


def vraag6(country):
    landenMetDollar = (country['CURRENCY_NAME'].isin(['dollars', 'new dollar']))
    return country.loc[landenMetDollar, ['COUNTRY']].sort_values(by='COUNTRY')


def vraag7(sales_branch):
    postcodeIsD = sales_branch['POSTAL_ZONE'].str.startswith('D')
    return sales_branch.loc[postcodeIsD, ['ADDRESS1', 'ADDRESS2', 'CITY']].sort_values(by='ADDRESS2')


def vraag8(returned_item):
    return returned_item['RETURN_QUANTITY'].sum()


def vraag9(sales_branch):
    return sales_branch['REGION'].count()
