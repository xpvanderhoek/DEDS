import sqlite3
import pandas as pd
import os

# Pad naar de database
db_path = "../../DEDS Portfolio/week1/Data/go_sales_train.sqlite"  # Pas dit aan voor andere databases
output_dir = "../../DEDS Portfolio/week1/Data/Exports"

# Zorg dat de exportmap bestaat
os.makedirs(output_dir, exist_ok=True)

# Verbind met de database
conn = sqlite3.connect(db_path)

# Haal alle tabellen op
tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)

# Loop door alle tabellen en sla ze op als Excel
for table_name in tables["name"]:
    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    output_file = os.path.join(output_dir, f"{table_name}.xlsx")
    df.to_excel(output_file, index=False)
    print(f"Data uit '{table_name}' opgeslagen als {output_file}")

# Sluit de verbinding
conn.close()
print("Exporteren voltooid!")