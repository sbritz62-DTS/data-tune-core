-- ================================================================
-- Migration 001: Add Contact Information to Clients Table
-- Adds fields for contact person, email, phone, and billing address
-- ================================================================

-- Add new columns to Clients table
ALTER TABLE Clients
ADD ContactName NVARCHAR(200) NULL,
    ContactEmail NVARCHAR(255) NULL,
    ContactPhone NVARCHAR(50) NULL,
    BillingAddress NVARCHAR(1000) NULL;

GO

-- Add index on email for quick lookups
CREATE NONCLUSTERED INDEX IX_Clients_ContactEmail
ON Clients(ContactEmail)
WHERE ContactEmail IS NOT NULL;

GO

PRINT 'Migration 001 completed: Added contact fields to Clients table';

