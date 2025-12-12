-- =============================================
-- Null Detection and Handling Patterns
-- Data Tune Solutions
-- =============================================
-- Patterns for finding, analyzing, and handling NULL values
-- Platform: T-SQL (SQL Server / Azure SQL)
-- =============================================

-- =============================================
-- Pattern 1: Find Columns with High Null Rates
-- =============================================
-- Identify which columns have missing data
-- Use for: Data quality assessment, choosing features

-- Generate NULL count for all columns in a table
DECLARE @TableName NVARCHAR(128) = 'YourTableName';
DECLARE @SQL NVARCHAR(MAX) = '';

SELECT @SQL = @SQL +
    'SELECT ''' + COLUMN_NAME + ''' AS ColumnName, ' +
    'COUNT(*) AS TotalRows, ' +
    'SUM(CASE WHEN [' + COLUMN_NAME + '] IS NULL THEN 1 ELSE 0 END) AS NullCount, ' +
    'CAST(SUM(CASE WHEN [' + COLUMN_NAME + '] IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS NullPercent ' +
    'FROM ' + @TableName + ' UNION ALL '
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = @TableName;

-- Remove trailing UNION ALL
SET @SQL = LEFT(@SQL, LEN(@SQL) - 10);

-- Add ORDER BY
SET @SQL = @SQL + ' ORDER BY NullPercent DESC';

-- Execute
EXEC sp_executesql @SQL;

-- =============================================
-- Pattern 2: NULL Summary Report
-- =============================================
-- Comprehensive NULL analysis for a table
-- Use for: Data profiling, quality reports

WITH NullAnalysis AS (
    SELECT
        COUNT(*) AS TotalRecords,

        -- Count NULLs per column
        SUM(CASE WHEN Column1 IS NULL THEN 1 ELSE 0 END) AS Column1_Nulls,
        SUM(CASE WHEN Column2 IS NULL THEN 1 ELSE 0 END) AS Column2_Nulls,
        SUM(CASE WHEN Column3 IS NULL THEN 1 ELSE 0 END) AS Column3_Nulls,

        -- Percentage NULLs
        CAST(SUM(CASE WHEN Column1 IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS Column1_NullPct,
        CAST(SUM(CASE WHEN Column2 IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS Column2_NullPct,
        CAST(SUM(CASE WHEN Column3 IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS Column3_NullPct,

        -- Records with ALL columns NULL
        SUM(CASE
            WHEN Column1 IS NULL AND Column2 IS NULL AND Column3 IS NULL
            THEN 1 ELSE 0
        END) AS AllNulls,

        -- Records with ANY column NULL
        SUM(CASE
            WHEN Column1 IS NULL OR Column2 IS NULL OR Column3 IS NULL
            THEN 1 ELSE 0
        END) AS AnyNulls,

        -- Records with NO nulls (complete records)
        SUM(CASE
            WHEN Column1 IS NOT NULL AND Column2 IS NOT NULL AND Column3 IS NOT NULL
            THEN 1 ELSE 0
        END) AS NoNulls
    FROM YourTable
)
SELECT
    TotalRecords,
    Column1_Nulls,
    Column1_NullPct,
    Column2_Nulls,
    Column2_NullPct,
    Column3_Nulls,
    Column3_NullPct,
    AllNulls,
    AnyNulls,
    NoNulls,
    CAST(NoNulls * 100.0 / TotalRecords AS DECIMAL(5,2)) AS CompleteRecordsPct
FROM NullAnalysis;

-- =============================================
-- Pattern 3: Required Field Validation
-- =============================================
-- Find records missing required fields
-- Use for: Data validation, ETL error detection

SELECT
    RecordID,
    CASE WHEN RequiredField1 IS NULL THEN 'Missing RequiredField1' ELSE '' END +
    CASE WHEN RequiredField2 IS NULL THEN 'Missing RequiredField2' ELSE '' END +
    CASE WHEN RequiredField3 IS NULL THEN 'Missing RequiredField3' ELSE '' END AS MissingFields,

    -- Count of missing required fields
    (CASE WHEN RequiredField1 IS NULL THEN 1 ELSE 0 END +
     CASE WHEN RequiredField2 IS NULL THEN 1 ELSE 0 END +
     CASE WHEN RequiredField3 IS NULL THEN 1 ELSE 0 END) AS MissingCount
FROM YourTable
WHERE RequiredField1 IS NULL
   OR RequiredField2 IS NULL
   OR RequiredField3 IS NULL
ORDER BY MissingCount DESC;

-- =============================================
-- Pattern 4: NULL vs Empty String Detection
-- =============================================
-- Distinguish between NULL and empty strings
-- Use for: Data cleansing, standardization

SELECT
    FieldName,

    -- Count actual NULLs
    SUM(CASE WHEN FieldName IS NULL THEN 1 ELSE 0 END) AS TrueNulls,

    -- Count empty strings
    SUM(CASE WHEN FieldName = '' THEN 1 ELSE 0 END) AS EmptyStrings,

    -- Count whitespace only
    SUM(CASE WHEN LTRIM(RTRIM(FieldName)) = '' AND FieldName IS NOT NULL THEN 1 ELSE 0 END) AS WhitespaceOnly,

    -- Count "missing" values (NULL or empty or whitespace)
    SUM(CASE
        WHEN FieldName IS NULL
          OR FieldName = ''
          OR LTRIM(RTRIM(FieldName)) = ''
        THEN 1 ELSE 0
    END) AS TotalMissing,

    -- Count valid values
    SUM(CASE
        WHEN FieldName IS NOT NULL
         AND FieldName <> ''
         AND LTRIM(RTRIM(FieldName)) <> ''
        THEN 1 ELSE 0
    END) AS ValidValues
FROM YourTable;

-- =============================================
-- Pattern 5: NULL Impact Analysis
-- =============================================
-- Understand how NULLs affect calculations
-- Use for: Revenue analysis, metric validation

SELECT
    Category,

    -- Without handling NULLs (incorrect)
    AVG(SalesAmount) AS AvgWithNulls,  -- Excludes NULLs from calculation

    -- Treating NULLs as zero (may be appropriate)
    AVG(ISNULL(SalesAmount, 0)) AS AvgTreatingNullsAsZero,

    -- Count of NULLs
    SUM(CASE WHEN SalesAmount IS NULL THEN 1 ELSE 0 END) AS NullCount,

    -- Percentage of records with values
    CAST(COUNT(SalesAmount) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS PopulatedPercent,

    -- Sum comparison
    SUM(SalesAmount) AS SumIgnoringNulls,
    SUM(ISNULL(SalesAmount, 0)) AS SumTreatingNullsAsZero,

    -- Difference
    SUM(ISNULL(SalesAmount, 0)) - SUM(SalesAmount) AS Difference  -- Always 0
FROM Sales
GROUP BY Category;

-- =============================================
-- Pattern 6: Conditional NULL Replacement
-- =============================================
-- Replace NULLs with appropriate values
-- Use for: Data cleaning, report preparation

SELECT
    CustomerID,

    -- Replace with zero
    ISNULL(OrderCount, 0) AS OrderCount,

    -- Replace with default value
    ISNULL(CustomerType, 'Unknown') AS CustomerType,

    -- Replace with calculated value
    ISNULL(LastOrderDate, GETDATE()) AS LastOrderDate,

    -- Chain of fallbacks (COALESCE)
    COALESCE(Email, AlternateEmail, 'no-email@example.com') AS ContactEmail,

    -- Conditional replacement
    CASE
        WHEN Phone IS NULL AND HasAccount = 1 THEN '[Contact Required]'
        WHEN Phone IS NULL AND HasAccount = 0 THEN '[Not Applicable]'
        ELSE Phone
    END AS PhoneNumber
FROM Customers;

-- =============================================
-- Pattern 7: NULL Propagation in Calculations
-- =============================================
-- Handle NULLs in mathematical operations
-- Use for: Avoiding unexpected NULL results

SELECT
    OrderID,
    Quantity,
    UnitPrice,
    Discount,

    -- Bad: NULL in any field causes NULL result
    Quantity * UnitPrice * (1 - Discount) AS TotalBad,

    -- Good: Handle NULLs explicitly
    ISNULL(Quantity, 0) * ISNULL(UnitPrice, 0) * (1 - ISNULL(Discount, 0)) AS TotalGood,

    -- Alternative: Only calculate if all values present
    CASE
        WHEN Quantity IS NOT NULL AND UnitPrice IS NOT NULL AND Discount IS NOT NULL
        THEN Quantity * UnitPrice * (1 - Discount)
        ELSE NULL
    END AS TotalConditional
FROM OrderDetails;

-- =============================================
-- Pattern 8: NULL in JOINs
-- =============================================
-- Handle NULLs when joining tables
-- Use for: Finding orphan records, data validation

-- Find records in Table A without matches in Table B (including NULLs)
SELECT
    a.ID,
    a.Name,
    CASE
        WHEN a.ForeignKeyID IS NULL THEN 'NULL Foreign Key'
        WHEN b.ID IS NULL THEN 'Orphan Record'
        ELSE 'Valid'
    END AS Status
FROM TableA a
LEFT JOIN TableB b ON a.ForeignKeyID = b.ID
WHERE a.ForeignKeyID IS NULL OR b.ID IS NULL;

-- =============================================
-- Pattern 9: NULL Density Over Time
-- =============================================
-- Track NULL rates by time period
-- Use for: Data quality monitoring, identifying issues

SELECT
    YEAR(CreatedDate) AS Year,
    MONTH(CreatedDate) AS Month,
    COUNT(*) AS TotalRecords,

    -- NULL counts per field
    SUM(CASE WHEN Email IS NULL THEN 1 ELSE 0 END) AS Email_Nulls,
    SUM(CASE WHEN Phone IS NULL THEN 1 ELSE 0 END) AS Phone_Nulls,
    SUM(CASE WHEN Address IS NULL THEN 1 ELSE 0 END) AS Address_Nulls,

    -- NULL percentages
    CAST(SUM(CASE WHEN Email IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS Email_NullPct,
    CAST(SUM(CASE WHEN Phone IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS Phone_NullPct,
    CAST(SUM(CASE WHEN Address IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS Address_NullPct
FROM Customers
GROUP BY YEAR(CreatedDate), MONTH(CreatedDate)
ORDER BY Year DESC, Month DESC;

-- =============================================
-- Pattern 10: Automated NULL Detection Report
-- =============================================
-- Generate comprehensive NULL report for data quality dashboard
-- Use for: Regular monitoring, alerting

WITH NullStats AS (
    SELECT
        'TableName' AS TableName,
        'Column1' AS ColumnName,
        COUNT(*) AS TotalRows,
        SUM(CASE WHEN Column1 IS NULL THEN 1 ELSE 0 END) AS NullCount,
        CAST(SUM(CASE WHEN Column1 IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS NullPercent,
        MIN(CreatedDate) AS OldestRecord,
        MAX(CreatedDate) AS NewestRecord
    FROM YourTable
    -- Repeat for each column...
)
SELECT
    TableName,
    ColumnName,
    TotalRows,
    NullCount,
    NullPercent,
    CASE
        WHEN NullPercent = 0 THEN 'Excellent'
        WHEN NullPercent < 5 THEN 'Good'
        WHEN NullPercent < 20 THEN 'Acceptable'
        WHEN NullPercent < 50 THEN 'Poor'
        ELSE 'Critical'
    END AS QualityRating,
    OldestRecord,
    NewestRecord,
    DATEDIFF(day, OldestRecord, NewestRecord) AS DataSpanDays
FROM NullStats
WHERE NullPercent > 0  -- Only show columns with NULLs
ORDER BY NullPercent DESC;

-- =============================================
-- Usage Examples
-- =============================================

-- Example 1: Clean NULL values before loading to data warehouse
UPDATE StagingTable
SET
    Email = CASE WHEN Email = '' OR LTRIM(RTRIM(Email)) = '' THEN NULL ELSE Email END,
    Phone = CASE WHEN Phone = '' OR LTRIM(RTRIM(Phone)) = '' THEN NULL ELSE Phone END,
    CustomerType = COALESCE(NULLIF(CustomerType, ''), 'Unknown');

-- Example 2: Flag records for review
SELECT
    CustomerID,
    'High NULL density' AS IssueType,
    (CASE WHEN Email IS NULL THEN 1 ELSE 0 END +
     CASE WHEN Phone IS NULL THEN 1 ELSE 0 END +
     CASE WHEN Address IS NULL THEN 1 ELSE 0 END +
     CASE WHEN City IS NULL THEN 1 ELSE 0 END) AS NullFieldCount
FROM Customers
WHERE (CASE WHEN Email IS NULL THEN 1 ELSE 0 END +
       CASE WHEN Phone IS NULL THEN 1 ELSE 0 END +
       CASE WHEN Address IS NULL THEN 1 ELSE 0 END +
       CASE WHEN City IS NULL THEN 1 ELSE 0 END) >= 3;

-- Example 3: Data quality alert
IF EXISTS (
    SELECT 1
    FROM Customers
    WHERE Email IS NULL
      AND CreatedDate >= DATEADD(day, -7, GETDATE())
    HAVING COUNT(*) > 100
)
BEGIN
    -- Send alert: Over 100 customers added in last 7 days without email
    PRINT 'ALERT: High NULL rate in recent customer data';
END

-- =============================================
-- Performance Tips
-- =============================================
-- 1. Index columns frequently checked for NULL (WHERE col IS NULL)
-- 2. Consider filtered indexes for sparse columns
-- 3. Use computed persisted columns for complex NULL handling
-- 4. For data quality checks, run during off-peak hours
-- 5. Consider creating a DQ_NullStats summary table updated nightly

-- =============================================
-- Best Practices
-- =============================================
-- 1. Distinguish between NULL (unknown) and empty/zero (known to be absent)
-- 2. Document business meaning of NULLs in each column
-- 3. Establish NULL handling standards for your organization
-- 4. Monitor NULL rates over time for data quality trends
-- 5. Use constraints (NOT NULL) to enforce data requirements at database level

-- =============================================
