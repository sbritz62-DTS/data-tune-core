"""
Time Tracking App - Database Helper Module (IMPROVED)
Provides reusable functions for database operations with error handling and logging
"""

import os
import pyodbc
import logging
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


class DatabaseError(Exception):
    """Custom exception for database operations"""
    pass


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


class DatabaseHelper:
    """Helper class for SQL Server database operations with improved error handling"""
    
    def __init__(self):
        """Initialize database connection"""
        self.server = os.getenv('SQL_SERVER', 'localhost')
        self.database = os.getenv('SQL_DATABASE', 'DataTuneTimeTracking')
        self.username = os.getenv('SQL_USERNAME', '')
        self.password = os.getenv('SQL_PASSWORD', '')
        self.trusted_connection = os.getenv('SQL_TRUSTED_CONNECTION', 'yes').lower() == 'yes'
        self.conn = None
        logger.info(f"Database helper initialized for {self.server}/{self.database}")
        
    def get_connection(self):
        """Get database connection with health check"""
        try:
            if self.conn is None or self.conn.closed:
                logger.info("Creating new database connection")
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
                self.conn = pyodbc.connect(conn_str, timeout=10)
            
            # Quick health check
            cursor = self.conn.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            
            return self.conn
            
        except pyodbc.Error as e:
            logger.error(f"Database connection failed: {e}", exc_info=True)
            raise DatabaseError(f"Failed to connect to database: {e}") from e
    
    def close_connection(self):
        """Close database connection"""
        try:
            if self.conn and not self.conn.closed:
                self.conn.close()
                logger.info("Database connection closed")
                self.conn = None
        except Exception as e:
            logger.warning(f"Error closing connection: {e}")
    
    # ===== VALIDATION HELPERS =====
    
    @staticmethod
    def validate_rate(rate):
        """Validate hourly rate"""
        if rate < 0:
            raise ValidationError("Rate must be positive")
        if rate > 999999.99:
            raise ValidationError("Rate seems unreasonably high")
    
    @staticmethod
    def validate_payment_terms(terms):
        """Validate payment terms"""
        if terms < 0:
            raise ValidationError("Payment terms must be positive")
        if terms > 365:
            raise ValidationError("Payment terms should not exceed 365 days")
    
    @staticmethod
    def validate_hours(hours):
        """Validate hours worked"""
        if hours < 0:
            raise ValidationError("Hours cannot be negative")
        if hours > 24:
            raise ValidationError("Hours cannot exceed 24 per day")
    
    @staticmethod
    def validate_client_name(name):
        """Validate client name"""
        if not name or len(name.strip()) == 0:
            raise ValidationError("Client name is required")
        if len(name) > 200:
            raise ValidationError("Client name too long (max 200 characters)")
    
    # ===== CLIENT OPERATIONS =====
    
    def get_all_clients(self, active_only=True):
        """Get all clients
        
        Args:
            active_only (bool): If True, return only active clients
            
        Returns:
            list: List of client dictionaries
            
        Raises:
            DatabaseError: If query fails
        """
        try:
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
            
            logger.info(f"Fetching {'active' if active_only else 'all'} clients")
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
            
            logger.info(f"Retrieved {len(clients)} clients")
            cursor.close()
            return clients
            
        except pyodbc.Error as e:
            logger.error(f"Failed to fetch clients: {e}", exc_info=True)
            raise DatabaseError(f"Failed to fetch clients: {e}") from e
    
    def get_client_by_id(self, client_id):
        """Get a specific client by ID
        
        Args:
            client_id (int): Client ID
            
        Returns:
            dict: Client dictionary or None
            
        Raises:
            DatabaseError: If query fails
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            logger.info(f"Fetching client {client_id}")
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
            
        except pyodbc.Error as e:
            logger.error(f"Failed to fetch client {client_id}: {e}", exc_info=True)
            raise DatabaseError(f"Failed to fetch client: {e}") from e
    
    def add_client(self, client_name, default_rate, payment_terms=30, active=True,
                  contact_name='', contact_email='', contact_phone='', billing_address=''):
        """Add a new client with validation
        
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
            
        Raises:
            ValidationError: If validation fails
            DatabaseError: If insert fails
        """
        try:
            # Validate inputs
            self.validate_client_name(client_name)
            self.validate_rate(default_rate)
            self.validate_payment_terms(payment_terms)
            
            logger.info(f"Adding new client: {client_name}")
            
            conn = self.get_connection()
            cursor = conn.cursor()
            
            try:
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
                new_id = int(cursor.fetchone()[0])
                
                logger.info(f"Client added successfully with ID: {new_id}")
                cursor.close()
                return new_id
                
            except pyodbc.Error as e:
                conn.rollback()
                logger.error(f"Failed to add client: {e}", exc_info=True)
                raise DatabaseError(f"Failed to add client: {e}") from e
            
        except ValidationError as e:
            logger.warning(f"Client validation failed: {e}")
            raise
    
    def update_client(self, client_id, client_name=None, default_rate=None, 
                      payment_terms=None, active=None, contact_name=None,
                      contact_email=None, contact_phone=None, billing_address=None):
        """Update an existing client with validation
        
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
            
        Raises:
            ValidationError: If validation fails
            DatabaseError: If update fails
        """
        try:
            # Validate inputs
            if client_name is not None:
                self.validate_client_name(client_name)
            if default_rate is not None:
                self.validate_rate(default_rate)
            if payment_terms is not None:
                self.validate_payment_terms(payment_terms)
            
            logger.info(f"Updating client {client_id}")
            
            conn = self.get_connection()
            cursor = conn.cursor()
            
            try:
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
                    logger.info(f"No updates provided for client {client_id}")
                    return False
                
                updates.append("ModifiedDate = GETDATE()")
                params.append(client_id)
                
                query = f"UPDATE Clients SET {', '.join(updates)} WHERE ClientID = ?"
                cursor.execute(query, params)
                conn.commit()
                
                logger.info(f"Client {client_id} updated successfully")
                cursor.close()
                return True
                
            except pyodbc.Error as e:
                conn.rollback()
                logger.error(f"Failed to update client {client_id}: {e}", exc_info=True)
                raise DatabaseError(f"Failed to update client: {e}") from e
        
        except ValidationError as e:
            logger.warning(f"Client validation failed: {e}")
            raise
    
    def delete_client(self, client_id):
        """Soft delete a client (mark as inactive)
        
        Args:
            client_id (int): Client ID to delete
            
        Returns:
            bool: True if successful
            
        Raises:
            DatabaseError: If update fails
        """
        logger.info(f"Deactivating client {client_id}")
        return self.update_client(client_id, active=False)
    
    # ===== TIME ENTRY OPERATIONS =====
    
    def get_weekly_timesheet(self, week_start_date):
        """Get weekly timesheet data
        
        Args:
            week_start_date (date): Monday of the week
            
        Returns:
            dict: Nested dict {client_id: {day: {hours, rate, entry_id, notes}}}
            
        Raises:
            DatabaseError: If query fails
        """
        try:
            logger.info(f"Fetching timesheet for week starting {week_start_date}")
            
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
            
            logger.info(f"Retrieved timesheet with {len(timesheet)} clients")
            cursor.close()
            return timesheet
            
        except pyodbc.Error as e:
            logger.error(f"Failed to fetch timesheet: {e}", exc_info=True)
            raise DatabaseError(f"Failed to fetch timesheet: {e}") from e
    
    def save_time_entry(self, client_id, week_start_date, day_of_week, 
                       hours_worked, rate_used, notes=''):
        """Save or update a time entry with validation
        
        Args:
            client_id (int): Client ID
            week_start_date (date): Monday of the week
            day_of_week (int): 1=Mon, 7=Sun
            hours_worked (float): Hours worked
            rate_used (float): Rate to use
            notes (str): Optional notes
            
        Returns:
            int: Entry ID or None if deleted
            
        Raises:
            ValidationError: If validation fails
            DatabaseError: If operation fails
        """
        try:
            # Validate inputs
            self.validate_hours(hours_worked)
            self.validate_rate(rate_used)
            
            if day_of_week < 1 or day_of_week > 7:
                raise ValidationError("Day of week must be 1-7")
            
            logger.info(f"Saving time entry: client={client_id}, week={week_start_date}, "
                       f"day={day_of_week}, hours={hours_worked}")
            
            conn = self.get_connection()
            cursor = conn.cursor()
            
            try:
                # Check if entry exists
                cursor.execute("""
                    SELECT EntryID FROM TimeEntries
                    WHERE ClientID = ? AND WeekStartDate = ? AND DayOfWeek = ?
                """, (client_id, week_start_date, day_of_week))
                
                existing = cursor.fetchone()
                
                if existing:
                    # Update or delete existing entry
                    if hours_worked > 0:
                        cursor.execute("""
                            UPDATE TimeEntries
                            SET HoursWorked = ?, RateUsed = ?, Notes = ?
                            WHERE EntryID = ?
                        """, (hours_worked, rate_used, notes, existing.EntryID))
                        entry_id = existing.EntryID
                        logger.info(f"Updated entry {entry_id}")
                    else:
                        # Delete if hours is 0
                        cursor.execute("DELETE FROM TimeEntries WHERE EntryID = ?", 
                                     (existing.EntryID,))
                        entry_id = None
                        logger.info(f"Deleted entry {existing.EntryID}")
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
                        logger.info(f"Inserted new entry {entry_id}")
                    else:
                        entry_id = None
                
                conn.commit()
                cursor.close()
                return entry_id
                
            except pyodbc.Error as e:
                conn.rollback()
                logger.error(f"Failed to save time entry: {e}", exc_info=True)
                raise DatabaseError(f"Failed to save time entry: {e}") from e
        
        except ValidationError as e:
            logger.warning(f"Time entry validation failed: {e}")
            raise
    
    def delete_time_entry(self, entry_id):
        """Delete a time entry
        
        Args:
            entry_id (int): Entry ID to delete
            
        Returns:
            bool: True if successful
            
        Raises:
            DatabaseError: If operation fails
        """
        try:
            logger.info(f"Deleting entry {entry_id}")
            
            conn = self.get_connection()
            cursor = conn.cursor()
            
            try:
                cursor.execute("DELETE FROM TimeEntries WHERE EntryID = ?", (entry_id,))
                conn.commit()
                logger.info(f"Entry {entry_id} deleted successfully")
                cursor.close()
                return True
                
            except pyodbc.Error as e:
                conn.rollback()
                logger.error(f"Failed to delete entry {entry_id}: {e}", exc_info=True)
                raise DatabaseError(f"Failed to delete entry: {e}") from e
        
        except Exception as e:
            logger.error(f"Unexpected error deleting entry: {e}", exc_info=True)
            raise
    
    # ===== UTILITY FUNCTIONS =====
    
    @staticmethod
    def get_week_start(date=None):
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
    
    @staticmethod
    def get_week_dates(week_start):
        """Get all dates for a week (Mon-Sun)
        
        Args:
            week_start (date): Monday of the week
            
        Returns:
            list: List of 7 dates (Mon-Sun)
        """
        return [week_start + timedelta(days=i) for i in range(7)]


# Singleton instance
db = DatabaseHelper()
