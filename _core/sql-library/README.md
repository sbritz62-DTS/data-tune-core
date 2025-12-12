# SQL Library - Data Tune Solutions

## Overview

This directory contains reusable SQL patterns and templates for common data engineering tasks. All SQL is written in T-SQL (SQL Server/Azure SQL) unless otherwise noted.

## Directory Structure

### `common-transforms/`
Standard data transformation patterns used across projects:
- Date/time transformations
- String manipulation
- Type conversions
- Aggregation patterns
- Window functions

### `data-quality-checks/`
SQL queries for validating data quality:
- Row count comparisons
- Null value detection
- Duplicate identification
- Data type validation
- Referential integrity checks
- Business rule validation

### `performance-patterns/`
Optimized query patterns for common scenarios:
- Efficient joins
- Partitioning strategies
- Index recommendations
- Incremental load patterns
- Large table handling

## Usage Guidelines

### 1. Copy and Adapt
- Copy relevant template to your project
- Customize for specific tables/columns
- Add project-specific business logic
- Keep comments explaining the logic

### 2. Testing
- Always test with sample data first
- Validate row counts before/after
- Check for edge cases
- Verify performance with production volumes

### 3. Documentation
- Add inline comments for complex logic
- Document assumptions and dependencies
- Note any platform-specific syntax
- Include example usage

## Naming Conventions

### Stored Procedures
```sql
-- Pattern: usp_<Action><Entity><Purpose>
usp_LoadCustomerData
usp_GetSalesMetrics
usp_ValidateOrderIntegrity
```

### Functions
```sql
-- Pattern: fn_<Purpose><ReturnType>
fn_GetBusinessDays  -- Returns INT
fn_ParseJsonToTable -- Returns TABLE
```

### Tables
```sql
-- Staging: stg_<SourceSystem>_<Entity>
stg_Salesforce_Accounts

-- Dimension: dim_<Entity>
dim_Customer

-- Fact: fact_<Process>
fact_Sales

-- Log: log_<Process>_<Timestamp>
log_DataLoad_20240101
```

## Common Patterns

### Template: Incremental Load
```sql
-- Load only new/changed records since last load
DECLARE @LastLoadDate DATETIME = (SELECT MAX(LoadDate) FROM Target_Table);

INSERT INTO Target_Table (Col1, Col2, LoadDate)
SELECT 
    Col1, 
    Col2,
    GETDATE() AS LoadDate
FROM Source_Table
WHERE ModifiedDate > @LastLoadDate;
```

### Template: Upsert (Merge)
```sql
MERGE INTO Target_Table AS Target
USING Source_Table AS Source
ON Target.ID = Source.ID
WHEN MATCHED THEN
    UPDATE SET 
        Target.Col1 = Source.Col1,
        Target.Col2 = Source.Col2,
        Target.UpdatedDate = GETDATE()
WHEN NOT MATCHED BY TARGET THEN
    INSERT (ID, Col1, Col2, CreatedDate)
    VALUES (Source.ID, Source.Col1, Source.Col2, GETDATE())
WHEN NOT MATCHED BY SOURCE THEN
    UPDATE SET Target.IsActive = 0;  -- Soft delete
```

### Template: Logging
```sql
-- Create log table
CREATE TABLE log_PipelineExecution (
    LogID INT IDENTITY(1,1) PRIMARY KEY,
    PipelineName VARCHAR(100),
    StartTime DATETIME,
    EndTime DATETIME,
    RowsProcessed INT,
    Status VARCHAR(20),
    ErrorMessage VARCHAR(MAX)
);

-- Log execution
DECLARE @LogID INT;
DECLARE @StartTime DATETIME = GETDATE();
DECLARE @RowsProcessed INT = 0;

BEGIN TRY
    -- Your ETL logic here
    SELECT @RowsProcessed = @@ROWCOUNT;
    
    -- Log success
    INSERT INTO log_PipelineExecution 
    VALUES ('Pipeline_Name', @StartTime, GETDATE(), @RowsProcessed, 'Success', NULL);
END TRY
BEGIN CATCH
    -- Log error
    INSERT INTO log_PipelineExecution 
    VALUES ('Pipeline_Name', @StartTime, GETDATE(), 0, 'Failed', ERROR_MESSAGE());
END CATCH
```

## Performance Tips

### Use CTEs for Readability
```sql
-- Good: Clear and maintainable
WITH FilteredData AS (
    SELECT * FROM LargeTable
    WHERE Date >= DATEADD(day, -30, GETDATE())
),
Aggregated AS (
    SELECT Category, SUM(Amount) AS Total
    FROM FilteredData
    GROUP BY Category
)
SELECT * FROM Aggregated
WHERE Total > 1000;
```

### Avoid Cursors (Use Set-Based Operations)
```sql
-- Bad: Cursor (slow)
DECLARE cursor_name CURSOR FOR SELECT ID FROM Table;
-- Loop through records...

-- Good: Set-based operation (fast)
UPDATE Target
SET Target.Value = Source.Value
FROM Target
INNER JOIN Source ON Target.ID = Source.ID;
```

### Use Appropriate Indexes
```sql
-- Create index on frequently filtered/joined columns
CREATE NONCLUSTERED INDEX IX_Customer_Date
ON Customer (CreatedDate)
INCLUDE (CustomerName, Email);
```

## Cross-Platform Notes

### BigQuery Differences
- Use \` instead of [] for identifiers
- DATE_SUB() instead of DATEADD()
- STRING_AGG() vs STRING_AGG() (different syntax)

### Snowflake Differences
- DATEADD(day, -30, CURRENT_DATE()) syntax
- Different time zone handling
- Different MERGE syntax

Store platform-specific queries in separate files with clear naming:
- `query_name_tsql.sql`
- `query_name_bigquery.sql`
- `query_name_snowflake.sql`

---

*Contribute new patterns as you develop them. Keep this library growing!*

