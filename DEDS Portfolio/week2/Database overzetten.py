#%%
import sqlite3
import pyodbc
import pandas as pd

server = r'Xanderslaptop\SQLEXPRESS'
database = 'TEST'
#%%
go_sales_con = sqlite3.connect('go_sales_train.sqlite')
go_staff_con = sqlite3.connect('go_staff_train.sqlite')
go_crm_con = sqlite3.connect('go_crm_train.sqlite')

inventory_levels = pd.read_csv('inventory_levels_train.csv', header=0)
product_forecast = pd.read_csv('product_forecast_train.csv', header=0)

def get_sql_server_connection():
    try:
        conn = pyodbc.connect(f"DRIVER={{SQL Server}};SERVER={server};DATABASE={database}")
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
product_data = pd.read_sql_query(sales_query, go_sales_con)

product_type_query = "SELECT * FROM product_type"
product_type_data = pd.read_sql_query(product_type_query, go_sales_con)

product_line_query = "SELECT * FROM product_line"
product_line_data = pd.read_sql_query(product_line_query, go_sales_con)

sales_staff_query = "SELECT * FROM sales_staff"
sales_staff_data = pd.read_sql_query(sales_staff_query, go_staff_con)

sales_branch_query = "SELECT * FROM sales_branch"
sales_branch_data = pd.read_sql_query(sales_branch_query, go_sales_con)

retailer_site_query = "SELECT * FROM retailer_site"
retailer_site_data = pd.read_sql_query(retailer_site_query, go_sales_con)


country_query_crm = "SELECT * FROM country"
country_crm = pd.read_sql_query(country_query_crm, go_crm_con)
country_query_sales = "SELECT * FROM country"
country_sales = pd.read_sql_query(country_query_sales, go_sales_con)
country_sales = country_sales.rename(columns={"COUNTRY": "COUNTRY_EN"})
merged_data = pd.merge(country_crm, country_sales, on="COUNTRY_CODE", how="outer")
merged_data = merged_data.drop(columns=["COUNTRY_EN_y"], errors="ignore")
merged_data = merged_data.rename(columns={"COUNTRY_EN_x": "COUNTRY_EN"})


order_header_query = "SELECT * FROM order_header"
order_header_data = pd.read_sql_query(order_header_query, go_sales_con)

order_details_query = "SELECT * FROM order_details"
order_details_data = pd.read_sql_query(order_details_query, go_sales_con)

returned_item_query = "SELECT * FROM returned_item"
returned_item_data = pd.read_sql_query(returned_item_query, go_sales_con)

return_reason_query = "SELECT * FROM return_reason"
return_reason_data = pd.read_sql_query(return_reason_query, go_sales_con)

course_query = "SELECT * FROM course"
course_data = pd.read_sql_query(course_query, go_staff_con)

satisfaction_query = "SELECT * FROM satisfaction"
satisfaction_data = pd.read_sql_query(satisfaction_query, go_staff_con)

satisfaction_type_query = "SELECT * FROM satisfaction_type"
satisfaction_type_data = pd.read_sql_query(satisfaction_type_query, go_staff_con)

training_query = "SELECT * FROM training"
training_data = pd.read_sql_query(training_query, go_staff_con)

age_group_query = "SELECT * FROM age_group"
age_group_data = pd.read_sql_query(age_group_query, go_crm_con)

retailer_query = "SELECT * FROM retailer"
retailer_data = pd.read_sql_query(retailer_query, go_crm_con)

retailer_contact_query = "SELECT * FROM retailer_contact"
retailer_contact_data = pd.read_sql_query(retailer_contact_query, go_crm_con)

retailer_headquarters_query = "SELECT * FROM retailer_headquarters"
retailer_headquarters_data = pd.read_sql_query(retailer_headquarters_query, go_crm_con)

retailer_segment_query = "SELECT * FROM retailer_segment"
retailer_segment_data = pd.read_sql_query(retailer_segment_query, go_crm_con)

retailer_site_query_crm = "SELECT * FROM retailer_site"
retailer_site_data_crm = pd.read_sql_query(retailer_site_query_crm, go_crm_con)

retailer_type_query = "SELECT * FROM retailer_type"
retailer_type_data = pd.read_sql_query(retailer_type_query, go_crm_con)

sales_demographic_query = "SELECT * FROM sales_demographic"
sales_demographic_data = pd.read_sql_query(sales_demographic_query, go_crm_con)

sales_territory_query = "SELECT * FROM sales_territory"
sales_territory_data = pd.read_sql_query(sales_territory_query, go_crm_con)

inventory_levels_data = inventory_levels
product_forecast_data = product_forecast

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
        except Exception as e:
            print(f"Error inserting row {index} in {table_name}: {e}")

    conn.commit()
    cursor.close()
    conn.close()


#%%

insert_data_to_sql_server(sales_territory_data, 'Sales_Territory')
insert_data_to_sql_server(product_line_data, 'Product_Line')
insert_data_to_sql_server(retailer_segment_data, 'Retailer_Segment')
insert_data_to_sql_server(retailer_type_data, 'Retailer_Type')
insert_data_to_sql_server(satisfaction_type_data, 'Satisfaction_Type')
insert_data_to_sql_server(course_data, 'Course')
insert_data_to_sql_server(age_group_data, 'Age_Group')
insert_data_to_sql_server(return_reason_data, 'Return_Reason')


#%%

insert_data_to_sql_server(merged_data, 'Country')
insert_data_to_sql_server(sales_branch_data, 'Sales_Branch')
insert_data_to_sql_server(product_type_data, 'Product_Type')
insert_data_to_sql_server(retailer_headquarters_data, 'Retailer_Headquarters')
insert_data_to_sql_server(sales_staff_data, 'Sales_Staff')
#%%
insert_data_to_sql_server(retailer_data, 'Retailer')
insert_data_to_sql_server(retailer_site_data, 'Retailer_Site')
insert_data_to_sql_server(product_data, 'Product')
insert_data_to_sql_server(satisfaction_data, 'Satisfaction')
insert_data_to_sql_server(training_data, 'Training')

#%%
insert_data_to_sql_server(order_header_data, 'Order_Header')
insert_data_to_sql_server(order_details_data, 'Order_Details')
insert_data_to_sql_server(inventory_levels_data, 'Inventory_Levels')
insert_data_to_sql_server(product_forecast_data, 'Product_Forecast')
insert_data_to_sql_server(retailer_contact_data, 'Retailer_Contact')
insert_data_to_sql_server(sales_demographic_data, 'Sales_Demographic')
insert_data_to_sql_server(returned_item_data, 'Returned_Item')

#%%
go_sales_con.close()
go_staff_con.close()
go_crm_con.close()
get_sql_server_connection().close()

