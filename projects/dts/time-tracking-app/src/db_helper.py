"""
Time Tracking App - Database Helper Module
Provides reusable functions for database operations
"""

import os
import pyodbc
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

class DatabaseHelper:
    """Helper class for SQL Server database operations"""
    
    def __init__(self):
        """Initialize database connection"""
        self.server = os.getenv('SQL_SERVER', 'localhost')
        self.database = os.getenv('SQL_DATABASE', 'DataTuneTimeTracking')
        self.username = os.getenv('SQL_USERNAME', '')
        self.password = os.getenv('SQL_PASSWORD', '')
        self.trusted_connection = os.getenv('SQL_TRUSTED_CONNECTION', 'yes').lower() == 'yes'
        self.conn = None
        
    def get_connection(self):
        """Get database connection"""
        if self.conn is None or self.conn.closed:
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
            self.conn = pyodbc.connect(conn_str)
        return self.conn
    
    def close_connection(self):
        """Close database connection"""
        if self.conn and not self.conn.closed:
            self.conn.close()
            self.conn = None
    
    # ===== CLIENT OPERATIONS =====
    
    def get_all_clients(self, active_only=True):
        """Get all clients
        
        Args:
            active_only (bool): If True, return only active clients
            
        Returns:
            list: List of client dictionaries
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT ClientID, ClientName, DefaultRate, PaymentTerms, Active, 
                   ContactName, ContactEmail, ContactPhone, BillingAddress,
                   CreatedDate, ModifiedDate
            FROM Clients
        """
        if active_only:
            query += " WHERE Active = 1"
        query += " ORDER BY ClientName"
        
        cursor.execute(query)
        
        clients = []
        for row in cursor.fetchall():
            clients.append({
                'ClientID': row.ClientID,
                'ClientName': row.ClientName,
                'DefaultRate': float(row.DefaultRate),
                'PaymentTerms': row.PaymentTerms,
                'Active': bool(row.Active),
                'ContactName': row.ContactName or '',
                'ContactEmail': row.ContactEmail or '',
                'ContactPhone': row.ContactPhone or '',
                'BillingAddress': row.BillingAddress or '',
                'CreatedDate': row.CreatedDate,
                'ModifiedDate': row.ModifiedDate
            })
        
        cursor.close()
        return clients
    
    def get_client_by_id(self, client_id):
        """Get a specific client by ID
        
        Args:
            client_id (int): Client ID
            
        Returns:
            dict: Client dictionary or None
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT ClientID, ClientName, DefaultRate, PaymentTerms, Active,
                   ContactName, ContactEmail, ContactPhone, BillingAddress,
                   CreatedDate, ModifiedDate
            FROM Clients
            WHERE ClientID = ?
        """, (client_id,))
        
        row = cursor.fetchone()
        cursor.close()
        
        if row:
            return {
                'ClientID': row.ClientID,
                'ClientName': row.ClientName,
                'DefaultRate': float(row.DefaultRate),
                'PaymentTerms': row.PaymentTerms,
                'Active': bool(row.Active),
                'ContactName': row.ContactName or '',
                'ContactEmail': row.ContactEmail or '',
                'ContactPhone': row.ContactPhone or '',
                'BillingAddress': row.BillingAddress or '',
                'CreatedDate': row.CreatedDate,
                'ModifiedDate': row.ModifiedDate
            }
        return None
    
    def add_client(self, client_name, default_rate, payment_terms=30, active=True,
                  contact_name='', contact_email='', contact_phone='', billing_address=''):
        """Add a new client
        
        Args:
            client_name (str): Client name
            default_rate (float): Default hourly rate
            payment_terms (int): Payment terms in days
            active (bool): Active status
            contact_name (str): Contact person name
            contact_email (str): Contact email
            contact_phone (str): Contact phone
            billing_address (str): Billing address
            
        Returns:
            int: New client ID
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO Clients (ClientName, DefaultRate, PaymentTerms, Active,
                               ContactName, ContactEmail, ContactPhone, BillingAddress)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (client_name, default_rate, payment_terms, 1 if active else 0,
              contact_name or None, contact_email or None, 
              contact_phone or None, billing_address or None))
        
        conn.commit()
        
        # Get the new client ID
        cursor.execute("SELECT @@IDENTITY AS NewID")
        new_id = cursor.fetchone()[0]
        
        cursor.close()
        return int(new_id)
    
    def update_client(self, client_id, client_name=None, default_rate=None, 
                      payment_terms=None, active=None, contact_name=None,
                      contact_email=None, contact_phone=None, billing_address=None):
        """Update an existing client
        
        Args:
            client_id (int): Client ID to update
            client_name (str, optional): New client name
            default_rate (float, optional): New default rate
            payment_terms (int, optional): New payment terms
            active (bool, optional): New active status
            contact_name (str, optional): New contact name
            contact_email (str, optional): New contact email
            contact_phone (str, optional): New contact phone
            billing_address (str, optional): New billing address
            
        Returns:
            bool: True if successful
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        updates = []
        params = []
        
        if client_name is not None:
            updates.append("ClientName = ?")
            params.append(client_name)
        
        if default_rate is not None:
            updates.append("DefaultRate = ?")
            params.append(default_rate)
        
        if payment_terms is not None:
            updates.append("PaymentTerms = ?")
            params.append(payment_terms)
        
        if active is not None:
            updates.append("Active = ?")
            params.append(1 if active else 0)
        
        if contact_name is not None:
            updates.append("ContactName = ?")
            params.append(contact_name or None)
        
        if contact_email is not None:
            updates.append("ContactEmail = ?")
            params.append(contact_email or None)
        
        if contact_phone is not None:
            updates.append("ContactPhone = ?")
            params.append(contact_phone or None)
        
        if billing_address is not None:
            updates.append("BillingAddress = ?")
            params.append(billing_address or None)
        
        if not updates:
            return False
        
        updates.append("ModifiedDate = GETDATE()")
        params.append(client_id)
        
        query = f"UPDATE Clients SET {', '.join(updates)} WHERE ClientID = ?"
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        
        return True
    
    def delete_client(self, client_id):
        """Soft delete a client (mark as inactive)
        
        Args:
            client_id (int): Client ID to delete
            
        Returns:
            bool: True if successful
        """
        return self.update_client(client_id, active=False)
    
    # ===== TIME ENTRY OPERATIONS =====
    
    def get_weekly_timesheet(self, week_start_date):
        """Get weekly timesheet data
        
        Args:
            week_start_date (date): Monday of the week
            
        Returns:
            dict: Nested dict {client_id: {day: {hours, rate, entry_id, notes}}}
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                c.ClientID,
                c.ClientName,
                c.DefaultRate,
                te.DayOfWeek,
                ISNULL(te.HoursWorked, 0) AS HoursWorked,
                ISNULL(te.RateUsed, c.DefaultRate) AS RateUsed,
                te.Notes,
                te.EntryID
            FROM Clients c
            CROSS JOIN (SELECT 1 AS DayOfWeek UNION SELECT 2 UNION SELECT 3 
                       UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7) AS days
            LEFT JOIN TimeEntries te 
                ON c.ClientID = te.ClientID 
                AND te.WeekStartDate = ?
                AND te.DayOfWeek = days.DayOfWeek
            WHERE c.Active = 1
            ORDER BY c.ClientName, days.DayOfWeek
        """, (week_start_date,))
        
        timesheet = {}
        
        for row in cursor.fetchall():
            client_id = row.ClientID
            day = row.DayOfWeek
            
            if client_id not in timesheet:
                timesheet[client_id] = {
                    'ClientName': row.ClientName,
                    'DefaultRate': float(row.DefaultRate),
                    'days': {}
                }
            
            timesheet[client_id]['days'][day] = {
                'hours': float(row.HoursWorked) if row.HoursWorked else 0.0,
                'rate': float(row.RateUsed) if row.RateUsed else float(row.DefaultRate),
                'entry_id': row.EntryID,
                'notes': row.Notes or ''
            }
        
        cursor.close()
        return timesheet
    
    def save_time_entry(self, client_id, week_start_date, day_of_week, 
                       hours_worked, rate_used, notes=''):
        """Save or update a time entry
        
        Args:
            client_id (int): Client ID
            week_start_date (date): Monday of the week
            day_of_week (int): 1=Mon, 7=Sun
            hours_worked (float): Hours worked
            rate_used (float): Rate to use
            notes (str): Optional notes
            
        Returns:
            int: Entry ID
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Check if entry exists
        cursor.execute("""
            SELECT EntryID FROM TimeEntries
            WHERE ClientID = ? AND WeekStartDate = ? AND DayOfWeek = ?
        """, (client_id, week_start_date, day_of_week))
        
        existing = cursor.fetchone()
        
        if existing:
            # Update existing entry
            if hours_worked > 0:
                cursor.execute("""
                    UPDATE TimeEntries
                    SET HoursWorked = ?, RateUsed = ?, Notes = ?
                    WHERE EntryID = ?
                """, (hours_worked, rate_used, notes, existing.EntryID))
                entry_id = existing.EntryID
            else:
                # Delete if hours is 0
                cursor.execute("DELETE FROM TimeEntries WHERE EntryID = ?", 
                             (existing.EntryID,))
                entry_id = None
        else:
            # Insert new entry (only if hours > 0)
            if hours_worked > 0:
                cursor.execute("""
                    INSERT INTO TimeEntries 
                    (ClientID, WeekStartDate, DayOfWeek, HoursWorked, RateUsed, Notes)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (client_id, week_start_date, day_of_week, hours_worked, 
                      rate_used, notes))
                
                cursor.execute("SELECT @@IDENTITY AS NewID")
                entry_id = int(cursor.fetchone()[0])
            else:
                entry_id = None
        
        conn.commit()
        cursor.close()
        
        return entry_id
    
    def delete_time_entry(self, entry_id):
        """Delete a time entry
        
        Args:
            entry_id (int): Entry ID to delete
            
        Returns:
            bool: True if successful
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM TimeEntries WHERE EntryID = ?", (entry_id,))
        conn.commit()
        cursor.close()
        
        return True
    
    # ===== UTILITY FUNCTIONS =====
    
    def get_week_start(self, date=None):
        """Get the Monday of the week for a given date
        
        Args:
            date (date, optional): Date to get week start for. Defaults to today.
            
        Returns:
            date: Monday of the week
        """
        if date is None:
            date = datetime.now().date()
        
        # Calculate days since Monday (0=Monday, 6=Sunday)
        days_since_monday = date.weekday()
        week_start = date - timedelta(days=days_since_monday)
        
        return week_start
    
    def get_week_dates(self, week_start):
        """Get all dates for a week (Mon-Sun)
        
        Args:
            week_start (date): Monday of the week
            
        Returns:
            list: List of 7 dates (Mon-Sun)
        """
        return [week_start + timedelta(days=i) for i in range(7)]

# Singleton instance
db = DatabaseHelper()

