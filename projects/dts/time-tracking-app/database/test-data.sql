-- ================================================================
-- Data Tune Solutions - Time Tracking Application
-- Test Data Script
-- ================================================================

USE DataTuneTimeTracking;
GO

-- ================================================================
-- Clear existing data (for re-runs)
-- ================================================================
DELETE FROM InvoiceLineItems;
DELETE FROM Invoices;
DELETE FROM TimeEntries;
DELETE FROM Clients;

PRINT 'Existing data cleared';
GO

-- ================================================================
-- Sample Clients
-- ================================================================
INSERT INTO Clients (ClientName, DefaultRate, PaymentTerms, Active)
VALUES 
    ('Acme Corporation', 150.00, 30, 1),
    ('Beta Industries', 175.00, 15, 1),
    ('Gamma Solutions', 125.00, 30, 1),
    ('Delta Consulting', 200.00, 45, 1),
    ('Epsilon Tech', 160.00, 30, 0); -- Inactive client

PRINT 'Sample clients inserted: 5 clients (4 active, 1 inactive)';
GO

-- ================================================================
-- Sample Time Entries (Current Week)
-- ================================================================
DECLARE @CurrentWeekStart DATE;
SET @CurrentWeekStart = DATEADD(DAY, 1 - DATEPART(WEEKDAY, GETDATE()), CAST(GETDATE() AS DATE));

-- Acme Corporation - Full week
INSERT INTO TimeEntries (ClientID, WeekStartDate, DayOfWeek, HoursWorked, RateUsed, Notes)
VALUES 
    (1, @CurrentWeekStart, 1, 8.0, 150.00, 'Database optimization work'),
    (1, @CurrentWeekStart, 2, 6.5, 150.00, 'Power BI dashboard development'),
    (1, @CurrentWeekStart, 3, 7.0, 150.00, 'ETL pipeline troubleshooting'),
    (1, @CurrentWeekStart, 4, 8.0, 150.00, 'Client meeting and reporting'),
    (1, @CurrentWeekStart, 5, 5.5, 150.00, 'Documentation updates');

-- Beta Industries - Partial week
INSERT INTO TimeEntries (ClientID, WeekStartDate, DayOfWeek, HoursWorked, RateUsed, Notes)
VALUES 
    (2, @CurrentWeekStart, 1, 4.0, 175.00, 'Data migration planning'),
    (2, @CurrentWeekStart, 3, 6.0, 175.00, 'Azure Data Factory setup'),
    (2, @CurrentWeekStart, 5, 3.5, 175.00, 'Testing and validation');

-- Gamma Solutions - Two days
INSERT INTO TimeEntries (ClientID, WeekStartDate, DayOfWeek, HoursWorked, RateUsed, Notes)
VALUES 
    (3, @CurrentWeekStart, 2, 8.0, 125.00, 'SQL query optimization'),
    (3, @CurrentWeekStart, 4, 7.5, 125.00, 'Performance tuning');

PRINT 'Sample time entries inserted for current week';
GO

-- ================================================================
-- Sample Time Entries (Previous Week)
-- ================================================================
DECLARE @CurrentWeekStart DATE;
SET @CurrentWeekStart = DATEADD(DAY, 1 - DATEPART(WEEKDAY, GETDATE()), CAST(GETDATE() AS DATE));

DECLARE @PreviousWeekStart DATE;
SET @PreviousWeekStart = DATEADD(WEEK, -1, @CurrentWeekStart);

INSERT INTO TimeEntries (ClientID, WeekStartDate, DayOfWeek, HoursWorked, RateUsed, Notes)
VALUES 
    (1, @PreviousWeekStart, 1, 8.0, 150.00, 'Initial discovery meeting'),
    (1, @PreviousWeekStart, 2, 7.0, 150.00, 'Requirements gathering'),
    (1, @PreviousWeekStart, 3, 8.0, 150.00, 'Database design'),
    (1, @PreviousWeekStart, 4, 6.5, 150.00, 'Development work'),
    (1, @PreviousWeekStart, 5, 7.5, 150.00, 'Testing and deployment'),
    
    (4, @PreviousWeekStart, 2, 4.0, 200.00, 'Strategic consulting'),
    (4, @PreviousWeekStart, 4, 5.0, 200.00, 'Architecture review');

PRINT 'Sample time entries inserted for previous week';
GO

-- ================================================================
-- Sample Invoice (Previous Week - Acme Corp)
-- ================================================================
DECLARE @CurrentWeekStart DATE;
SET @CurrentWeekStart = DATEADD(DAY, 1 - DATEPART(WEEKDAY, GETDATE()), CAST(GETDATE() AS DATE));

DECLARE @PreviousWeekStart DATE;
SET @PreviousWeekStart = DATEADD(WEEK, -1, @CurrentWeekStart);

DECLARE @InvoiceDate DATE;
SET @InvoiceDate = DATEADD(DAY, 7, @PreviousWeekStart);

DECLARE @DueDate DATE;
SET @DueDate = DATEADD(DAY, 30, @InvoiceDate);

DECLARE @InvoiceID INT;

INSERT INTO Invoices (ClientID, InvoiceNumber, InvoiceDate, DueDate, TotalHours, TotalAmount, Status)
VALUES (1, 'INV-2024-001', @InvoiceDate, @DueDate, 37.0, 5550.00, 'Sent');

SET @InvoiceID = SCOPE_IDENTITY();

-- Link time entries to invoice
INSERT INTO InvoiceLineItems (InvoiceID, EntryID, Description, Hours, Rate, Amount)
SELECT 
    @InvoiceID,
    te.EntryID,
    c.ClientName + ' - Week of ' + CONVERT(VARCHAR(10), te.WeekStartDate, 101),
    te.HoursWorked,
    te.RateUsed,
    te.HoursWorked * te.RateUsed
FROM TimeEntries te
INNER JOIN Clients c ON te.ClientID = c.ClientID
WHERE te.ClientID = 1 
    AND te.WeekStartDate = @PreviousWeekStart;

PRINT 'Sample invoice created for Acme Corporation (previous week)';
GO

-- ================================================================
-- Verification Queries
-- ================================================================
DECLARE @CurrentWeekStart DATE;
SET @CurrentWeekStart = DATEADD(DAY, 1 - DATEPART(WEEKDAY, GETDATE()), CAST(GETDATE() AS DATE));

DECLARE @PreviousWeekStart DATE;
SET @PreviousWeekStart = DATEADD(WEEK, -1, @CurrentWeekStart);

DECLARE @TotalClients INT;
DECLARE @ActiveClients INT;
DECLARE @TotalEntries INT;
DECLARE @CurrentWeekHours DECIMAL(10,2);
DECLARE @PreviousWeekHours DECIMAL(10,2);
DECLARE @TotalInvoices INT;

SELECT @TotalClients = COUNT(*) FROM Clients;
SELECT @ActiveClients = COUNT(*) FROM Clients WHERE Active = 1;
SELECT @TotalEntries = COUNT(*) FROM TimeEntries;
SELECT @CurrentWeekHours = ISNULL(SUM(HoursWorked), 0) FROM TimeEntries WHERE WeekStartDate = @CurrentWeekStart;
SELECT @PreviousWeekHours = ISNULL(SUM(HoursWorked), 0) FROM TimeEntries WHERE WeekStartDate = @PreviousWeekStart;
SELECT @TotalInvoices = COUNT(*) FROM Invoices;

PRINT '';
PRINT '=== Data Verification ===';
PRINT '';

PRINT 'Total Clients: ' + CAST(@TotalClients AS VARCHAR);
PRINT 'Active Clients: ' + CAST(@ActiveClients AS VARCHAR);
PRINT '';

PRINT 'Total Time Entries: ' + CAST(@TotalEntries AS VARCHAR);
PRINT 'Current Week Hours: ' + CAST(@CurrentWeekHours AS VARCHAR);
PRINT 'Previous Week Hours: ' + CAST(@PreviousWeekHours AS VARCHAR);
PRINT '';

PRINT 'Total Invoices: ' + CAST(@TotalInvoices AS VARCHAR);
PRINT '';

-- Show summary by client
SELECT 
    c.ClientName,
    COUNT(DISTINCT te.WeekStartDate) AS WeeksTracked,
    SUM(te.HoursWorked) AS TotalHours,
    SUM(te.HoursWorked * te.RateUsed) AS TotalBillable
FROM Clients c
LEFT JOIN TimeEntries te ON c.ClientID = te.ClientID
WHERE c.Active = 1
GROUP BY c.ClientName
ORDER BY c.ClientName;

PRINT '';
PRINT 'Test data setup complete!';

