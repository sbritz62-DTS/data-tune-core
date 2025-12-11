-- ================================================================
-- Data Tune Solutions - Data Quality Check Queries
-- Platform: T-SQL (SQL Server / Azure SQL)
-- Purpose: Standard validation queries for ETL pipelines
-- ================================================================

-- ----------------------------------------------------------------
-- 1. Row Count Comparison (Source vs Target)
-- ----------------------------------------------------------------
-- Use this to validate data loads completed successfully

SELECT 
    'Source' AS TableType,
    COUNT(*) AS RowCount,
    MIN(LoadDate) AS MinDate,
    MAX(LoadDate) AS MaxDate
FROM Source_Table
WHERE LoadDate >= CAST(GETDATE() AS DATE)  -- Today's data

UNION ALL

SELECT 
    'Target' AS TableType,
    COUNT(*) AS RowCount,
    MIN(LoadDate) AS MinDate,
    MAX(LoadDate) AS MaxDate
FROM Target_Table
WHERE LoadDate >= CAST(GETDATE() AS DATE);

-- ----------------------------------------------------------------
-- 2. Null Value Detection
-- ----------------------------------------------------------------
-- Check for nulls in critical columns

SELECT 
    'CustomerID' AS ColumnName,
    COUNT(*) AS NullCount,
    CAST(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Customers) AS DECIMAL(5,2)) AS NullPercentage
FROM Customers
WHERE CustomerID IS NULL

UNION ALL

SELECT 
    'Email' AS ColumnName,
    COUNT(*) AS NullCount,
    CAST(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Customers) AS DECIMAL(5,2)) AS NullPercentage
FROM Customers
WHERE Email IS NULL

UNION ALL

SELECT 
    'CreatedDate' AS ColumnName,
    COUNT(*) AS NullCount,
    CAST(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Customers) AS DECIMAL(5,2)) AS NullPercentage
FROM Customers
WHERE CreatedDate IS NULL;

-- ----------------------------------------------------------------
-- 3. Duplicate Detection
-- ----------------------------------------------------------------
-- Find duplicate records based on business key

-- Simple duplicate check
SELECT 
    CustomerEmail,
    COUNT(*) AS DuplicateCount
FROM Customers
GROUP BY CustomerEmail
HAVING COUNT(*) > 1;

-- Detailed duplicate analysis with record IDs
SELECT 
    a.CustomerID,
    a.CustomerEmail,
    a.CreatedDate,
    COUNT(*) OVER (PARTITION BY a.CustomerEmail) AS DuplicateCount
FROM Customers a
WHERE a.CustomerEmail IN (
    SELECT CustomerEmail 
    FROM Customers 
    GROUP BY CustomerEmail 
    HAVING COUNT(*) > 1
)
ORDER BY a.CustomerEmail, a.CreatedDate;

-- ----------------------------------------------------------------
-- 4. Referential Integrity Check
-- ----------------------------------------------------------------
-- Check for orphaned records (foreign key violations)

-- Orders without valid customers
SELECT 
    o.OrderID,
    o.CustomerID,
    'Missing Customer' AS Issue
FROM Orders o
LEFT JOIN Customers c ON o.CustomerID = c.CustomerID
WHERE c.CustomerID IS NULL;

-- Summary of referential integrity issues
SELECT 
    'Orders missing Customer' AS Check_Description,
    COUNT(*) AS IssueCount
FROM Orders o
LEFT JOIN Customers c ON o.CustomerID = c.CustomerID
WHERE c.CustomerID IS NULL

UNION ALL

SELECT 
    'OrderItems missing Order' AS Check_Description,
    COUNT(*) AS IssueCount
FROM OrderItems oi
LEFT JOIN Orders o ON oi.OrderID = o.OrderID
WHERE o.OrderID IS NULL;

-- ----------------------------------------------------------------
-- 5. Data Type Validation
-- ----------------------------------------------------------------
-- Check if string columns contain non-numeric data when they should be numeric

SELECT 
    CustomerID,
    PhoneNumber,
    'Phone contains non-numeric' AS Issue
FROM Customers
WHERE PhoneNumber NOT LIKE REPLICATE('[0-9]', LEN(PhoneNumber))
    AND PhoneNumber IS NOT NULL;

-- Check for invalid email formats (basic check)
SELECT 
    CustomerID,
    Email,
    'Invalid email format' AS Issue
FROM Customers
WHERE Email NOT LIKE '%@%.%'
    AND Email IS NOT NULL;

-- Check for invalid date ranges
SELECT 
    OrderID,
    OrderDate,
    ShippedDate,
    'Shipped before ordered' AS Issue
FROM Orders
WHERE ShippedDate < OrderDate;

-- ----------------------------------------------------------------
-- 6. Business Rule Validation
-- ----------------------------------------------------------------
-- Examples of common business rule checks

-- Negative amounts where they shouldn't be
SELECT 
    OrderID,
    Amount,
    'Negative amount detected' AS Issue
FROM Orders
WHERE Amount < 0;

-- Sales with zero or negative quantity
SELECT 
    SaleID,
    Quantity,
    'Invalid quantity' AS Issue
FROM Sales
WHERE Quantity <= 0;

-- Future dates in historical data
SELECT 
    TransactionID,
    TransactionDate,
    'Future date detected' AS Issue
FROM Transactions
WHERE TransactionDate > GETDATE();

-- ----------------------------------------------------------------
-- 7. Completeness Check
-- ----------------------------------------------------------------
-- Check data completeness by time period

WITH ExpectedDates AS (
    -- Generate expected date range
    SELECT CAST('2024-01-01' AS DATE) AS ExpectedDate
    UNION ALL
    SELECT DATEADD(DAY, 1, ExpectedDate)
    FROM ExpectedDates
    WHERE ExpectedDate < '2024-12-31'
),
ActualDates AS (
    SELECT DISTINCT CAST(TransactionDate AS DATE) AS ActualDate
    FROM Transactions
)
SELECT 
    ed.ExpectedDate,
    CASE WHEN ad.ActualDate IS NULL THEN 'Missing' ELSE 'Present' END AS Status
FROM ExpectedDates ed
LEFT JOIN ActualDates ad ON ed.ExpectedDate = ad.ActualDate
WHERE ad.ActualDate IS NULL
OPTION (MAXRECURSION 0);

-- ----------------------------------------------------------------
-- 8. Data Distribution / Outlier Detection
-- ----------------------------------------------------------------
-- Find outliers using IQR method or standard deviation

WITH Stats AS (
    SELECT 
        AVG(Amount) AS AvgAmount,
        STDEV(Amount) AS StdDevAmount,
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY Amount) OVER () AS Q1,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY Amount) OVER () AS Q3
    FROM Orders
)
SELECT DISTINCT
    'Outliers (3 Std Dev)' AS Method,
    COUNT(*) AS OutlierCount
FROM Orders o
CROSS JOIN Stats s
WHERE o.Amount > (s.AvgAmount + 3 * s.StdDevAmount)
   OR o.Amount < (s.AvgAmount - 3 * s.StdDevAmount);

-- ----------------------------------------------------------------
-- 9. Comprehensive Data Quality Report
-- ----------------------------------------------------------------
-- Run all checks and get summary report

WITH QualityChecks AS (
    -- Row count
    SELECT 
        'Total Records' AS CheckType,
        COUNT(*) AS Value,
        CAST(NULL AS VARCHAR(50)) AS Status
    FROM Customers
    
    UNION ALL
    
    -- Null checks
    SELECT 
        'Null EmailAddress' AS CheckType,
        COUNT(*) AS Value,
        CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END AS Status
    FROM Customers
    WHERE Email IS NULL
    
    UNION ALL
    
    -- Duplicates
    SELECT 
        'Duplicate Emails' AS CheckType,
        COUNT(*) AS Value,
        CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END AS Status
    FROM (
        SELECT Email
        FROM Customers
        GROUP BY Email
        HAVING COUNT(*) > 1
    ) Duplicates
    
    UNION ALL
    
    -- Orphaned records
    SELECT 
        'Orders Without Customer' AS CheckType,
        COUNT(*) AS Value,
        CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END AS Status
    FROM Orders o
    LEFT JOIN Customers c ON o.CustomerID = c.CustomerID
    WHERE c.CustomerID IS NULL
)
SELECT 
    CheckType,
    Value,
    Status,
    GETDATE() AS CheckDateTime
FROM QualityChecks
ORDER BY 
    CASE Status 
        WHEN 'FAIL' THEN 1 
        ELSE 2 
    END,
    CheckType;

-- ----------------------------------------------------------------
-- 10. Create Validation Log Table (One-time setup)
-- ----------------------------------------------------------------
/*
CREATE TABLE log_DataQualityChecks (
    LogID INT IDENTITY(1,1) PRIMARY KEY,
    CheckDateTime DATETIME DEFAULT GETDATE(),
    TableName VARCHAR(100),
    CheckType VARCHAR(100),
    ExpectedValue INT,
    ActualValue INT,
    Status VARCHAR(20),
    ErrorMessage VARCHAR(MAX)
);

-- Example of logging a quality check
INSERT INTO log_DataQualityChecks 
    (TableName, CheckType, ExpectedValue, ActualValue, Status, ErrorMessage)
VALUES 
    ('Customers', 'Row Count', 10000, 9995, 'Warning', '5 records missing');
*/

-- ================================================================
-- Usage Notes:
-- - Run these checks after each data load
-- - Adapt thresholds to your specific business rules
-- - Log results for trend analysis
-- - Set up alerts for critical failures
-- - Include in automated testing framework
-- ================================================================

