"""
Verify database schema
"""

import sys
sys.path.insert(0, '.')
from db_helper import db

print("=" * 60)
print("Database Schema Verification")
print("=" * 60)

try:
    conn = db.get_connection()
    cursor = conn.cursor()
    
    # Get columns in Clients table
    cursor.execute("""
        SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, CHARACTER_MAXIMUM_LENGTH
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME = 'Clients'
        ORDER BY ORDINAL_POSITION
    """)
    
    print("\nColumns in Clients table:")
    print("-" * 60)
    
    for row in cursor.fetchall():
        col_name = row[0]
        data_type = row[1]
        nullable = row[2]
        max_length = row[3] if row[3] else ''
        
        print(f"  {col_name:<25} {data_type:<15} {nullable:<10} {max_length}")
    
    # Check if migration tracking table exists
    cursor.execute("""
        SELECT COUNT(*) 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_NAME = 'AppliedMigrations'
    """)
    
    has_migrations = cursor.fetchone()[0] > 0
    
    if has_migrations:
        print("\n" + "=" * 60)
        print("Applied Migrations:")
        print("-" * 60)
        cursor.execute("SELECT MigrationName, AppliedDate FROM AppliedMigrations ORDER BY AppliedDate")
        
        for row in cursor.fetchall():
            print(f"  {row[0]:<40} {row[1]}")
    else:
        print("\n[WARNING] AppliedMigrations table does not exist")
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 60)
    print("[SUCCESS] Schema verification complete")
    print("=" * 60)
    
except Exception as e:
    print(f"\n[ERROR] {e}")

