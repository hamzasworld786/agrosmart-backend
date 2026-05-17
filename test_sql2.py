import pyodbc

# Print all available drivers
print("Available ODBC Drivers:")
for driver in pyodbc.drivers():
    print(f"  - {driver}")

# Try to connect with exact driver name
conn_str = "Driver=ODBC Driver 18 for SQL Server;Server=tcp:agrosmart-sql-server.database.windows.net,1433;Database=agrosmart-db;Uid=agrosmartadmin;Pwd=AgroSmart@2024;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

try:
    conn = pyodbc.connect(conn_str)
    print("Connected to Azure SQL successfully")
    conn.close()
except Exception as e:
    print(f"Connection failed: {e}")
