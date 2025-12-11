-- ================================================================
-- Data Tune Solutions - Date Transformation Patterns
-- Platform: T-SQL (SQL Server / Azure SQL)
-- ================================================================

-- ----------------------------------------------------------------
-- 1. Date Dimension / Calendar Table Generation
-- ----------------------------------------------------------------
-- Useful for creating a date dimension for Power BI or data warehouse

DECLARE @StartDate DATE = '2020-01-01';
DECLARE @EndDate DATE = '2030-12-31';

WITH DateRange AS (
    SELECT @StartDate AS DateValue
    UNION ALL
    SELECT DATEADD(DAY, 1, DateValue)
    FROM DateRange
    WHERE DateValue < @EndDate
)
SELECT 
    DateValue AS Date,
    YEAR(DateValue) AS Year,
    MONTH(DateValue) AS Month,
    DAY(DateValue) AS Day,
    DATENAME(MONTH, DateValue) AS MonthName,
    DATENAME(WEEKDAY, DateValue) AS DayOfWeekName,
    DATEPART(WEEKDAY, DateValue) AS DayOfWeek,
    DATEPART(QUARTER, DateValue) AS Quarter,
    DATEPART(WEEK, DateValue) AS WeekOfYear,
    DATEPART(DAYOFYEAR, DateValue) AS DayOfYear,
    CASE WHEN DATEPART(WEEKDAY, DateValue) IN (1, 7) THEN 1 ELSE 0 END AS IsWeekend,
    EOMONTH(DateValue) AS EndOfMonth,
    DATEFROMPARTS(YEAR(DateValue), MONTH(DateValue), 1) AS StartOfMonth
FROM DateRange
OPTION (MAXRECURSION 0);

-- ----------------------------------------------------------------
-- 2. Calculate Age from Date of Birth
-- ----------------------------------------------------------------
SELECT 
    DateOfBirth,
    DATEDIFF(YEAR, DateOfBirth, GETDATE()) - 
        CASE 
            WHEN MONTH(DateOfBirth) > MONTH(GETDATE()) 
                OR (MONTH(DateOfBirth) = MONTH(GETDATE()) AND DAY(DateOfBirth) > DAY(GETDATE()))
            THEN 1 
            ELSE 0 
        END AS Age
FROM Customers;

-- ----------------------------------------------------------------
-- 3. Business Days Calculation (excluding weekends)
-- ----------------------------------------------------------------
-- Calculate number of business days between two dates
DECLARE @StartDate2 DATE = '2024-01-01';
DECLARE @EndDate2 DATE = '2024-01-31';

SELECT 
    (DATEDIFF(DAY, @StartDate2, @EndDate2) + 1)  -- Total days
    - (DATEDIFF(WEEK, @StartDate2, @EndDate2) * 2)  -- Subtract weekends
    - CASE WHEN DATENAME(WEEKDAY, @StartDate2) = 'Sunday' THEN 1 ELSE 0 END
    - CASE WHEN DATENAME(WEEKDAY, @EndDate2) = 'Saturday' THEN 1 ELSE 0 END
    AS BusinessDays;

-- ----------------------------------------------------------------
-- 4. Time Period Flags (MTD, QTD, YTD)
-- ----------------------------------------------------------------
SELECT 
    TransactionDate,
    Amount,
    -- Month to Date
    CASE WHEN YEAR(TransactionDate) = YEAR(GETDATE()) 
         AND MONTH(TransactionDate) = MONTH(GETDATE()) 
         THEN 1 ELSE 0 END AS IsMTD,
    
    -- Quarter to Date  
    CASE WHEN YEAR(TransactionDate) = YEAR(GETDATE())
         AND DATEPART(QUARTER, TransactionDate) = DATEPART(QUARTER, GETDATE())
         THEN 1 ELSE 0 END AS IsQTD,
    
    -- Year to Date
    CASE WHEN YEAR(TransactionDate) = YEAR(GETDATE())
         AND TransactionDate <= GETDATE()
         THEN 1 ELSE 0 END AS IsYTD,
    
    -- Same Period Last Year
    DATEADD(YEAR, -1, TransactionDate) AS SameDateLastYear
FROM Transactions;

-- ----------------------------------------------------------------
-- 5. Date Bucketing / Grouping
-- ----------------------------------------------------------------
SELECT 
    -- Group by year-month
    DATEFROMPARTS(YEAR(OrderDate), MONTH(OrderDate), 1) AS YearMonth,
    
    -- Group by quarter
    CONCAT('Q', DATEPART(QUARTER, OrderDate), '-', YEAR(OrderDate)) AS Quarter,
    
    -- Group by week start (Monday)
    DATEADD(DAY, 1 - DATEPART(WEEKDAY, OrderDate), OrderDate) AS WeekStart,
    
    COUNT(*) AS OrderCount,
    SUM(Amount) AS TotalAmount
FROM Orders
GROUP BY 
    DATEFROMPARTS(YEAR(OrderDate), MONTH(OrderDate), 1),
    CONCAT('Q', DATEPART(QUARTER, OrderDate), '-', YEAR(OrderDate)),
    DATEADD(DAY, 1 - DATEPART(WEEKDAY, OrderDate), OrderDate);

-- ----------------------------------------------------------------
-- 6. Common Date Functions Reference
-- ----------------------------------------------------------------
-- Current date/time functions
SELECT 
    GETDATE() AS CurrentDateTime,
    GETUTCDATE() AS CurrentUTCDateTime,
    SYSDATETIME() AS HighPrecisionDateTime,
    CAST(GETDATE() AS DATE) AS CurrentDateOnly,
    CAST(GETDATE() AS TIME) AS CurrentTimeOnly;

-- Date arithmetic
SELECT
    DATEADD(DAY, 7, GETDATE()) AS OneWeekFromNow,
    DATEADD(MONTH, -1, GETDATE()) AS OneMonthAgo,
    DATEADD(YEAR, 1, GETDATE()) AS OneYearFromNow,
    DATEDIFF(DAY, '2024-01-01', GETDATE()) AS DaysSinceStartOfYear,
    DATEDIFF(HOUR, GETDATE(), DATEADD(DAY, 1, GETDATE())) AS HoursInDay;

-- Date parts
SELECT
    YEAR(GETDATE()) AS CurrentYear,
    MONTH(GETDATE()) AS CurrentMonth,
    DAY(GETDATE()) AS CurrentDay,
    DATENAME(WEEKDAY, GETDATE()) AS DayName,
    DATEPART(QUARTER, GETDATE()) AS CurrentQuarter,
    EOMONTH(GETDATE()) AS LastDayOfMonth,
    EOMONTH(GETDATE(), -1) AS LastDayOfPreviousMonth;

-- ----------------------------------------------------------------
-- 7. Time Zone Conversion (if needed)
-- ----------------------------------------------------------------
-- Convert UTC to EST
SELECT 
    UTCDateTime,
    UTCDateTime AT TIME ZONE 'UTC' AT TIME ZONE 'Eastern Standard Time' AS EasternTime
FROM Events;

-- ----------------------------------------------------------------
-- 8. Fiscal Year Calculations (Example: July 1 fiscal year start)
-- ----------------------------------------------------------------
SELECT 
    TransactionDate,
    CASE 
        WHEN MONTH(TransactionDate) >= 7 THEN YEAR(TransactionDate)
        ELSE YEAR(TransactionDate) - 1
    END AS FiscalYear,
    CASE
        WHEN MONTH(TransactionDate) >= 7 THEN MONTH(TransactionDate) - 6
        ELSE MONTH(TransactionDate) + 6
    END AS FiscalMonth
FROM Transactions;

-- ================================================================
-- Notes:
-- - Adapt fiscal year logic based on client requirements
-- - Consider creating functions for frequently used calculations
-- - Test edge cases (leap years, month-end dates, etc.)
-- ================================================================

