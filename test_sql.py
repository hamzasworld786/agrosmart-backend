import pyodbc

conn_str = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:agrosmart-sql-server.database.windows.net,1433;Database=agrosmart-db;Uid=agrosmartadmin;Pwd=AgroSmart@2024;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

try:
    conn = pyodbc.connect(conn_str)
    print("Connected to Azure SQL successfully")
    conn.close()
except Exception as e:
    print(f"Connection failed: {e}")
