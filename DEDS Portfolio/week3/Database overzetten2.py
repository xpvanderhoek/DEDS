#%%
import sqlite3
import pyodbc
import pandas as pd
import warnings
from pandas import DataFrame


#%%
server = r'Xanderslaptop\SQLEXPRESS'
database = 'TEST'
database2 = 'werkend'
databaseje = pyodbc.connect(f"DRIVER={{SQL Server}};SERVER={server};DATABASE={database}")

def get_sql_server_connection():
    try:
        conn = pyodbc.connect(f"DRIVER={{SQL Server}};SERVER={server};DATABASE={database2}")
        return conn
    except Exception as e:
        print("Error connecting to SQL Server:", e)
        raise


#%%
def delete_tables():
    conn = get_sql_server_connection()
    cursor = conn.cursor()

    cursor.execute("EXEC sp_msforeachtable 'ALTER TABLE ? NOCHECK CONSTRAINT ALL'")

    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_type = 'BASE TABLE'")
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]
        cursor.execute(f"DELETE FROM {table_name}")

    conn.commit()

    cursor.execute("EXEC sp_msforeachtable 'ALTER TABLE ? CHECK CONSTRAINT ALL'")

    cursor.close()

delete_tables()

#%%


sales_query = "SELECT * FROM product"
product_data = pd.read_sql_query(sales_query, databaseje)

product_type_query = "SELECT * FROM product_type"
product_type_data = pd.read_sql_query(product_type_query, databaseje)

product_line_query = "SELECT * FROM product_line"
product_line_data = pd.read_sql_query(product_line_query, databaseje)

merged_products = pd.merge(product_data, product_type_data, on='PRODUCT_TYPE_CODE', how='left')
merged_products = pd.merge(merged_products, product_line_data, on='PRODUCT_LINE_CODE', how='left')


merged_products = merged_products.rename(columns={'PRODUCT_NUMBER': 'Product_id', 'INTRODUCTION_DATE': 'Introduction_date', 'PRODUCTION_COST': 'Production_cost', 'MARGIN': 'Margin', 'PRODUCT_IMAGE': 'Product_image', 'LANGUAGE': 'Language', 'PRODUCT_NAME': 'Product_name', 'DESCRIPTION': 'Description', 'PRODUCT_TYPE_EN': 'Product_type_en', 'PRODUCT_LINE_EN': 'Product_line_en'})
merged_products = merged_products.drop(columns=[ 'PRODUCT_TYPE_CODE', 'PRODUCT_LINE_CODE'])

Course_query = "SELECT * FROM course"
Course_data = pd.read_sql_query(Course_query, databaseje)

Training_query = "SELECT * FROM training"
Training_data = pd.read_sql_query(Training_query, databaseje)
Training_data = Training_data.rename(columns={'SALES_STAFF_CODE': 'Sales_staff_id'})
Training_data = pd.merge(Training_data, Course_data, on='COURSE_CODE')
Training_data = Training_data.drop(columns=['COURSE_CODE'])

Satisfaction_type_query = "SELECT * FROM satisfaction_type"
Satisfaction_type_data = pd.read_sql_query(Satisfaction_type_query, databaseje)

Satisfaction_query = "SELECT * FROM satisfaction"
Satisfaction_data = pd.read_sql_query(Satisfaction_query, databaseje)
Satisfaction_data = Satisfaction_data.rename(columns={'SALES_STAFF_CODE': 'Sales_staff_id'})
Satisfaction_data = pd.merge(Satisfaction_data, Satisfaction_type_data, on='SATISFACTION_TYPE_CODE')
Satisfaction_data = Satisfaction_data.drop(columns=['SATISFACTION_TYPE_CODE'])

Returned_reason_query = "SELECT * FROM return_reason"
Returned_reason_data = pd.read_sql_query(Returned_reason_query, databaseje)

Returned_query = "SELECT * FROM returned_item"
Returned_data = pd.read_sql_query(Returned_query, databaseje)
Returned_data = Returned_data.rename(columns={'ORDER_DETAIL_CODE': 'Order_number', 'RETURN_CODE':'Return_id'})
Returned_data = pd.merge(Returned_data, Returned_reason_data, on='RETURN_REASON_CODE', how='left')
Returned_data = Returned_data.drop(columns=['RETURN_REASON_CODE'])

Sales_demographics_query = "SELECT * FROM sales_demographic"
Sales_demographics_data = pd.read_sql_query(Sales_demographics_query, databaseje)

Age_group_query = "SELECT * FROM age_group"
Age_group_data = pd.read_sql_query(Age_group_query, databaseje)
Sales_demographics_data = Sales_demographics_data.rename(columns={'RETAILER_CODEMR': 'Headquarters_id', 'DEMOGRAPHIC_CODE': 'Demographic_id'})
Sales_demographics_data = pd.merge(Sales_demographics_data, Age_group_data, on='AGE_GROUP_CODE')
Sales_demographics_data = Sales_demographics_data.drop(columns=['AGE_GROUP_CODE'])


Product_forecast_query = "SELECT * FROM product_forecast"
Product_forecast_data = pd.read_sql_query(Product_forecast_query, databaseje)
Product_forecast_data = Product_forecast_data.rename(columns={'PRODUCT_NUMBER': 'Product_id', 'EXPECTED_VOLUME': 'Forecast_quantity'})
Product_forecast_data['FORECAST_DATE'] = pd.to_datetime(
    Product_forecast_data[['YEAR', 'MONTH']].assign(day=1)
)
Product_forecast_data = Product_forecast_data.drop(columns=['YEAR', 'MONTH'])

Inventory_levels_query = "SELECT * FROM inventory_levels"
Inventory_levels_data = pd.read_sql_query(Inventory_levels_query, databaseje)
Inventory_levels_data = Inventory_levels_data.rename(columns={'PRODUCT_NUMBER': 'Product_id', 'INVENTORY_COUNT': 'Stock_quantity'})
Inventory_levels_data['Inventory_date'] = pd.to_datetime(
    Inventory_levels_data['INVENTORY_YEAR'].astype(str) + '-' +
    Inventory_levels_data['INVENTORY_MONTH'].astype(str).str.zfill(2) + '-01',
    format='%Y-%m-%d',
    errors='coerce'  # Hierdoor worden fouten vervangen door NaT
)
Inventory_levels_data = Inventory_levels_data.drop(columns=['INVENTORY_YEAR', 'INVENTORY_MONTH'])

Country_query = "SELECT * FROM country"
Country_data = pd.read_sql_query(Country_query, databaseje)
Segment_query = "SELECT * FROM retailer_segment"
Segment_data = pd.read_sql_query(Segment_query, databaseje)
Sales_territory_query = "SELECT * FROM sales_territory"
Sales_territory_data = pd.read_sql_query(Sales_territory_query, databaseje)

Headquarters_query = "SELECT * FROM retailer_headquarters"
Headquarters_data = pd.read_sql_query(Headquarters_query, databaseje)
test = Headquarters_data
Headquarters_data = pd.merge(Headquarters_data, Country_data, on='COUNTRY_CODE', how='left')
Headquarters_data = pd.merge(Headquarters_data, Sales_territory_data, on='SALES_TERRITORY_CODE', how='left')
Headquarters_data = Headquarters_data.rename(columns={'RETAILER_CODEMR': 'Headquarters_id', 'LANGUAGE': 'Country_language', 'TERRITORY_NAME_EN': 'Territory_en'})
Headquarters_data = pd.merge(Headquarters_data, Segment_data, on='SEGMENT_CODE', how='left')
Headquarters_data = Headquarters_data.drop(columns=['COUNTRY_CODE', 'SALES_TERRITORY_CODE', 'SEGMENT_CODE', 'Country_language', 'CURRENCY_NAME'])

RetailerType_query = "SELECT * FROM retailer_type"
RetailerType_data = pd.read_sql_query(RetailerType_query, databaseje)

RetailerSite_query = "SELECT * FROM retailer_site"
RetailerSite_data = pd.read_sql_query(RetailerSite_query, databaseje)

RetailerContact_query = "SELECT * FROM retailer_contact"
RetailerContact_data = pd.read_sql_query(RetailerContact_query, databaseje)

Retailer_query = "SELECT * FROM retailer"
Retailer_data = pd.read_sql_query(Retailer_query, databaseje)
Retailer_data = pd.merge(Retailer_data, RetailerType_data, on='RETAILER_TYPE_CODE', how='left')
Retailer_data = pd.merge(RetailerSite_data, Retailer_data, on='RETAILER_CODE', how='left')
Retailer_data = pd.merge(Retailer_data, RetailerContact_data, on='RETAILER_SITE_CODE', how='left')
Retailer_data = pd.merge(Retailer_data, Country_data, on='COUNTRY_CODE', how='left')
Retailer_data = pd.merge(Retailer_data, Sales_territory_data, on='SALES_TERRITORY_CODE', how='left')
Retailer_data = Retailer_data.rename(columns={'RETAILER_CODEMR': 'Headquarters_id', 'RETAILER_SITE_CODE': 'Retailer_id', 'E_MAIL': 'Email'})
Retailer_data = Retailer_data.drop(columns=['RETAILER_TYPE_CODE', 'SALES_TERRITORY_CODE', 'RETAILER_CONTACT_CODE', 'COUNTRY_CODE', 'RETAILER_CODE'])

Branch_query = "SELECT * FROM Sales_branch"
Branch_data = pd.read_sql_query(Branch_query, databaseje)

Staff_query = "SELECT * FROM Sales_staff"
Staff_data = pd.read_sql_query(Staff_query, databaseje)
Staff_data = pd.merge(Staff_data, Branch_data, on='SALES_BRANCH_CODE', how='left')
Staff_data = pd.merge(Staff_data, Country_data, on='COUNTRY_CODE', how='left')
Staff_data = pd.merge(Staff_data, Sales_territory_data, on='SALES_TERRITORY_CODE', how='left')
Staff_data = Staff_data.rename(columns={'SALES_STAFF_CODE': 'Sales_staff_id', 'MANAGER_CODE': 'Manager_id'})
Staff_data = Staff_data.drop(columns=['SALES_TERRITORY_CODE', 'COUNTRY_CODE', 'SALES_BRANCH_CODE'])


OrderDetails_query = "SELECT * FROM Order_Details"
OrderDetails_data = pd.read_sql_query(OrderDetails_query, databaseje)
OrderDetails_data = OrderDetails_data.rename(columns={'ORDER_NUMBER': 'Sales_id', 'ORDER_DETAIL_CODE': 'Order_number'})

OrderMethod_query = "SELECT * FROM Order_Method"
OrderMethod_data = pd.read_sql_query(OrderMethod_query, databaseje)

Sales_query = "SELECT * FROM Order_header"
Sales_data = pd.read_sql_query(Sales_query, databaseje)
Sales_data = pd.merge(Sales_data, OrderMethod_data, on='ORDER_METHOD_CODE', how='left')
Sales_data = Sales_data.rename(columns={'ORDER_NUMBER': 'Sales_id', 'SALES_STAFF_CODE': 'Sales_staff_id', 'RETAILER_SITE_CODE': 'Retailer_id'})


Sales_data = pd.merge(Sales_data, OrderDetails_data, on='Sales_id', how='left')
Sales_data['Korting'] = ((Sales_data['UNIT_PRICE'] - Sales_data['UNIT_SALE_PRICE']) != 0).astype(int)
Sales_data['ORDER_DATE'] = pd.to_datetime(Sales_data['ORDER_DATE'])

def determine_season(month):
    if month in [3, 4, 5]:
        return 'Lente'
    elif month in [6, 7, 8]:
        return 'Zomer'
    elif month in [9, 10, 11]:
        return 'Herfst'
    else:
        return 'Winter'


Sales_data['Kosten'] = Sales_data['UNIT_COST'] * Sales_data['QUANTITY']

Sales_data['Seizoen'] = Sales_data['ORDER_DATE'].dt.month.apply(determine_season)

Sales_data['Totaal_prijs'] = Sales_data['UNIT_SALE_PRICE'] * Sales_data['QUANTITY']

Sales_data['Kortingprijs'] = (Sales_data['UNIT_PRICE'] - Sales_data['UNIT_SALE_PRICE']) * Sales_data['QUANTITY']

Sales_data['Totale_Prijs'] = Sales_data.groupby('Sales_id')['Totaal_prijs'].transform('sum')
Sales_data['Totale_Kosten'] = Sales_data.groupby('Sales_id')['Kosten'].transform('sum')
Sales_data['Totale_korting'] = Sales_data.groupby('Sales_id')['Kortingprijs'].transform('sum')

Sales_data['Korting'] = (Sales_data['Totale_korting'] != 0)

Sales_data['Bestellingslaag'] = Sales_data['Totale_Prijs'].apply(lambda x: 'Duur' if x > 30000 else 'Goedkoop')

Sales_data['Omzet'] = (Sales_data['Totale_Prijs'] - Sales_data['Totale_Kosten'])

Sales_data = Sales_data.drop(columns=['RETAILER_NAME', 'Kortingprijs', 'Totaal_prijs', 'RETAILER_CONTACT_CODE', 'SALES_BRANCH_CODE', 'ORDER_METHOD_CODE', 'Order_number', 'PRODUCT_NUMBER', 'QUANTITY', 'UNIT_COST', 'UNIT_PRICE', 'UNIT_SALE_PRICE'])

grouped_sales_data = Sales_data.groupby('Sales_id').agg({
    'Retailer_id': 'first',  # Je kunt kiezen om de eerste waarde per Sales_id te nemen
    'Sales_staff_id': 'first',
    'ORDER_DATE': 'first',  # Kies een representatieve datum per Sales_id
    'ORDER_METHOD_EN': 'first',  # Je kunt kiezen om de eerste waarde per Sales_id te nemen
    'Korting': 'max',  # Kies de max waarde voor Korting (of pas aan zoals nodig)
    'Seizoen': 'first',  # Kies de eerste waarde van Seizoen per Sales_id
    'Totale_Prijs': 'sum',  # Bereken de som van Totale_Prijs per Sales_id
    'Totale_korting': 'sum',  # Bereken de som van Totale_korting per Sales_id
    'Bestellingslaag': 'first',  # Kies de eerste waarde van Bestellingslaag per Sales_id
    'Omzet': 'first'
}).reset_index()

pd.set_option('display.float_format', lambda x: '%.3f' % x)
#%%
printje = grouped_sales_data.head(1000)
print(printje.to_string())


#%%
def clean_and_handle_data(df):
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    for col in df.select_dtypes(include=['float64', 'float32']):
        df[col] = df[col].fillna(0).astype('Int64', errors='ignore')

    for col in df.select_dtypes(include=['object']):
        df[col] = df[col].fillna('')

    return df

def insert_data_to_sql_server(df, table_name):
    conn = get_sql_server_connection()
    cursor = conn.cursor()
    df = clean_and_handle_data(df)
    columns = ', '.join(df.columns)
    values_placeholder = ', '.join(['?'] * len(df.columns))
    insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({values_placeholder})"

    for index, row in df.iterrows():
        try:
            cursor.execute(insert_query, tuple(row))
            print(f"Goede insert bij row {index} in {table_name}")
        except Exception as e:
            print(f"Error inserting row {index} in {table_name}: {e}")

    conn.commit()
    cursor.close()
    conn.close()


#%%
insert_data_to_sql_server(Training_data, 'Training')
insert_data_to_sql_server(Satisfaction_data, 'Satisfaction')
insert_data_to_sql_server(Returned_data, 'Returned_item')
insert_data_to_sql_server(Sales_demographics_data, 'Sales_demographic')
insert_data_to_sql_server(Product_forecast_data, 'Product_forecast')
insert_data_to_sql_server(Inventory_levels_data, 'Inventory_levels')
insert_data_to_sql_server(merged_products, 'Product')
insert_data_to_sql_server(Headquarters_data, 'Retailer_headquarters')
insert_data_to_sql_server(Retailer_data, 'Retailer')
insert_data_to_sql_server(Staff_data, 'Sales_staff')
insert_data_to_sql_server(OrderDetails_data, 'Order_details')
insert_data_to_sql_server(grouped_sales_data, 'Sales')


#%%
databaseje.close()
get_sql_server_connection().close()

