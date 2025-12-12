-- =============================================
-- Incremental Load Patterns
-- Data Tune Solutions
-- =============================================
-- Patterns for loading only new/changed data
-- Platform: T-SQL (SQL Server / Azure SQL)
-- =============================================

-- =============================================
-- Pattern 1: Simple Watermark (Date-Based)
-- =============================================
-- Load records modified since last load
-- Use for: Daily ETL, change tracking

-- Step 1: Get last load date
DECLARE @LastLoadDate DATETIME;
SELECT @LastLoadDate = MAX(LoadDate) FROM TargetTable;

-- If first load, use a default start date
IF @LastLoadDate IS NULL
    SET @LastLoadDate = '1900-01-01';

-- Step 2: Load new/modified records
INSERT INTO TargetTable (ID, Name, Value, ModifiedDate, LoadDate)
SELECT
    ID,
    Name,
    Value,
    ModifiedDate,
    GETDATE() AS LoadDate
FROM SourceTable
WHERE ModifiedDate > @LastLoadDate;

-- Step 3: Log the load
INSERT INTO ETL_LoadLog (TableName, LoadDate, RowsLoaded)
VALUES ('TargetTable', GETDATE(), @@ROWCOUNT);

-- =============================================
-- Pattern 2: Watermark with Configurable Table
-- =============================================
-- Centralized watermark management
-- Use for: Multiple table loads, production ETL

-- Create watermark table (one-time setup)
IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name = 'ETL_Watermarks')
BEGIN
    CREATE TABLE ETL_Watermarks (
        TableName VARCHAR(100) PRIMARY KEY,
        WatermarkValue DATETIME NOT NULL,
        LastUpdateDate DATETIME NOT NULL
    );
END

-- Get watermark
DECLARE @TableName VARCHAR(100) = 'SourceTable';
DECLARE @Watermark DATETIME;

SELECT @Watermark = WatermarkValue
FROM ETL_Watermarks
WHERE TableName = @TableName;

-- If no watermark exists, initialize
IF @Watermark IS NULL
BEGIN
    SET @Watermark = '1900-01-01';
    INSERT INTO ETL_Watermarks (TableName, WatermarkValue, LastUpdateDate)
    VALUES (@TableName, @Watermark, GETDATE());
END

-- Load incremental data
INSERT INTO TargetTable (ID, Data, ModifiedDate, LoadDate)
SELECT
    ID,
    Data,
    ModifiedDate,
    GETDATE()
FROM SourceTable
WHERE ModifiedDate > @Watermark;

-- Update watermark
DECLARE @NewWatermark DATETIME = (SELECT MAX(ModifiedDate) FROM SourceTable);

UPDATE ETL_Watermarks
SET
    WatermarkValue = @NewWatermark,
    LastUpdateDate = GETDATE()
WHERE TableName = @TableName;

-- =============================================
-- Pattern 3: Change Data Capture (CDC)
-- =============================================
-- Track inserts, updates, deletes separately
-- Use for: Maintaining slowly changing dimensions

-- Enable CDC (one-time setup, requires sysadmin)
-- EXEC sys.sp_cdc_enable_db;
-- EXEC sys.sp_cdc_enable_table
--     @source_schema = 'dbo',
--     @source_name = 'SourceTable',
--     @role_name = NULL;

-- Query CDC data
DECLARE @from_lsn BINARY(10), @to_lsn BINARY(10);

-- Get LSN range
SET @from_lsn = sys.fn_cdc_get_min_lsn('dbo_SourceTable');
SET @to_lsn = sys.fn_cdc_get_max_lsn();

-- Get all changes
SELECT
    __$operation AS Operation,  -- 1=Delete, 2=Insert, 3=Update(before), 4=Update(after)
    __$start_lsn AS LSN,
    ID,
    Name,
    Value,
    ModifiedDate
FROM cdc.fn_cdc_get_all_changes_dbo_SourceTable(@from_lsn, @to_lsn, 'all')
ORDER BY __$start_lsn;

-- Process changes
MERGE TargetTable AS Target
USING (
    SELECT ID, Name, Value, ModifiedDate, __$operation
    FROM cdc.fn_cdc_get_all_changes_dbo_SourceTable(@from_lsn, @to_lsn, 'all')
    WHERE __$operation IN (2, 4)  -- Insert or Update
) AS Source
ON Target.ID = Source.ID
WHEN MATCHED THEN
    UPDATE SET
        Target.Name = Source.Name,
        Target.Value = Source.Value,
        Target.ModifiedDate = Source.ModifiedDate,
        Target.LoadDate = GETDATE()
WHEN NOT MATCHED BY TARGET THEN
    INSERT (ID, Name, Value, ModifiedDate, LoadDate)
    VALUES (Source.ID, Source.Name, Source.Value, Source.ModifiedDate, GETDATE());

-- Handle deletes
DELETE FROM TargetTable
WHERE ID IN (
    SELECT ID
    FROM cdc.fn_cdc_get_all_changes_dbo_SourceTable(@from_lsn, @to_lsn, 'all')
    WHERE __$operation = 1  -- Delete
);

-- =============================================
-- Pattern 4: Hash-Based Change Detection
-- =============================================
-- Detect changes without ModifiedDate column
-- Use for: External sources, flat files

-- Step 1: Add hash column to target (one-time)
-- ALTER TABLE TargetTable ADD RowHash VARBINARY(32);

-- Step 2: Calculate hash and compare
WITH SourceWithHash AS (
    SELECT
        ID,
        Name,
        Value,
        HASHBYTES('SHA2_256',
            CONCAT(
                ISNULL(CAST(ID AS VARCHAR(50)), ''),
                ISNULL(Name, ''),
                ISNULL(CAST(Value AS VARCHAR(50)), '')
            )
        ) AS RowHash
    FROM SourceTable
)
MERGE TargetTable AS Target
USING SourceWithHash AS Source
ON Target.ID = Source.ID
WHEN MATCHED AND Target.RowHash <> Source.RowHash THEN
    -- Row changed
    UPDATE SET
        Target.Name = Source.Name,
        Target.Value = Source.Value,
        Target.RowHash = Source.RowHash,
        Target.LoadDate = GETDATE()
WHEN NOT MATCHED BY TARGET THEN
    -- New row
    INSERT (ID, Name, Value, RowHash, LoadDate)
    VALUES (Source.ID, Source.Name, Source.Value, Source.RowHash, GETDATE())
WHEN NOT MATCHED BY SOURCE THEN
    -- Deleted in source (optional: soft delete)
    UPDATE SET
        Target.IsActive = 0,
        Target.LoadDate = GETDATE();

-- =============================================
-- Pattern 5: Partitioned Incremental Load
-- =============================================
-- Load data in chunks/batches
-- Use for: Large tables, avoiding locks

DECLARE @BatchSize INT = 10000;
DECLARE @LastID INT = 0;
DECLARE @MaxID INT;

SELECT @MaxID = MAX(ID) FROM SourceTable;

WHILE @LastID < @MaxID
BEGIN
    -- Load batch
    INSERT INTO TargetTable (ID, Data, LoadDate)
    SELECT
        ID,
        Data,
        GETDATE()
    FROM SourceTable
    WHERE ID > @LastID
      AND ID <= @LastID + @BatchSize
      AND ModifiedDate > (SELECT MAX(LoadDate) FROM TargetTable);

    SET @LastID = @LastID + @BatchSize;

    -- Log progress
    PRINT 'Loaded batch up to ID: ' + CAST(@LastID AS VARCHAR);

    -- Optional: Brief pause to reduce locking
    WAITFOR DELAY '00:00:01';
END

-- =============================================
-- Pattern 6: Upsert with Slowly Changing Dimension Type 2
-- =============================================
-- Maintain history of changes
-- Use for: Data warehouse dimensions

MERGE DimCustomer AS Target
USING StagingCustomer AS Source
ON Target.CustomerBusinessKey = Source.CustomerID
   AND Target.IsCurrent = 1
WHEN MATCHED AND (
    Target.Name <> Source.Name OR
    Target.Email <> Source.Email
) THEN
    -- Expire old record
    UPDATE SET
        Target.IsCurrent = 0,
        Target.EndDate = GETDATE()
WHEN NOT MATCHED BY TARGET THEN
    -- New customer
    INSERT (CustomerBusinessKey, Name, Email, StartDate, EndDate, IsCurrent)
    VALUES (Source.CustomerID, Source.Name, Source.Email, GETDATE(), NULL, 1);

-- Insert changed records as new rows
INSERT INTO DimCustomer (CustomerBusinessKey, Name, Email, StartDate, EndDate, IsCurrent)
SELECT
    Source.CustomerID,
    Source.Name,
    Source.Email,
    GETDATE() AS StartDate,
    NULL AS EndDate,
    1 AS IsCurrent
FROM StagingCustomer Source
INNER JOIN DimCustomer Target
    ON Target.CustomerBusinessKey = Source.CustomerID
    AND Target.IsCurrent = 0
    AND Target.EndDate = CAST(GETDATE() AS DATE)  -- Just expired
WHERE Target.Name <> Source.Name
   OR Target.Email <> Source.Email;

-- =============================================
-- Pattern 7: Delta Detection with Staging Table
-- =============================================
-- Compare full snapshot to find changes
-- Use for: API loads, external data sources

-- Step 1: Load full snapshot to staging
TRUNCATE TABLE StagingCustomers;

INSERT INTO StagingCustomers (CustomerID, Name, Email, Status)
SELECT CustomerID, Name, Email, Status
FROM ExternalSource;

-- Step 2: Find new records
INSERT INTO Customers (CustomerID, Name, Email, Status, CreatedDate)
SELECT
    s.CustomerID,
    s.Name,
    s.Email,
    s.Status,
    GETDATE()
FROM StagingCustomers s
LEFT JOIN Customers c ON s.CustomerID = c.CustomerID
WHERE c.CustomerID IS NULL;

-- Step 3: Find updated records
UPDATE c
SET
    c.Name = s.Name,
    c.Email = s.Email,
    c.Status = s.Status,
    c.ModifiedDate = GETDATE()
FROM Customers c
INNER JOIN StagingCustomers s ON c.CustomerID = s.CustomerID
WHERE c.Name <> s.Name
   OR c.Email <> s.Email
   OR c.Status <> s.Status;

-- Step 4: Find deleted records (soft delete)
UPDATE c
SET
    c.IsActive = 0,
    c.ModifiedDate = GETDATE()
FROM Customers c
LEFT JOIN StagingCustomers s ON c.CustomerID = s.CustomerID
WHERE s.CustomerID IS NULL
  AND c.IsActive = 1;

-- =============================================
-- Pattern 8: Incremental Load with Error Handling
-- =============================================
-- Robust pattern with logging and rollback
-- Use for: Production ETL jobs

CREATE PROCEDURE usp_IncrementalLoad_Customers
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @LoadID INT;
    DECLARE @RowsLoaded INT = 0;
    DECLARE @ErrorMessage NVARCHAR(4000);

    BEGIN TRY
        BEGIN TRANSACTION;

        -- Log start
        INSERT INTO ETL_LoadLog (TableName, LoadStartTime, Status)
        VALUES ('Customers', GETDATE(), 'Running');
        SET @LoadID = SCOPE_IDENTITY();

        -- Get watermark
        DECLARE @LastLoadDate DATETIME;
        SELECT @LastLoadDate = MAX(LoadDate) FROM Customers;
        IF @LastLoadDate IS NULL SET @LastLoadDate = '1900-01-01';

        -- Perform incremental load
        INSERT INTO Customers (CustomerID, Name, Email, ModifiedDate, LoadDate)
        SELECT
            CustomerID,
            Name,
            Email,
            ModifiedDate,
            GETDATE()
        FROM SourceCustomers
        WHERE ModifiedDate > @LastLoadDate;

        SET @RowsLoaded = @@ROWCOUNT;

        -- Log success
        UPDATE ETL_LoadLog
        SET
            LoadEndTime = GETDATE(),
            RowsLoaded = @RowsLoaded,
            Status = 'Success'
        WHERE LoadID = @LoadID;

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        -- Rollback on error
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;

        -- Log error
        SET @ErrorMessage = ERROR_MESSAGE();

        UPDATE ETL_LoadLog
        SET
            LoadEndTime = GETDATE(),
            Status = 'Failed',
            ErrorMessage = @ErrorMessage
        WHERE LoadID = @LoadID;

        -- Re-throw error
        THROW;
    END CATCH
END
GO

-- =============================================
-- Pattern 9: Parallel Incremental Loads
-- =============================================
-- Load multiple tables simultaneously
-- Use for: Overnight ETL windows, performance

-- Table 1 load (can run in parallel with others)
EXEC usp_IncrementalLoad_Customers;

-- Table 2 load
EXEC usp_IncrementalLoad_Orders;

-- Table 3 load
EXEC usp_IncrementalLoad_Products;

-- Or use SQL Agent jobs to run truly parallel

-- =============================================
-- Pattern 10: Monitoring and Alerts
-- =============================================
-- Track load performance and data freshness
-- Use for: Operations monitoring, SLA tracking

-- Data freshness check
SELECT
    TableName,
    MAX(LoadDate) AS LastLoadDate,
    DATEDIFF(hour, MAX(LoadDate), GETDATE()) AS HoursSinceLoad,
    CASE
        WHEN DATEDIFF(hour, MAX(LoadDate), GETDATE()) > 24 THEN 'Stale'
        WHEN DATEDIFF(hour, MAX(LoadDate), GETDATE()) > 12 THEN 'Warning'
        ELSE 'Fresh'
    END AS DataFreshness
FROM (
    SELECT 'Customers' AS TableName, MAX(LoadDate) AS LoadDate FROM Customers
    UNION ALL
    SELECT 'Orders', MAX(LoadDate) FROM Orders
    UNION ALL
    SELECT 'Products', MAX(LoadDate) FROM Products
) AS DataFreshness
GROUP BY TableName;

-- Load performance trend
SELECT
    TableName,
    CAST(LoadStartTime AS DATE) AS LoadDate,
    COUNT(*) AS LoadCount,
    SUM(RowsLoaded) AS TotalRowsLoaded,
    AVG(DATEDIFF(second, LoadStartTime, LoadEndTime)) AS AvgLoadTimeSeconds,
    MAX(DATEDIFF(second, LoadStartTime, LoadEndTime)) AS MaxLoadTimeSeconds
FROM ETL_LoadLog
WHERE LoadStartTime >= DATEADD(day, -30, GETDATE())
  AND Status = 'Success'
GROUP BY TableName, CAST(LoadStartTime AS DATE)
ORDER BY TableName, LoadDate DESC;

-- =============================================
-- Performance Tips
-- =============================================
-- 1. Index ModifiedDate column for efficient filtering
-- 2. Use TABLOCK hint for bulk inserts when appropriate
-- 3. Consider columnstore indexes for large fact tables
-- 4. Partition large tables by date for easier management
-- 5. Monitor transaction log size during large loads
-- 6. Use Read Committed Snapshot Isolation to reduce locking

-- =============================================
-- Best Practices
-- =============================================
-- 1. Always use transactions for atomicity
-- 2. Log every load attempt (success and failure)
-- 3. Include error handling and rollback logic
-- 4. Test incremental loads with various scenarios (empty, full, partial)
-- 5. Document watermark strategy and business rules
-- 6. Monitor data latency and load performance
-- 7. Have a process to handle late-arriving data
-- 8. Consider idempotency (safe to rerun)

-- =============================================
