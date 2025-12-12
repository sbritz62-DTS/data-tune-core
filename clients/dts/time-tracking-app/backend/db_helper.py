"""
Time Tracking App - Database Helper Module
Provides reusable functions for database operations
Includes: Clients, Departments, Time Entries, and Invoices

IMPORTANT: All SQL queries use table aliases (a, c, t, i, etc.) and prefix all columns
with the table alias to prevent ambiguous column name errors.
"""

import os
import pyodbc
from dotenv import load_dotenv
from datetime import datetime, timedelta
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# ===== CUSTOM EXCEPTIONS =====

class DatabaseError(Exception):
    """Database operation error"""
    pass

class ValidationError(Exception):
    """Validation error"""
    pass

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
        """Get all clients"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT c.ClientID, c.ClientName, c.DefaultRate, c.PaymentTerms, c.Active, 
                   c.ContactName, c.ContactEmail, c.ContactPhone, c.BillingAddress,
                   c.CreatedDate, c.ModifiedDate
            FROM Clients AS c
        """
        if active_only:
            query += " WHERE c.Active = 1"
        query += " ORDER BY c.ClientName"
        
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
        """Get a specific client by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT c.ClientID, c.ClientName, c.DefaultRate, c.PaymentTerms, c.Active,
                   c.ContactName, c.ContactEmail, c.ContactPhone, c.BillingAddress,
                   c.CreatedDate, c.ModifiedDate
            FROM Clients AS c
            WHERE c.ClientID = ?
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
        """Add a new client"""
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
        
        cursor.execute("SELECT @@IDENTITY AS NewID")
        new_id = cursor.fetchone()[0]
        
        cursor.close()
        return int(new_id)
    
    def update_client(self, client_id, client_name=None, default_rate=None, 
                      payment_terms=None, active=None, contact_name=None,
                      contact_email=None, contact_phone=None, billing_address=None):
        """Update an existing client"""
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
        """Soft delete a client (mark as inactive)"""
        return self.update_client(client_id, active=False)
    
    # ===== DEPARTMENT OPERATIONS =====
    
    def get_client_departments(self, client_id):
        """Get all departments for a client"""
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT cd.ClientDepartmentID, cd.ClientID, cd.DepartmentName, 
                       cd.BillingRate, cd.IsActive, cd.CreatedDate, cd.ModifiedDate
                FROM ClientDepartments AS cd
                WHERE cd.ClientID = ? AND cd.IsActive = 1
                ORDER BY cd.DepartmentName
            """, (client_id,))
            
            departments = []
            for row in cursor.fetchall():
                departments.append({
                    'ClientDepartmentID': row.ClientDepartmentID,
                    'ClientID': row.ClientID,
                    'DepartmentName': row.DepartmentName,
                    'BillingRate': float(row.BillingRate) if row.BillingRate else None,
                    'IsActive': bool(row.IsActive),
                    'CreatedDate': row.CreatedDate,
                    'ModifiedDate': row.ModifiedDate
                })
            
            logger.info(f"Retrieved {len(departments)} departments for client {client_id}")
            return departments
            
        except Exception as e:
            logger.error(f"Error getting client departments: {e}")
            raise DatabaseError(f"Failed to get client departments: {str(e)}")
        finally:
            if cursor:
                cursor.close()
    
    def add_client_department(self, client_id, department_name, billing_rate=None):
        """Add a new department for a client"""
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO ClientDepartments (ClientID, DepartmentName, BillingRate, IsActive)
                VALUES (?, ?, ?, 1)
            """, (client_id, department_name, billing_rate))
            
            conn.commit()
            
            cursor.execute("SELECT @@IDENTITY AS NewID")
            dept_id = cursor.fetchone()[0]
            
            logger.info(f"Created department '{department_name}' for client {client_id}")
            return int(dept_id)
            
        except Exception as e:
            logger.error(f"Error adding client department: {e}")
            raise DatabaseError(f"Failed to add department: {str(e)}")
        finally:
            if cursor:
                cursor.close()
    
    def update_client_department(self, dept_id, department_name=None, billing_rate=None, is_active=None):
        """Update a department"""
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            updates = []
            params = []
            
            if department_name is not None:
                updates.append("DepartmentName = ?")
                params.append(department_name)
            
            if billing_rate is not None:
                updates.append("BillingRate = ?")
                params.append(billing_rate)
            
            if is_active is not None:
                updates.append("IsActive = ?")
                params.append(1 if is_active else 0)
            
            if not updates:
                return False
            
            updates.append("ModifiedDate = GETDATE()")
            params.append(dept_id)
            
            query = f"UPDATE ClientDepartments SET {', '.join(updates)} WHERE ClientDepartmentID = ?"
            cursor.execute(query, params)
            conn.commit()
            
            logger.info(f"Updated department {dept_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating department: {e}")
            raise DatabaseError(f"Failed to update department: {str(e)}")
        finally:
            if cursor:
                cursor.close()
    
    def delete_client_department(self, dept_id):
        """Soft delete a department (mark as inactive)"""
        return self.update_client_department(dept_id, is_active=False)
    
    # ===== TIME ENTRY OPERATIONS =====
    
    def get_weekly_timesheet(self, week_start_date):
        """Get weekly timesheet data"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                c.ClientID,
                c.ClientName,
                c.DefaultRate,
                d.DayOfWeek,
                ISNULL(t.HoursWorked, 0) AS HoursWorked,
                ISNULL(t.RateUsed, c.DefaultRate) AS RateUsed,
                t.Notes,
                t.EntryID
            FROM Clients AS c
            CROSS JOIN (SELECT 1 AS DayOfWeek UNION SELECT 2 UNION SELECT 3 
                       UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7) AS d
            LEFT JOIN TimeEntries AS t 
                ON c.ClientID = t.ClientID 
                AND t.WeekStartDate = ?
                AND t.DayOfWeek = d.DayOfWeek
            WHERE c.Active = 1
            ORDER BY c.ClientName, d.DayOfWeek
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
    
    def get_day_entries(self, client_id, week_start_date, day_of_week):
        """Get all time entries for a specific client/day with department info"""
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT t.EntryID, t.ClientDepartmentID, 
                       ISNULL(cd.DepartmentName, c.ClientName) AS DepartmentName,
                       t.HoursWorked, t.RateUsed, t.Notes,
                       cd.ClientDepartmentID, cd.BillingRate,
                       c.DefaultRate
                FROM TimeEntries AS t
                LEFT JOIN ClientDepartments AS cd ON t.ClientDepartmentID = cd.ClientDepartmentID
                JOIN Clients AS c ON t.ClientID = c.ClientID
                WHERE t.ClientID = ? AND t.WeekStartDate = ? AND t.DayOfWeek = ?
                ORDER BY ISNULL(cd.DepartmentName, 'General')
            """, (client_id, week_start_date, day_of_week))
            
            entries = []
            for row in cursor.fetchall():
                entry_rate = row.RateUsed
                if entry_rate is None:
                    if row.BillingRate:
                        entry_rate = row.BillingRate
                    else:
                        entry_rate = row.DefaultRate
                
                entries.append({
                    'EntryID': row.EntryID,
                    'ClientDepartmentID': row.ClientDepartmentID,
                    'DepartmentName': row.DepartmentName,
                    'HoursWorked': float(row.HoursWorked),
                    'RateUsed': float(entry_rate),
                    'Notes': row.Notes or ''
                })
            
            logger.info(f"Retrieved {len(entries)} entries for client {client_id}, day {day_of_week}")
            return entries
            
        except Exception as e:
            logger.error(f"Error getting day entries: {e}")
            raise DatabaseError(f"Failed to get day entries: {str(e)}")
        finally:
            if cursor:
                cursor.close()
    
    def save_day_entries(self, client_id, week_start_date, day_of_week, entries):
        """
        Save time entries for a specific client/day
        entries: [ { dept_id, hours, rate, notes }, ... ]
        """
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Delete existing entries for this day/client
            cursor.execute("""
                DELETE FROM TimeEntries
                WHERE ClientID = ? AND WeekStartDate = ? AND DayOfWeek = ?
            """, (client_id, week_start_date, day_of_week))
            
            # Insert new entries
            for entry in entries:
                if float(entry.get('hours', 0)) > 0:
                    cursor.execute("""
                        INSERT INTO TimeEntries 
                        (ClientID, WeekStartDate, DayOfWeek, ClientDepartmentID, 
                         HoursWorked, RateUsed, Notes)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        client_id,
                        week_start_date,
                        day_of_week,
                        entry.get('dept_id') or None,
                        float(entry.get('hours', 0)),
                        float(entry.get('rate', 0)),
                        entry.get('notes') or None
                    ))
            
            conn.commit()
            logger.info(f"Saved {len(entries)} entries for client {client_id}, day {day_of_week}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving day entries: {e}")
            raise DatabaseError(f"Failed to save day entries: {str(e)}")
        finally:
            if cursor:
                cursor.close()
    
    def save_time_entry(self, client_id, week_start_date, day_of_week, 
                       hours_worked, rate_used, notes='', dept_id=None):
        """Save or update a single time entry"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT t.EntryID FROM TimeEntries AS t
            WHERE t.ClientID = ? AND t.WeekStartDate = ? AND t.DayOfWeek = ? AND t.ClientDepartmentID IS ?
        """, (client_id, week_start_date, day_of_week, dept_id))
        
        existing = cursor.fetchone()
        
        if existing:
            if hours_worked > 0:
                cursor.execute("""
                    UPDATE TimeEntries
                    SET HoursWorked = ?, RateUsed = ?, Notes = ?
                    WHERE EntryID = ?
                """, (hours_worked, rate_used, notes, existing.EntryID))
                entry_id = existing.EntryID
            else:
                cursor.execute("DELETE FROM TimeEntries WHERE EntryID = ?", 
                             (existing.EntryID,))
                entry_id = None
        else:
            if hours_worked > 0:
                cursor.execute("""
                    INSERT INTO TimeEntries 
                    (ClientID, WeekStartDate, DayOfWeek, ClientDepartmentID, HoursWorked, RateUsed, Notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (client_id, week_start_date, day_of_week, dept_id, hours_worked, 
                      rate_used, notes))
                
                cursor.execute("SELECT @@IDENTITY AS NewID")
                entry_id = int(cursor.fetchone()[0])
            else:
                entry_id = None
        
        conn.commit()
        cursor.close()
        
        return entry_id
    
    def delete_time_entry(self, entry_id):
        """Delete a time entry"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM TimeEntries WHERE EntryID = ?", (entry_id,))
        conn.commit()
        cursor.close()
        
        return True
    
    # ===== INVOICE OPERATIONS =====
    
    def get_hours_grouped_by_department(self, client_id, start_date, end_date):
        """Get timesheet hours grouped by department for invoice creation"""
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    t.ClientDepartmentID,
                    ISNULL(cd.DepartmentName, 'General') AS DepartmentName,
                    ISNULL(cd.BillingRate, c.DefaultRate) AS BillingRate,
                    SUM(t.HoursWorked) AS TotalHours,
                    SUM(t.HoursWorked * ISNULL(t.RateUsed, ISNULL(cd.BillingRate, c.DefaultRate))) AS TotalAmount,
                    STRING_AGG(CAST(t.EntryID AS VARCHAR), ',') AS EntryIDs
                FROM TimeEntries AS t
                JOIN Clients AS c ON t.ClientID = c.ClientID
                LEFT JOIN ClientDepartments AS cd ON t.ClientDepartmentID = cd.ClientDepartmentID
                WHERE t.ClientID = ?
                  AND DATEADD(day, t.DayOfWeek - 1, t.WeekStartDate) >= ?
                  AND DATEADD(day, t.DayOfWeek - 1, t.WeekStartDate) <= ?
                  AND t.EntryID NOT IN (
                      SELECT DISTINCT ili_te.TimeEntryID 
                      FROM InvoiceLineItems_TimeEntries AS ili_te
                  )
                GROUP BY t.ClientDepartmentID, cd.DepartmentName, cd.BillingRate, c.DefaultRate
                ORDER BY ISNULL(cd.DepartmentName, 'General')
            """, (client_id, start_date, end_date))
            
            departments = []
            total_hours = 0.0
            total_amount = 0.0
            
            for row in cursor.fetchall():
                dept_hours = float(row.TotalHours)
                dept_amount = float(row.TotalAmount)
                entry_ids = [int(id) for id in row.EntryIDs.split(',')] if row.EntryIDs else []
                
                departments.append({
                    'ClientDepartmentID': row.ClientDepartmentID,
                    'DepartmentName': row.DepartmentName,
                    'TotalHours': dept_hours,
                    'BillingRate': float(row.BillingRate),
                    'TotalAmount': dept_amount,
                    'EntryIDs': entry_ids
                })
                
                total_hours += dept_hours
                total_amount += dept_amount
            
            logger.info(f"Retrieved {len(departments)} departments with {total_hours} hours for client {client_id}")
            return {
                'total_hours': total_hours,
                'total_amount': total_amount,
                'departments': departments
            }
            
        except Exception as e:
            logger.error(f"Error getting hours grouped by department: {e}")
            raise DatabaseError(f"Failed to get grouped hours: {str(e)}")
        finally:
            if cursor:
                cursor.close()
    
    def create_invoice(self, client_id, invoice_date, items, notes=""):
        """
        Create a new invoice with department-based line items
        items: [ { dept_id, line_description, total_hours, hourly_rate, entry_ids }, ... ]
        """
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Calculate totals
            total_hours = sum(float(item.get('total_hours', 0)) for item in items)
            total_amount = sum(float(item.get('hourly_rate', 0)) * float(item.get('total_hours', 0)) for item in items)
            
            # Generate unique invoice number
            invoice_number = None
            for attempt in range(1, 1000):
                candidate_number = f"INV-{invoice_date.year}-{str(attempt).zfill(4)}"
                cursor.execute("""
                    SELECT COUNT(*) FROM Invoices AS i
                    WHERE i.InvoiceNumber = ?
                """, (candidate_number,))
                if cursor.fetchone()[0] == 0:
                    invoice_number = candidate_number
                    break
            
            if not invoice_number:
                raise DatabaseError("Could not generate unique invoice number")
            
            # Get payment terms for due date
            cursor.execute("SELECT c.PaymentTerms FROM Clients AS c WHERE c.ClientID = ?", (client_id,))
            result = cursor.fetchone()
            payment_terms = result[0] if result else 30
            
            due_date = invoice_date + timedelta(days=payment_terms)
            
            # Create invoice
            cursor.execute("""
                INSERT INTO Invoices 
                (ClientID, InvoiceNumber, InvoiceDate, DueDate, TotalHours, TotalAmount, Status, Notes, CreatedDate, ModifiedDate)
                VALUES (?, ?, ?, ?, ?, ?, 'Draft', ?, GETDATE(), GETDATE())
            """, (client_id, invoice_number, invoice_date, due_date, total_hours, total_amount, notes))
            
            conn.commit()
            
            cursor.execute("SELECT @@IDENTITY")
            invoice_id = int(cursor.fetchone()[0])
            
            # Create line items and junction records
            for item in items:
                cursor.execute("""
                    INSERT INTO InvoiceLineItems 
                    (InvoiceID, ClientDepartmentID, LineDescription, BillingCategory, TotalHours, HourlyRate, Amount)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    invoice_id,
                    item.get('dept_id') or None,
                    item.get('line_description', 'Services Rendered'),
                    item.get('billing_category', 'General'),
                    float(item.get('total_hours', 0)),
                    float(item.get('hourly_rate', 0)),
                    float(item.get('total_hours', 0)) * float(item.get('hourly_rate', 0))
                ))
                
                line_item_id = int(cursor.fetchone()[0]) if cursor.rowcount > 0 else None
                
                # Link time entries to invoice line item
                if line_item_id and item.get('entry_ids'):
                    cursor.execute("SELECT @@IDENTITY")
                    line_item_id = int(cursor.fetchone()[0])
                    
                    for entry_id in item.get('entry_ids', []):
                        cursor.execute("""
                            INSERT INTO InvoiceLineItems_TimeEntries 
                            (LineItemID, TimeEntryID, HoursIncluded)
                            SELECT ?, ?, t.HoursWorked
                            FROM TimeEntries AS t
                            WHERE t.EntryID = ?
                        """, (line_item_id, entry_id, entry_id))
            
            conn.commit()
            
            logger.info(f"Invoice {invoice_number} created for client {client_id} with {len(items)} line items")
            return int(invoice_id)
            
        except Exception as e:
            logger.error(f"Error creating invoice: {e}")
            raise DatabaseError(f"Failed to create invoice: {str(e)}")
        finally:
            if cursor:
                cursor.close()
    
    def get_invoices(self, client_id=None):
        """Get all invoices, optionally filtered by client"""
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if client_id:
                cursor.execute("""
                    SELECT i.InvoiceID, i.ClientID, c.ClientName, i.InvoiceNumber, i.InvoiceDate, 
                           i.DueDate, i.TotalHours, i.TotalAmount, i.Status, i.Notes, i.CreatedDate
                    FROM Invoices AS i
                    JOIN Clients AS c ON i.ClientID = c.ClientID
                    WHERE i.ClientID = ?
                    ORDER BY i.InvoiceDate DESC
                """, (client_id,))
            else:
                cursor.execute("""
                    SELECT i.InvoiceID, i.ClientID, c.ClientName, i.InvoiceNumber, i.InvoiceDate, 
                           i.DueDate, i.TotalHours, i.TotalAmount, i.Status, i.Notes, i.CreatedDate
                    FROM Invoices AS i
                    JOIN Clients AS c ON i.ClientID = c.ClientID
                    ORDER BY i.InvoiceDate DESC
                """)
            
            invoices = []
            for row in cursor.fetchall():
                invoices.append({
                    'InvoiceID': row[0],
                    'ClientID': row[1],
                    'ClientName': row[2],
                    'InvoiceNumber': row[3],
                    'InvoiceDate': str(row[4]) if row[4] else None,
                    'DueDate': str(row[5]) if row[5] else None,
                    'TotalHours': float(row[6]),
                    'TotalAmount': float(row[7]),
                    'Status': row[8],
                    'Notes': row[9],
                    'CreatedDate': str(row[10]) if row[10] else None
                })
            
            logger.info(f"Retrieved {len(invoices)} invoices")
            return invoices
            
        except Exception as e:
            logger.error(f"Error getting invoices: {e}")
            raise DatabaseError(f"Failed to get invoices: {str(e)}")
        finally:
            if cursor:
                cursor.close()
    
    def get_invoice(self, invoice_id):
        """Get a specific invoice with line items"""
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Get invoice header
            cursor.execute("""
                SELECT i.InvoiceID, i.ClientID, c.ClientName, i.InvoiceNumber, i.InvoiceDate, 
                       i.DueDate, i.TotalHours, i.TotalAmount, i.Status, i.Notes, i.PDFPath
                FROM Invoices AS i
                JOIN Clients AS c ON i.ClientID = c.ClientID
                WHERE i.InvoiceID = ?
            """, (invoice_id,))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            invoice = {
                'InvoiceID': row[0],
                'ClientID': row[1],
                'ClientName': row[2],
                'InvoiceNumber': row[3],
                'InvoiceDate': str(row[4]) if row[4] else None,
                'DueDate': str(row[5]) if row[5] else None,
                'TotalHours': float(row[6]),
                'TotalAmount': float(row[7]),
                'Status': row[8],
                'Notes': row[9],
                'PDFPath': row[10]
            }
            
            # Get line items
            cursor.execute("""
                SELECT ili.LineItemID, ili.InvoiceID, ili.ClientDepartmentID, 
                       ili.LineDescription, ili.BillingCategory, ili.TotalHours, 
                       ili.HourlyRate, ili.Amount
                FROM InvoiceLineItems AS ili
                WHERE ili.InvoiceID = ?
                ORDER BY ili.LineItemID
            """, (invoice_id,))
            
            items = []
            for item_row in cursor.fetchall():
                items.append({
                    'ItemID': item_row[0],
                    'InvoiceID': item_row[1],
                    'ClientDepartmentID': item_row[2],
                    'LineDescription': item_row[3],
                    'BillingCategory': item_row[4],
                    'Hours': float(item_row[5]),
                    'Rate': float(item_row[6]),
                    'Amount': float(item_row[7])
                })
            
            invoice['Items'] = items
            logger.info(f"Retrieved invoice {invoice_id} with {len(items)} line items")
            return invoice
            
        except Exception as e:
            logger.error(f"Error getting invoice: {e}")
            raise DatabaseError(f"Failed to get invoice: {str(e)}")
        finally:
            if cursor:
                cursor.close()
    
    def update_invoice_status(self, invoice_id, status):
        """Update invoice status"""
        cursor = None
        try:
            valid_statuses = ['Draft', 'Sent', 'Paid', 'Overdue', 'Cancelled']
            if status not in valid_statuses:
                raise ValidationError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
            
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE Invoices
                SET Status = ?, ModifiedDate = GETDATE()
                WHERE InvoiceID = ?
            """, (status, invoice_id))
            
            conn.commit()
            logger.info(f"Invoice {invoice_id} status updated to {status}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating invoice status: {e}")
            raise DatabaseError(f"Failed to update invoice: {str(e)}")
        finally:
            if cursor:
                cursor.close()
    
    def update_invoice_pdf_path(self, invoice_id, pdf_path):
        """Update the PDF path for an invoice"""
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE Invoices
                SET PDFPath = ?, ModifiedDate = GETDATE()
                WHERE InvoiceID = ?
            """, (pdf_path, invoice_id))
            
            conn.commit()
            logger.info(f"Updated PDF path for invoice {invoice_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating PDF path: {e}")
            raise DatabaseError(f"Failed to update PDF path: {str(e)}")
        finally:
            if cursor:
                cursor.close()
    
    def delete_invoice(self, invoice_id):
        """Delete an invoice (and its items via cascade)"""
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM Invoices WHERE InvoiceID = ?", (invoice_id,))
            conn.commit()
            
            logger.info(f"Invoice {invoice_id} deleted")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting invoice: {e}")
            raise DatabaseError(f"Failed to delete invoice: {str(e)}")
        finally:
            if cursor:
                cursor.close()
    
    # ===== UTILITY FUNCTIONS =====
    
    def get_week_start(self, date=None):
        """Get the Monday of the week for a given date"""
        if date is None:
            date = datetime.now().date()
        
        days_since_monday = date.weekday()
        week_start = date - timedelta(days=days_since_monday)
        
        return week_start
    
    def get_week_dates(self, week_start):
        """Get all dates for a week (Mon-Sun)"""
        return [week_start + timedelta(days=i) for i in range(7)]

# Singleton instance
db = DatabaseHelper()
