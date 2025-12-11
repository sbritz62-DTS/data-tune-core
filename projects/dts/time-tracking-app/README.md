# Time Tracking & Invoicing Application

## Overview
Desktop application for tracking billable hours and generating invoices. Replaces Excel-based time tracking with a streamlined Python GUI connected to SQL Server.

## Features

### Phase 1 (Current)
- ✅ SQL Server database setup
- ✅ Client management schema
- ✅ Time entry tracking
- ✅ Invoice data structure

### Phase 2 (Complete)
- ✅ Client Management GUI (add/edit clients and rates)
- ✅ Weekly timesheet view (Mon-Sun grid)
- ✅ Auto-save time entries
- ✅ Week navigation

### Phase 3 (Future)
- Invoice generation
- PDF export
- Reporting

## Tech Stack
- **Language**: Python 3.x
- **GUI**: Tkinter (built-in)
- **Database**: SQL Server (local instance)
- **PDF**: ReportLab

## Prerequisites

1. **Python 3.8+**
   - Download: https://www.python.org/downloads/
   - Make sure to check "Add Python to PATH" during installation

2. **SQL Server** (already installed)
   - Ensure SQL Server service is running
   - Note your server name (usually `localhost` or `.\SQLEXPRESS`)

3. **ODBC Driver for SQL Server**
   - Download: https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
   - Install "ODBC Driver 17 for SQL Server" or newer

## Installation

### Step 1: Database Setup

1. **Create the database** (using SQL Server Management Studio or Azure Data Studio):
   ```sql
   CREATE DATABASE DataTuneTimeTracking;
   GO
   ```

2. **Run the schema script**:
   - Open `database/schema.sql`
   - Execute against the `DataTuneTimeTracking` database
   - This creates all tables, indexes, stored procedures, and views

3. **Optional: Add test data**:
   - Open `database/test-data.sql`
   - Execute against the `DataTuneTimeTracking` database
   - This adds sample clients and time entries

### Step 2: Python Environment Setup

1. **Create virtual environment** (recommended):
   ```powershell
   cd "C:\Users\shane\Cursor Projects\projects\time-tracking-app"
   python -m venv venv
   .\venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

### Step 3: Configure Connection

1. **Copy the environment template**:
   ```powershell
   cp .env.template .env
   ```

2. **Edit `.env` file** with your SQL Server details:
   ```ini
   SQL_SERVER=localhost
   SQL_DATABASE=DataTuneTimeTracking
   SQL_TRUSTED_CONNECTION=yes
   ```

   Or if using SQL authentication:
   ```ini
   SQL_SERVER=localhost
   SQL_DATABASE=DataTuneTimeTracking
   SQL_USERNAME=your_username
   SQL_PASSWORD=your_password
   SQL_TRUSTED_CONNECTION=no
   ```

### Step 4: Test Connection

Run the connection test script:
```powershell
python src/test_connection.py
```

You should see: "✅ Connection successful!"

## Database Schema

### Clients Table
Stores client information and billing rates.

| Column | Type | Description |
|--------|------|-------------|
| ClientID | INT | Primary key |
| ClientName | NVARCHAR(200) | Client name |
| DefaultRate | DECIMAL(10,2) | Default hourly rate |
| PaymentTerms | INT | Payment terms in days (default 30) |
| Active | BIT | Active status |
| CreatedDate | DATETIME | Record created |
| ModifiedDate | DATETIME | Last modified |

### TimeEntries Table
Stores daily time entries for each client.

| Column | Type | Description |
|--------|------|-------------|
| EntryID | INT | Primary key |
| ClientID | INT | Foreign key to Clients |
| WeekStartDate | DATE | Monday of the work week |
| DayOfWeek | TINYINT | 1=Mon, 7=Sun |
| HoursWorked | DECIMAL(5,2) | Hours worked |
| RateUsed | DECIMAL(10,2) | Rate (can override default) |
| Notes | NVARCHAR(500) | Optional notes |
| CreatedDate | DATETIME | Record created |

### Invoices Table
Tracks generated invoices (Phase 2).

| Column | Type | Description |
|--------|------|-------------|
| InvoiceID | INT | Primary key |
| ClientID | INT | Foreign key to Clients |
| InvoiceNumber | NVARCHAR(50) | Unique invoice number |
| InvoiceDate | DATE | Invoice date |
| DueDate | DATE | Payment due date |
| TotalHours | DECIMAL(10,2) | Total billable hours |
| TotalAmount | DECIMAL(12,2) | Total invoice amount |
| Status | NVARCHAR(20) | Draft/Sent/Paid/Overdue |
| PDFPath | NVARCHAR(500) | Path to generated PDF |

## Project Structure

```
time-tracking-app/
├── database/
│   ├── schema.sql           # Database schema
│   └── test-data.sql        # Sample data
├── src/
│   ├── test_connection.py   # Connection test script
│   ├── db_helper.py          # Database operations module
│   ├── gui_main.py           # Main application window
│   ├── gui_clients.py        # Client management screen
│   └── gui_timesheet.py      # Weekly timesheet screen
├── run_app.py                # Application launcher
├── docs/
│   └── (future documentation)
├── .env.template            # Connection config template
├── .env                     # Your actual config (not committed)
├── .gitignore              # Git ignore rules
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Running the Application

### Start the App

1. **Activate virtual environment** (if not already active):
   ```powershell
   cd "C:\Users\shane\Cursor Projects\projects\time-tracking-app"
   .\venv\Scripts\activate
   ```

2. **Run the application**:
   ```powershell
   python run_app.py
   ```

The application window will open with two main screens:
- **Timesheet**: Weekly time entry grid (Mon-Sun x Clients)
- **Clients**: Manage clients and rates

### Using the Timesheet

1. Navigate weeks using Previous/Next/Current Week buttons
2. Enter hours directly in grid cells (Mon-Sun columns)
3. Hours auto-save when you leave a cell
4. Click "Save All Changes" to manually save everything
5. Weekly totals and amounts shown at bottom

### Managing Clients

1. Click "👥 Clients" button
2. View all active clients in the list
3. Add new clients with "Add New Client" button
4. Edit clients by selecting and clicking "Edit Selected"
5. Deactivate clients (removes from timesheet) with "Deactivate Selected"

## Usage (Database Only)

You can also work directly with SQL if needed:

1. **Add clients manually**:
   ```sql
   INSERT INTO Clients (ClientName, DefaultRate, PaymentTerms)
   VALUES ('Your Client Name', 150.00, 30);
   ```

2. **Add time entries**:
   ```sql
   INSERT INTO TimeEntries (ClientID, WeekStartDate, DayOfWeek, HoursWorked, RateUsed)
   VALUES (1, '2024-12-09', 1, 8.0, 150.00);
   ```

3. **View weekly totals**:
   ```sql
   SELECT * FROM vw_WeeklyClientTotals
   WHERE WeekStartDate = '2024-12-09'
   ORDER BY ClientName;
   ```

4. **Get weekly timesheet**:
   ```sql
   EXEC usp_GetWeeklyTimesheet @WeekStartDate = '2024-12-09';
   ```

## Development Roadmap

- [x] Phase 1: Database setup
- [x] Phase 2: GUI Application (Client Management + Weekly Timesheet)
- [ ] Phase 3: Invoice Generation & PDF Export
- [ ] Phase 4: Invoice generation and PDF export

## Troubleshooting

### Connection Issues

**Error: "pyodbc.Error: ('01000', '[01000]..."**
- Install ODBC Driver: https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server

**Error: "Login failed for user"**
- Check SQL Server authentication mode (mixed mode required for SQL auth)
- Or use Windows Authentication (set `SQL_TRUSTED_CONNECTION=yes`)

**Error: "Cannot open database"**
- Verify database exists: Run `CREATE DATABASE DataTuneTimeTracking;`
- Check database name in `.env` file

### Python Issues

**Error: "python: command not found"**
- Install Python 3.8+
- Ensure Python is in your PATH

**Error: "No module named 'pyodbc'"**
- Activate virtual environment: `.\venv\Scripts\activate`
- Install dependencies: `pip install -r requirements.txt`

## Support

For issues or questions about this application, refer to the Data Tune Solutions documentation in `data-tune-core/docs/`.

---

**Data Tune Solutions** - Time Tracking Application
*Version 1.0 - Phase 1*

