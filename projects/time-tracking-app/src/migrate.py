"""
Database Migration Runner
Automatically applies SQL migrations to the database
"""

import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()

class MigrationRunner:
    """Handles database migrations"""
    
    def __init__(self):
        self.server = os.getenv('SQL_SERVER', 'localhost')
        self.database = os.getenv('SQL_DATABASE', 'DataTuneTimeTracking')
        self.username = os.getenv('SQL_USERNAME', '')
        self.password = os.getenv('SQL_PASSWORD', '')
        self.trusted_connection = os.getenv('SQL_TRUSTED_CONNECTION', 'yes').lower() == 'yes'
        
    def get_connection(self):
        """Get database connection"""
        if self.trusted_connection:
            conn_str = (
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={self.server};"
                f"DATABASE={self.database};"
                f"Trusted_Connection=yes;"
            )
        else:
            conn_str = (
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={self.server};"
                f"DATABASE={self.database};"
                f"UID={self.username};"
                f"PWD={self.password};"
            )
        return pyodbc.connect(conn_str)
    
    def create_migrations_table(self):
        """Create table to track applied migrations"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'AppliedMigrations')
            BEGIN
                CREATE TABLE AppliedMigrations (
                    MigrationID INT IDENTITY(1,1) PRIMARY KEY,
                    MigrationName NVARCHAR(255) NOT NULL UNIQUE,
                    AppliedDate DATETIME NOT NULL DEFAULT GETDATE()
                );
                PRINT 'Created AppliedMigrations table';
            END
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
    
    def get_applied_migrations(self):
        """Get list of already applied migrations"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT MigrationName FROM AppliedMigrations ORDER BY MigrationName")
        applied = [row[0] for row in cursor.fetchall()]
        
        cursor.close()
        conn.close()
        
        return applied
    
    def mark_migration_applied(self, migration_name):
        """Mark a migration as applied"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO AppliedMigrations (MigrationName)
            VALUES (?)
        """, (migration_name,))
        
        conn.commit()
        cursor.close()
        conn.close()
    
    def run_migration(self, migration_file):
        """Run a single migration file"""
        print(f"\nRunning migration: {migration_file}")
        
        # Read migration SQL
        migrations_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            'database', 'migrations'
        )
        file_path = os.path.join(migrations_dir, migration_file)
        
        with open(file_path, 'r') as f:
            sql_script = f.read()
        
        # Split by GO statements
        batches = [batch.strip() for batch in sql_script.split('GO') if batch.strip()]
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            for i, batch in enumerate(batches, 1):
                if batch and not batch.startswith('--'):
                    print(f"  Executing batch {i}/{len(batches)}...")
                    cursor.execute(batch)
                    conn.commit()
            
            print(f"[SUCCESS] Migration {migration_file} completed successfully")
            
            # Mark as applied
            self.mark_migration_applied(migration_file)
            
            cursor.close()
            conn.close()
            return True
            
        except Exception as e:
            print(f"[ERROR] Error in migration {migration_file}: {e}")
            conn.rollback()
            cursor.close()
            conn.close()
            return False
    
    def run_all_migrations(self):
        """Run all pending migrations"""
        print("=" * 60)
        print("Database Migration Runner")
        print("=" * 60)
        
        # Create migrations table if needed
        self.create_migrations_table()
        
        # Get applied migrations
        applied = self.get_applied_migrations()
        print(f"\nAlready applied: {len(applied)} migration(s)")
        
        # Find migration files
        migrations_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            'database', 'migrations'
        )
        
        if not os.path.exists(migrations_dir):
            print(f"\n[WARNING] Migrations directory not found: {migrations_dir}")
            return
        
        migration_files = sorted([
            f for f in os.listdir(migrations_dir) 
            if f.endswith('.sql')
        ])
        
        if not migration_files:
            print("\nNo migration files found")
            return
        
        # Run pending migrations
        pending = [f for f in migration_files if f not in applied]
        
        if not pending:
            print("\n[OK] All migrations up to date!")
            return
        
        print(f"\nPending migrations: {len(pending)}")
        
        for migration_file in pending:
            success = self.run_migration(migration_file)
            if not success:
                print(f"\n[ERROR] Migration failed. Stopping.")
                return
        
        print("\n" + "=" * 60)
        print("[SUCCESS] All migrations completed successfully!")
        print("=" * 60)


def main():
    """Run migrations"""
    runner = MigrationRunner()
    runner.run_all_migrations()


if __name__ == "__main__":
    main()

