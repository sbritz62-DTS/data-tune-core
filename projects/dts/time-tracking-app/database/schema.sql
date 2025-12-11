-- ================================================================
-- Data Tune Solutions - Time Tracking Application
-- Database Schema Creation Script
-- ================================================================

-- Create Database (run this separately if needed)
-- CREATE DATABASE DataTuneTimeTracking;
-- GO
-- USE DataTuneTimeTracking;
-- GO

-- ================================================================
-- Drop existing objects if they exist (for re-runs)
-- ================================================================
IF OBJECT_ID('InvoiceLineItems', 'U') IS NOT NULL DROP TABLE InvoiceLineItems;
IF OBJECT_ID('Invoices', 'U') IS NOT NULL DROP TABLE Invoices;
IF OBJECT_ID('TimeEntries', 'U') IS NOT NULL DROP TABLE TimeEntries;
IF OBJECT_ID('Clients', 'U') IS NOT NULL DROP TABLE Clients;

IF OBJECT_ID('vw_WeeklyClientTotals', 'V') IS NOT NULL DROP VIEW vw_WeeklyClientTotals;
IF OBJECT_ID('vw_ActiveClients', 'V') IS NOT NULL DROP VIEW vw_ActiveClients;

IF OBJECT_ID('usp_GetUnbilledHours', 'P') IS NOT NULL DROP PROCEDURE usp_GetUnbilledHours;
IF OBJECT_ID('usp_GetWeeklyTimesheet', 'P') IS NOT NULL DROP PROCEDURE usp_GetWeeklyTimesheet;
GO

-- ================================================================
-- Table: Clients
-- Purpose: Store client information and billing rates
-- ================================================================
CREATE TABLE Clients (
    ClientID INT IDENTITY(1,1) PRIMARY KEY,
    ClientName NVARCHAR(200) NOT NULL,
    DefaultRate DECIMAL(10,2) NOT NULL,
    PaymentTerms INT NOT NULL DEFAULT 30, -- Days
    Active BIT NOT NULL DEFAULT 1,
    CreatedDate DATETIME NOT NULL DEFAULT GETDATE(),
    ModifiedDate DATETIME NOT NULL DEFAULT GETDATE(),
    CONSTRAINT CK_Clients_DefaultRate CHECK (DefaultRate >= 0),
    CONSTRAINT CK_Clients_PaymentTerms CHECK (PaymentTerms >= 0)
);

-- Index for active clients lookup
CREATE NONCLUSTERED INDEX IX_Clients_Active 
ON Clients(Active) 
INCLUDE (ClientName, DefaultRate);

-- ================================================================
-- Table: TimeEntries
-- Purpose: Store daily time entries for each client
-- ================================================================
CREATE TABLE TimeEntries (
    EntryID INT IDENTITY(1,1) PRIMARY KEY,
    ClientID INT NOT NULL,
    WeekStartDate DATE NOT NULL,
    DayOfWeek TINYINT NOT NULL, -- 1=Monday, 7=Sunday
    HoursWorked DECIMAL(5,2) NOT NULL,
    RateUsed DECIMAL(10,2) NOT NULL, -- Allows manual override
    Notes NVARCHAR(500) NULL,
    CreatedDate DATETIME NOT NULL DEFAULT GETDATE(),
    CONSTRAINT FK_TimeEntries_Clients 
        FOREIGN KEY (ClientID) REFERENCES Clients(ClientID),
    CONSTRAINT CK_TimeEntries_DayOfWeek 
        CHECK (DayOfWeek BETWEEN 1 AND 7),
    CONSTRAINT CK_TimeEntries_HoursWorked 
        CHECK (HoursWorked >= 0 AND HoursWorked <= 24)
);

-- Index for weekly time lookups
CREATE NONCLUSTERED INDEX IX_TimeEntries_WeekClient 
ON TimeEntries(WeekStartDate, ClientID) 
INCLUDE (DayOfWeek, HoursWorked, RateUsed);

-- Index for client time history
CREATE NONCLUSTERED INDEX IX_TimeEntries_ClientDate 
ON TimeEntries(ClientID, WeekStartDate DESC);

-- ================================================================
-- Table: Invoices
-- Purpose: Track generated invoices (Phase 2)
-- ================================================================
CREATE TABLE Invoices (
    InvoiceID INT IDENTITY(1,1) PRIMARY KEY,
    ClientID INT NOT NULL,
    InvoiceNumber NVARCHAR(50) NOT NULL UNIQUE,
    InvoiceDate DATE NOT NULL,
    DueDate DATE NOT NULL,
    TotalHours DECIMAL(10,2) NOT NULL,
    TotalAmount DECIMAL(12,2) NOT NULL,
    Status NVARCHAR(20) NOT NULL DEFAULT 'Draft', -- Draft, Sent, Paid, Overdue
    PDFPath NVARCHAR(500) NULL,
    Notes NVARCHAR(1000) NULL,
    CreatedDate DATETIME NOT NULL DEFAULT GETDATE(),
    ModifiedDate DATETIME NOT NULL DEFAULT GETDATE(),
    CONSTRAINT FK_Invoices_Clients 
        FOREIGN KEY (ClientID) REFERENCES Clients(ClientID),
    CONSTRAINT CK_Invoices_Status 
        CHECK (Status IN ('Draft', 'Sent', 'Paid', 'Overdue', 'Cancelled')),
    CONSTRAINT CK_Invoices_TotalHours 
        CHECK (TotalHours >= 0),
    CONSTRAINT CK_Invoices_TotalAmount 
        CHECK (TotalAmount >= 0)
);

-- Index for invoice lookups
CREATE NONCLUSTERED INDEX IX_Invoices_ClientDate 
ON Invoices(ClientID, InvoiceDate DESC);

CREATE NONCLUSTERED INDEX IX_Invoices_Status 
ON Invoices(Status, DueDate);

-- ================================================================
-- Table: InvoiceLineItems
-- Purpose: Link time entries to invoices (Phase 2)
-- ================================================================
CREATE TABLE InvoiceLineItems (
    LineItemID INT IDENTITY(1,1) PRIMARY KEY,
    InvoiceID INT NOT NULL,
    EntryID INT NULL, -- Can be NULL for manual line items
    Description NVARCHAR(500) NOT NULL,
    Hours DECIMAL(5,2) NOT NULL,
    Rate DECIMAL(10,2) NOT NULL,
    Amount DECIMAL(12,2) NOT NULL,
    CONSTRAINT FK_InvoiceLineItems_Invoices 
        FOREIGN KEY (InvoiceID) REFERENCES Invoices(InvoiceID),
    CONSTRAINT FK_InvoiceLineItems_TimeEntries 
        FOREIGN KEY (EntryID) REFERENCES TimeEntries(EntryID),
    CONSTRAINT CK_InvoiceLineItems_Hours 
        CHECK (Hours >= 0),
    CONSTRAINT CK_InvoiceLineItems_Amount 
        CHECK (Amount >= 0)
);

CREATE NONCLUSTERED INDEX IX_InvoiceLineItems_Invoice 
ON InvoiceLineItems(InvoiceID);

-- ================================================================
-- Stored Procedures
-- ================================================================
GO

-- Get weekly timesheet for display
CREATE PROCEDURE usp_GetWeeklyTimesheet
    @WeekStartDate DATE
AS
BEGIN
    SET NOCOUNT ON;
    
    SELECT 
        c.ClientID,
        c.ClientName,
        c.DefaultRate,
        te.DayOfWeek,
        ISNULL(te.HoursWorked, 0) AS HoursWorked,
        ISNULL(te.RateUsed, c.DefaultRate) AS RateUsed,
        te.Notes,
        te.EntryID
    FROM Clients c
    CROSS JOIN (SELECT 1 AS DayOfWeek UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 
                UNION SELECT 5 UNION SELECT 6 UNION SELECT 7) AS days
    LEFT JOIN TimeEntries te 
        ON c.ClientID = te.ClientID 
        AND te.WeekStartDate = @WeekStartDate
        AND te.DayOfWeek = days.DayOfWeek
    WHERE c.Active = 1
    ORDER BY c.ClientName, days.DayOfWeek;
END;
GO

-- Get unbilled time entries for a client
GO
CREATE PROCEDURE usp_GetUnbilledHours
    @ClientID INT
AS
BEGIN
    SET NOCOUNT ON;
    
    SELECT 
        te.EntryID,
        te.WeekStartDate,
        te.DayOfWeek,
        te.HoursWorked,
        te.RateUsed,
        te.Notes,
        (te.HoursWorked * te.RateUsed) AS Amount
    FROM TimeEntries te
    WHERE te.ClientID = @ClientID
        AND NOT EXISTS (
            SELECT 1 
            FROM InvoiceLineItems ili
            WHERE ili.EntryID = te.EntryID
        )
    ORDER BY te.WeekStartDate, te.DayOfWeek;
END;
GO

-- ================================================================
-- Views
-- ================================================================
GO

-- View: Active clients with current rates
CREATE VIEW vw_ActiveClients AS
SELECT 
    ClientID,
    ClientName,
    DefaultRate,
    PaymentTerms,
    CreatedDate,
    ModifiedDate
FROM Clients
WHERE Active = 1;
GO

-- View: Weekly totals by client
GO
CREATE VIEW vw_WeeklyClientTotals AS
SELECT 
    c.ClientID,
    c.ClientName,
    te.WeekStartDate,
    SUM(te.HoursWorked) AS TotalHours,
    AVG(te.RateUsed) AS AvgRate,
    SUM(te.HoursWorked * te.RateUsed) AS TotalAmount
FROM Clients c
INNER JOIN TimeEntries te ON c.ClientID = te.ClientID
GROUP BY c.ClientID, c.ClientName, te.WeekStartDate;
GO

-- ================================================================
-- Initial Setup Complete
-- ================================================================
PRINT 'Database schema created successfully!';
PRINT 'Next step: Run test-data.sql to add sample data';

