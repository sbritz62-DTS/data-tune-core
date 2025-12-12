-- =============================================
-- String Manipulation Patterns
-- Data Tune Solutions
-- =============================================
-- Common string cleaning and formatting patterns
-- Platform: T-SQL (SQL Server / Azure SQL)
-- =============================================

-- =============================================
-- Pattern 1: Clean and Trim Text
-- =============================================
-- Removes extra whitespace, special characters
-- Use for: Names, addresses, general text cleanup

SELECT
    -- Remove leading/trailing whitespace
    LTRIM(RTRIM(DirtyText)) AS CleanText,

    -- Remove all whitespace
    REPLACE(REPLACE(REPLACE(DirtyText, ' ', ''), CHAR(9), ''), CHAR(10), '') AS NoWhitespace,

    -- Remove multiple spaces (replace with single space)
    REPLACE(REPLACE(REPLACE(DirtyText, '  ', ' '), '  ', ' '), '  ', ' ') AS SingleSpaced,

    -- Remove special characters (keep letters, numbers, spaces)
    -- Note: Adjust pattern as needed for your use case
    REPLACE(REPLACE(REPLACE(REPLACE(DirtyText, '!', ''), '@', ''), '#', ''), ' , '') AS NoSpecialChars
FROM YourTable;

-- =============================================
-- Pattern 2: Proper Case / Title Case
-- =============================================
-- Converts text to proper case (first letter uppercase)
-- Use for: Names, titles, addresses

-- Simple proper case (first character only)
SELECT
    UPPER(LEFT(Name, 1)) + LOWER(SUBSTRING(Name, 2, LEN(Name))) AS ProperCase
FROM YourTable;

-- More sophisticated: Handle multiple words
WITH CleanNames AS (
    SELECT
        CustomerID,
        LTRIM(RTRIM(LOWER(Name))) AS CleanName
    FROM Customers
)
SELECT
    CustomerID,
    -- This handles first word, but for full title case you'd need a function
    UPPER(LEFT(CleanName, 1)) + SUBSTRING(CleanName, 2, LEN(CleanName)) AS ProperCase
FROM CleanNames;

-- =============================================
-- Pattern 3: Parse Full Names
-- =============================================
-- Split "FirstName LastName" into separate columns
-- Use for: Customer names, contact names

SELECT
    FullName,

    -- Extract first name (everything before first space)
    CASE
        WHEN CHARINDEX(' ', FullName) > 0
        THEN LEFT(FullName, CHARINDEX(' ', FullName) - 1)
        ELSE FullName  -- No space found, return whole name
    END AS FirstName,

    -- Extract last name (everything after last space)
    CASE
        WHEN CHARINDEX(' ', FullName) > 0
        THEN RIGHT(FullName, LEN(FullName) - CHARINDEX(' ', REVERSE(FullName)))
        ELSE NULL  -- No space found, no last name
    END AS LastName,

    -- Extract middle name (if exists)
    CASE
        WHEN LEN(FullName) - LEN(REPLACE(FullName, ' ', '')) >= 2  -- At least 2 spaces
        THEN SUBSTRING(
            FullName,
            CHARINDEX(' ', FullName) + 1,  -- Start after first space
            CHARINDEX(' ', FullName, CHARINDEX(' ', FullName) + 1) - CHARINDEX(' ', FullName) - 1  -- Length until second space
        )
        ELSE NULL
    END AS MiddleName
FROM Contacts;

-- =============================================
-- Pattern 4: Format Phone Numbers
-- =============================================
-- Standardize phone number formats
-- Use for: Contact information cleanup

SELECT
    RawPhone,

    -- Remove all non-numeric characters
    REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(
        RawPhone, '(', ''), ')', ''), '-', ''), ' ', ''), '.', ''), '+', ''
    ) AS DigitsOnly,

    -- Format as (XXX) XXX-XXXX
    CASE
        WHEN LEN(REPLACE(REPLACE(REPLACE(REPLACE(
            RawPhone, '(', ''), ')', ''), '-', ''), ' ', '')) = 10
        THEN
            '(' + LEFT(REPLACE(REPLACE(REPLACE(REPLACE(
                RawPhone, '(', ''), ')', ''), '-', ''), ' ', ''), 3) + ') ' +
            SUBSTRING(REPLACE(REPLACE(REPLACE(REPLACE(
                RawPhone, '(', ''), ')', ''), '-', ''), ' ', ''), 4, 3) + '-' +
            RIGHT(REPLACE(REPLACE(REPLACE(REPLACE(
                RawPhone, '(', ''), ')', ''), '-', ''), ' ', ''), 4)
        ELSE RawPhone  -- Invalid length, return as-is
    END AS FormattedPhone
FROM Contacts;

-- =============================================
-- Pattern 5: Email Validation & Cleanup
-- =============================================
-- Basic email cleaning and validation
-- Use for: Contact information, user accounts

SELECT
    Email,

    -- Convert to lowercase (standard practice)
    LOWER(LTRIM(RTRIM(Email))) AS CleanEmail,

    -- Basic validation: has @ and . after @
    CASE
        WHEN Email LIKE '%_@_%_.__%'
        THEN 1  -- Valid format
        ELSE 0  -- Invalid format
    END AS IsValidFormat,

    -- Extract domain
    CASE
        WHEN CHARINDEX('@', Email) > 0
        THEN RIGHT(Email, LEN(Email) - CHARINDEX('@', Email))
        ELSE NULL
    END AS Domain,

    -- Extract username (before @)
    CASE
        WHEN CHARINDEX('@', Email) > 0
        THEN LEFT(Email, CHARINDEX('@', Email) - 1)
        ELSE NULL
    END AS Username
FROM Contacts;

-- =============================================
-- Pattern 6: Address Cleaning
-- =============================================
-- Standardize address formats
-- Use for: Mailing addresses, shipping addresses

SELECT
    Address,

    -- Standardize common abbreviations
    REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(
        Address,
        ' Street', ' St'),
        ' Avenue', ' Ave'),
        ' Boulevard', ' Blvd'),
        ' Road', ' Rd'),
        ' Drive', ' Dr'
    ) AS StandardizedAddress,

    -- Remove apartment/suite info (extract to separate column)
    CASE
        WHEN Address LIKE '%Apt%' OR Address LIKE '%Suite%' OR Address LIKE '%#%'
        THEN LEFT(Address,
            CASE
                WHEN CHARINDEX('Apt', Address) > 0 THEN CHARINDEX('Apt', Address) - 1
                WHEN CHARINDEX('Suite', Address) > 0 THEN CHARINDEX('Suite', Address) - 1
                WHEN CHARINDEX('#', Address) > 0 THEN CHARINDEX('#', Address) - 1
                ELSE LEN(Address)
            END
        )
        ELSE Address
    END AS StreetAddress,

    -- Extract apartment/suite number
    CASE
        WHEN Address LIKE '%Apt%'
        THEN LTRIM(RIGHT(Address, LEN(Address) - CHARINDEX('Apt', Address) - 2))
        WHEN Address LIKE '%Suite%'
        THEN LTRIM(RIGHT(Address, LEN(Address) - CHARINDEX('Suite', Address) - 4))
        WHEN Address LIKE '%#%'
        THEN LTRIM(RIGHT(Address, LEN(Address) - CHARINDEX('#', Address)))
        ELSE NULL
    END AS ApartmentNumber
FROM Addresses;

-- =============================================
-- Pattern 7: Concatenate with Null Handling
-- =============================================
-- Safely combine fields even when some are NULL
-- Use for: Creating full names, full addresses, etc.

SELECT
    -- Traditional way (NULL breaks the entire string)
    FirstName + ' ' + MiddleName + ' ' + LastName AS TraditionalConcat,  -- NULL if any part is NULL

    -- Safe way using CONCAT (ignores NULLs)
    CONCAT(FirstName, ' ', MiddleName, ' ', LastName) AS SafeConcat,

    -- With separators only when needed (CONCAT_WS)
    CONCAT_WS(' ', FirstName, MiddleName, LastName) AS BestConcat,  -- Skips NULL, no extra spaces

    -- Full address example
    CONCAT_WS(', ',
        StreetAddress,
        CONCAT_WS(' ', City, State, ZipCode)
    ) AS FullAddress
FROM Contacts;

-- =============================================
-- Pattern 8: String Comparison (Fuzzy Matching)
-- =============================================
-- Find similar strings (useful for duplicate detection)
-- Use for: Matching customer names, addresses

-- SOUNDEX: Phonetic matching
SELECT
    Name1,
    Name2,
    SOUNDEX(Name1) AS Soundex1,
    SOUNDEX(Name2) AS Soundex2,
    CASE
        WHEN SOUNDEX(Name1) = SOUNDEX(Name2) THEN 'Potential Match'
        ELSE 'Different'
    END AS PhoneticMatch
FROM Names;

-- DIFFERENCE: Soundex similarity score (0-4, 4 = most similar)
SELECT
    Name1,
    Name2,
    DIFFERENCE(Name1, Name2) AS SimilarityScore,  -- 4 = very similar, 0 = very different
    CASE
        WHEN DIFFERENCE(Name1, Name2) >= 3 THEN 'Likely Match'
        WHEN DIFFERENCE(Name1, Name2) = 2 THEN 'Possible Match'
        ELSE 'No Match'
    END AS MatchCategory
FROM Names;

-- =============================================
-- Usage Examples
-- =============================================

-- Example 1: Clean customer names
SELECT
    CustomerID,
    CONCAT_WS(' ',
        UPPER(LEFT(LTRIM(RTRIM(FirstName)), 1)) + LOWER(SUBSTRING(LTRIM(RTRIM(FirstName)), 2, LEN(FirstName))),
        UPPER(LEFT(LTRIM(RTRIM(LastName)), 1)) + LOWER(SUBSTRING(LTRIM(RTRIM(LastName)), 2, LEN(LastName)))
    ) AS CleanFullName
FROM Customers;

-- Example 2: Standardize phone numbers
UPDATE Contacts
SET Phone = '(' + LEFT(REPLACE(REPLACE(REPLACE(Phone, '(', ''), ')', ''), '-', ''), 3) + ') ' +
            SUBSTRING(REPLACE(REPLACE(REPLACE(Phone, '(', ''), ')', ''), '-', ''), 4, 3) + '-' +
            RIGHT(REPLACE(REPLACE(REPLACE(Phone, '(', ''), ')', ''), '-', ''), 4)
WHERE LEN(REPLACE(REPLACE(REPLACE(Phone, '(', ''), ')', ''), '-', '')) = 10;

-- Example 3: Find potential duplicate customers by name
SELECT
    a.CustomerID AS CustomerID1,
    b.CustomerID AS CustomerID2,
    a.CustomerName,
    b.CustomerName,
    DIFFERENCE(a.CustomerName, b.CustomerName) AS SimilarityScore
FROM Customers a
CROSS JOIN Customers b
WHERE a.CustomerID < b.CustomerID  -- Avoid duplicate pairs
  AND DIFFERENCE(a.CustomerName, b.CustomerName) >= 3;  -- High similarity

-- =============================================
-- Performance Tips
-- =============================================
-- 1. For large tables, create computed persisted columns for frequently used transformations
-- 2. Index cleaned/standardized values for faster lookups
-- 3. Consider creating functions for reusable patterns
-- 4. Use VARCHAR instead of NVARCHAR if you don't need Unicode support (saves space)

-- =============================================
