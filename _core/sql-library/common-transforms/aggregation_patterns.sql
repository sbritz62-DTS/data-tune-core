-- =============================================
-- Aggregation Patterns
-- Data Tune Solutions
-- =============================================
-- Common aggregation and analytical patterns
-- Platform: T-SQL (SQL Server / Azure SQL)
-- =============================================

-- =============================================
-- Pattern 1: Running Totals
-- =============================================
-- Calculate cumulative sums over time
-- Use for: Sales totals, inventory levels, account balances

SELECT
    OrderDate,
    CustomerID,
    OrderAmount,

    -- Running total by date (all customers)
    SUM(OrderAmount) OVER (
        ORDER BY OrderDate
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS RunningTotal,

    -- Running total by customer
    SUM(OrderAmount) OVER (
        PARTITION BY CustomerID
        ORDER BY OrderDate
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS CustomerRunningTotal
FROM Orders
ORDER BY CustomerID, OrderDate;

-- =============================================
-- Pattern 2: Year-Over-Year (YoY) Comparison
-- =============================================
-- Compare metrics across years
-- Use for: Sales analysis, growth tracking

WITH MonthlySales AS (
    SELECT
        YEAR(OrderDate) AS Year,
        MONTH(OrderDate) AS Month,
        SUM(OrderAmount) AS TotalSales
    FROM Orders
    GROUP BY YEAR(OrderDate), MONTH(OrderDate)
)
SELECT
    Year,
    Month,
    TotalSales AS CurrentYearSales,

    -- Previous year same month
    LAG(TotalSales, 12) OVER (ORDER BY Year, Month) AS PriorYearSales,

    -- YoY Growth Amount
    TotalSales - LAG(TotalSales, 12) OVER (ORDER BY Year, Month) AS YoYGrowth,

    -- YoY Growth Percentage
    CASE
        WHEN LAG(TotalSales, 12) OVER (ORDER BY Year, Month) > 0
        THEN ((TotalSales - LAG(TotalSales, 12) OVER (ORDER BY Year, Month))
              / LAG(TotalSales, 12) OVER (ORDER BY Year, Month)) * 100
        ELSE NULL
    END AS YoYGrowthPercent
FROM MonthlySales
ORDER BY Year, Month;

-- =============================================
-- Pattern 3: Moving Averages
-- =============================================
-- Calculate rolling averages
-- Use for: Trend analysis, smoothing data

SELECT
    OrderDate,
    OrderAmount,

    -- 7-day moving average
    AVG(OrderAmount) OVER (
        ORDER BY OrderDate
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS MovingAvg7Day,

    -- 30-day moving average
    AVG(OrderAmount) OVER (
        ORDER BY OrderDate
        ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    ) AS MovingAvg30Day,

    -- Centered moving average (3 days before and after)
    AVG(OrderAmount) OVER (
        ORDER BY OrderDate
        ROWS BETWEEN 3 PRECEDING AND 3 FOLLOWING
    ) AS CenteredMovingAvg
FROM Orders
ORDER BY OrderDate;

-- =============================================
-- Pattern 4: Ranking and Percentiles
-- =============================================
-- Rank records and calculate percentiles
-- Use for: Top performers, outlier detection

SELECT
    CustomerID,
    CustomerName,
    TotalPurchases,

    -- Simple ranking (1, 2, 3, 4...)
    ROW_NUMBER() OVER (ORDER BY TotalPurchases DESC) AS RowNum,

    -- Rank with ties (1, 2, 2, 4...)
    RANK() OVER (ORDER BY TotalPurchases DESC) AS Rank,

    -- Dense rank (1, 2, 2, 3...)
    DENSE_RANK() OVER (ORDER BY TotalPurchases DESC) AS DenseRank,

    -- Percentile (0-100)
    PERCENT_RANK() OVER (ORDER BY TotalPurchases) * 100 AS Percentile,

    -- Quartile (1-4)
    NTILE(4) OVER (ORDER BY TotalPurchases) AS Quartile,

    -- Decile (1-10)
    NTILE(10) OVER (ORDER BY TotalPurchases) AS Decile
FROM Customers
ORDER BY TotalPurchases DESC;

-- =============================================
-- Pattern 5: Top N per Group
-- =============================================
-- Find top records within each category
-- Use for: Best sellers by category, top customers by region

WITH RankedProducts AS (
    SELECT
        Category,
        ProductName,
        TotalSales,
        ROW_NUMBER() OVER (
            PARTITION BY Category
            ORDER BY TotalSales DESC
        ) AS RankInCategory
    FROM ProductSales
)
SELECT
    Category,
    ProductName,
    TotalSales,
    RankInCategory
FROM RankedProducts
WHERE RankInCategory <= 5  -- Top 5 per category
ORDER BY Category, RankInCategory;

-- =============================================
-- Pattern 6: Cumulative Distribution
-- =============================================
-- Calculate what percentage of records fall below a value
-- Use for: Understanding data distribution

SELECT
    OrderAmount,

    -- Cumulative distribution (0-1)
    CUME_DIST() OVER (ORDER BY OrderAmount) AS CumulativeDist,

    -- As percentage
    CUME_DIST() OVER (ORDER BY OrderAmount) * 100 AS CumulativePercent,

    -- Interpretation
    CONCAT(
        CAST(CUME_DIST() OVER (ORDER BY OrderAmount) * 100 AS DECIMAL(5,2)),
        '% of orders are <= $',
        CAST(OrderAmount AS VARCHAR)
    ) AS Interpretation
FROM Orders
ORDER BY OrderAmount;

-- =============================================
-- Pattern 7: First and Last Values in Group
-- =============================================
-- Get first/last values within a partition
-- Use for: Initial orders, most recent activity

SELECT
    CustomerID,
    OrderDate,
    OrderAmount,

    -- First order amount for this customer
    FIRST_VALUE(OrderAmount) OVER (
        PARTITION BY CustomerID
        ORDER BY OrderDate
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS FirstOrderAmount,

    -- Last (most recent) order amount
    LAST_VALUE(OrderAmount) OVER (
        PARTITION BY CustomerID
        ORDER BY OrderDate
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS LastOrderAmount,

    -- Days since first order
    DATEDIFF(day,
        FIRST_VALUE(OrderDate) OVER (
            PARTITION BY CustomerID
            ORDER BY OrderDate
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ),
        OrderDate
    ) AS DaysSinceFirstOrder
FROM Orders
ORDER BY CustomerID, OrderDate;

-- =============================================
-- Pattern 8: Pivot (Rows to Columns)
-- =============================================
-- Convert rows into columns
-- Use for: Cross-tabulation, matrix views

-- Example: Monthly sales by product
SELECT
    ProductName,
    [1] AS Jan, [2] AS Feb, [3] AS Mar, [4] AS Apr,
    [5] AS May, [6] AS Jun, [7] AS Jul, [8] AS Aug,
    [9] AS Sep, [10] AS Oct, [11] AS Nov, [12] AS Dec
FROM (
    SELECT
        ProductName,
        MONTH(OrderDate) AS Month,
        OrderAmount
    FROM Orders
) AS SourceData
PIVOT (
    SUM(OrderAmount)
    FOR Month IN ([1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12])
) AS PivotTable;

-- =============================================
-- Pattern 9: Unpivot (Columns to Rows)
-- =============================================
-- Convert columns into rows
-- Use for: Normalizing data, creating time series

-- Example: Convert monthly columns to rows
SELECT
    ProductName,
    Month,
    Sales
FROM MonthlySalesWide
UNPIVOT (
    Sales FOR Month IN (Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec)
) AS UnpivotTable;

-- =============================================
-- Pattern 10: RFM Analysis (Recency, Frequency, Monetary)
-- =============================================
-- Customer segmentation based on purchase behavior
-- Use for: Marketing segmentation, customer value analysis

WITH CustomerMetrics AS (
    SELECT
        CustomerID,

        -- Recency: Days since last purchase
        DATEDIFF(day, MAX(OrderDate), GETDATE()) AS Recency,

        -- Frequency: Number of orders
        COUNT(DISTINCT OrderID) AS Frequency,

        -- Monetary: Total amount spent
        SUM(OrderAmount) AS Monetary
    FROM Orders
    GROUP BY CustomerID
),
RFMScores AS (
    SELECT
        CustomerID,
        Recency,
        Frequency,
        Monetary,

        -- Score each dimension (1-5, 5 = best)
        NTILE(5) OVER (ORDER BY Recency DESC) AS R_Score,  -- Reverse: recent = high score
        NTILE(5) OVER (ORDER BY Frequency) AS F_Score,
        NTILE(5) OVER (ORDER BY Monetary) AS M_Score
    FROM CustomerMetrics
)
SELECT
    CustomerID,
    Recency,
    Frequency,
    Monetary,
    R_Score,
    F_Score,
    M_Score,

    -- Combined RFM Score
    CONCAT(R_Score, F_Score, M_Score) AS RFM_Segment,

    -- Customer Category
    CASE
        WHEN R_Score >= 4 AND F_Score >= 4 AND M_Score >= 4 THEN 'Champions'
        WHEN R_Score >= 3 AND F_Score >= 3 AND M_Score >= 3 THEN 'Loyal Customers'
        WHEN R_Score >= 4 AND F_Score <= 2 THEN 'New Customers'
        WHEN R_Score <= 2 AND F_Score >= 3 THEN 'At Risk'
        WHEN R_Score <= 2 AND F_Score <= 2 THEN 'Lost'
        ELSE 'Other'
    END AS CustomerCategory
FROM RFMScores
ORDER BY M_Score DESC, F_Score DESC, R_Score DESC;

-- =============================================
-- Usage Examples
-- =============================================

-- Example 1: Sales dashboard metrics
WITH DailySales AS (
    SELECT
        CAST(OrderDate AS DATE) AS Date,
        SUM(OrderAmount) AS DailySales
    FROM Orders
    WHERE OrderDate >= DATEADD(month, -3, GETDATE())
    GROUP BY CAST(OrderDate AS DATE)
)
SELECT
    Date,
    DailySales,
    AVG(DailySales) OVER (ORDER BY Date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS SevenDayAvg,
    SUM(DailySales) OVER (ORDER BY Date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS RunningTotal,
    PERCENT_RANK() OVER (ORDER BY DailySales) * 100 AS Percentile
FROM DailySales
ORDER BY Date DESC;

-- =============================================
-- Performance Tips
-- =============================================
-- 1. Window functions are generally faster than self-joins for running totals
-- 2. For very large tables, consider creating summary tables for common aggregations
-- 3. Index date columns and grouping columns for better performance
-- 4. Use appropriate PARTITION BY to limit the window size
-- 5. For historical analysis, consider creating materialized views or summary tables

-- =============================================
