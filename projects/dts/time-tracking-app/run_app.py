"""
Time Tracking Application Launcher
Run this file to start the application
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run
from gui_main import main

if __name__ == "__main__":
    print("=" * 60)
    print("Data Tune Solutions - Time Tracking Application")
    print("=" * 60)
    print("\nStarting application...")
    print("\nTip: Navigate between Timesheet and Clients using the top buttons")
    print("=" * 60)
    print()
    
    try:
        main()
    except Exception as e:
        print(f"\nError starting application: {e}")
        print("\nMake sure:")
        print("1. Virtual environment is activated")
        print("2. Dependencies are installed (pip install -r requirements.txt)")
        print("3. .env file is configured with database connection")
        print("4. SQL Server is running and database exists")
        input("\nPress Enter to exit...")

