"""
Time Tracking App - SQL Server Connection Test
Tests database connectivity and verifies schema exists
"""

import os
import pyodbc
from dotenv import load_dotenv

def test_connection():
    """Test SQL Server connection and verify database setup"""
    
    # Load environment variables
    load_dotenv()
    
    server = os.getenv('SQL_SERVER', 'localhost')
    database = os.getenv('SQL_DATABASE', 'DataTuneTimeTracking')
    username = os.getenv('SQL_USERNAME', '')
    password = os.getenv('SQL_PASSWORD', '')
    trusted_connection = os.getenv('SQL_TRUSTED_CONNECTION', 'yes').lower() == 'yes'
    
    print("=" * 60)
    print("Time Tracking App - Connection Test")
    print("=" * 60)
    print(f"\nServer: {server}")
    print(f"Database: {database}")
    print(f"Authentication: {'Windows' if trusted_connection else 'SQL Server'}")
    print()
    
    try:
        # Build connection string
        if trusted_connection:
            conn_str = (
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={server};"
                f"DATABASE={database};"
                f"Trusted_Connection=yes;"
            )
        else:
            conn_str = (
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={server};"
                f"DATABASE={database};"
                f"UID={username};"
                f"PWD={password};"
            )
        
        # Attempt connection
        print("Connecting to SQL Server...")
        conn = pyodbc.connect(conn_str, timeout=10)
        cursor = conn.cursor()
        
        print("✅ Connection successful!\n")
        
        # Verify database schema
        print("Verifying database schema...")
        
        # Check tables
        cursor.execute("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_NAME
        """)
        tables = [row[0] for row in cursor.fetchall()]
        
        print(f"\nTables found: {len(tables)}")
        for table in tables:
            print(f"  - {table}")
        
        # Check if core tables exist
        required_tables = ['Clients', 'TimeEntries', 'Invoices']
        missing_tables = [t for t in required_tables if t not in tables]
        
        if missing_tables:
            print(f"\n⚠️  Warning: Missing tables: {', '.join(missing_tables)}")
            print("   Run database/schema.sql to create tables")
        else:
            print("\n✅ All core tables exist!")
        
        # Check for data
        print("\nData Summary:")
        
        if 'Clients' in tables:
            cursor.execute("SELECT COUNT(*) FROM Clients")
            client_count = cursor.fetchone()[0]
            print(f"  - Clients: {client_count}")
        
        if 'TimeEntries' in tables:
            cursor.execute("SELECT COUNT(*) FROM TimeEntries")
            entry_count = cursor.fetchone()[0]
            print(f"  - Time Entries: {entry_count}")
        
        if 'Invoices' in tables:
            cursor.execute("SELECT COUNT(*) FROM Invoices")
            invoice_count = cursor.fetchone()[0]
            print(f"  - Invoices: {invoice_count}")
        
        # Clean up
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print("✅ Connection test completed successfully!")
        print("=" * 60)
        
        return True
        
    except pyodbc.Error as e:
        print(f"\n❌ Connection failed!")
        print(f"\nError: {e}")
        print("\nTroubleshooting:")
        print("  1. Verify SQL Server is running")
        print("  2. Check server name in .env file")
        print("  3. Verify database exists (run CREATE DATABASE if needed)")
        print("  4. Check authentication credentials")
        print("  5. Ensure ODBC Driver 17 for SQL Server is installed")
        print("     Download: https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server")
        
        return False
    
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    test_connection()

