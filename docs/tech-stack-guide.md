# Data Tune Solutions - Tech Stack Guide

## 🎯 Technology Overview

This guide documents the tools, platforms, and technologies used in Data Tune Solutions projects.

## Primary Stack

### Microsoft Azure Ecosystem

#### **Azure Data Factory (ADF)**
- **Purpose**: Orchestrate data pipelines, ETL/ELT workflows
- **Common Uses**:
  - Scheduled data extraction from source systems
  - Data transformation and loading
  - Orchestrating complex workflows
  - Integration with multiple data sources

**Best Practices**:
- Use parameterized pipelines for flexibility
- Implement proper error handling and notifications
- Log pipeline execution to monitoring tables
- Use triggers for scheduling, not manual runs

**Connection Pattern**:
```json
{
  "type": "AzureSqlDatabase",
  "connectionString": "Referenced from Azure Key Vault",
  "parameters": {
    "serverName": "@pipeline().parameters.ServerName",
    "databaseName": "@pipeline().parameters.DatabaseName"
  }
}
```

#### **Azure SQL Database**
- **Purpose**: Relational data storage, data warehouse
- **Common Uses**:
  - Staging tables for ETL
  - Data warehouse layer
  - Reporting database for Power BI

**Best Practices**:
- Use appropriate service tier for workload
- Implement indexes on join/filter columns
- Partition large tables
- Regular maintenance (stats updates, index rebuilds)

**T-SQL Patterns**:
```sql
-- Use CTEs for readability
WITH FilteredData AS (
    SELECT * FROM SourceTable
    WHERE Date >= DATEADD(day, -30, GETDATE())
),
Aggregated AS (
    SELECT 
        Category,
        SUM(Amount) AS TotalAmount
    FROM FilteredData
    GROUP BY Category
)
SELECT * FROM Aggregated;
```

#### **Azure Key Vault**
- **Purpose**: Secure storage for secrets, connection strings, API keys
- **Common Uses**:
  - Database credentials
  - API keys
  - Certificate storage

**Integration**:
- Reference in Data Factory linked services
- Access via Managed Identity
- Never hardcode secrets in code

### Power BI

#### **Power BI Desktop**
- **Purpose**: Report and dashboard development
- **Common Uses**:
  - Data modeling
  - DAX measure creation
  - Visualization development

**Best Practices**:
- Import mode for small datasets, DirectQuery for large/real-time
- Use variables in complex DAX
- Avoid calculated columns where measures work
- Disable auto date/time if not needed

**DAX Pattern Library**:
```dax
-- Year-over-Year Growth
YoY Growth = 
VAR CurrentYear = [Total Sales]
VAR PreviousYear = 
    CALCULATE(
        [Total Sales],
        DATEADD('Date'[Date], -1, YEAR)
    )
RETURN
    DIVIDE(CurrentYear - PreviousYear, PreviousYear, 0)

-- Dynamic Time Intelligence
Sales Last N Days = 
VAR DaysToInclude = 30
VAR LastDate = MAX('Date'[Date])
VAR FirstDate = LastDate - DaysToInclude
RETURN
    CALCULATE(
        [Total Sales],
        'Date'[Date] >= FirstDate && 'Date'[Date] <= LastDate
    )
```

#### **Power BI Service**
- **Purpose**: Publishing, sharing, scheduled refresh
- **Common Uses**:
  - Report distribution
  - Scheduled data refresh
  - Row-level security implementation
  - Workspace management

**Workspace Pattern**:
- Development Workspace: Testing and iteration
- Production Workspace: Live reports for users

#### **Power Query (M Language)**
- **Purpose**: Data transformation before loading to model
- **Common Uses**:
  - Data cleaning
  - Column transformations
  - Merging/appending queries
  - Custom data connectors

**M Pattern Library**:
```m
// Date table generation
let
    StartDate = #date(2020, 1, 1),
    EndDate = #date(2025, 12, 31),
    NumberOfDays = Duration.Days(EndDate - StartDate) + 1,
    DateList = List.Dates(StartDate, NumberOfDays, #duration(1, 0, 0, 0)),
    TableFromList = Table.FromList(DateList, Splitter.SplitByNothing(), {"Date"}),
    AddYear = Table.AddColumn(TableFromList, "Year", each Date.Year([Date])),
    AddMonth = Table.AddColumn(AddYear, "Month", each Date.Month([Date])),
    AddMonthName = Table.AddColumn(AddMonth, "Month Name", each Date.MonthName([Date]))
in
    AddMonthName
```

## Secondary Platforms

### Google BigQuery
- **Purpose**: Cross-cloud data integration
- **Connection Method**: Service account JSON key (stored in Key Vault)
- **Common Uses**:
  - Query data from Google Cloud
  - Integration with Azure pipelines
  - Multi-cloud reporting

**Connection Pattern**:
```python
from google.cloud import bigquery
import os

# Credentials from environment variable
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/service-account.json'
client = bigquery.Client()

query = """
    SELECT * FROM `project.dataset.table`
    WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
"""
```

### Snowflake
- **Purpose**: Cloud data warehouse integration
- **Connection Method**: User/password or key pair authentication
- **Common Uses**:
  - Access client Snowflake instances
  - Data extraction for Power BI
  - Federated queries

**Connection Pattern**:
```python
import snowflake.connector

conn = snowflake.connector.connect(
    user='username',
    password='password',
    account='account_identifier',
    warehouse='warehouse_name',
    database='database_name',
    schema='schema_name'
)
```

## Emerging Technologies

### Python
- **Purpose**: Advanced data transformations, automation
- **Planned Uses**:
  - Complex data processing
  - API integrations
  - Custom pipeline automation
  - Data quality frameworks

**Future Library Stack**:
- `pandas`: Data manipulation
- `pyodbc` / `sqlalchemy`: Database connections
- `azure-identity`: Azure authentication
- `google-cloud-bigquery`: BigQuery integration
- `snowflake-connector-python`: Snowflake integration

**Standard Project Structure**:
```
python-project/
├── requirements.txt
├── .env.template
├── src/
│   ├── __init__.py
│   ├── extractors/
│   ├── transformers/
│   └── loaders/
└── tests/
```

## Development Tools

### Version Control
- **Git**: Source control for SQL, DAX, M, Python
- **GitHub** (planned): Remote repository hosting
- **Local Git**: Current setup during initial development

### IDEs & Editors
- **Cursor**: AI-assisted development
- **Azure Data Studio**: SQL development
- **VS Code**: Python development (future)
- **Power BI Desktop**: BI development

### Data Modeling
- **Tabular Editor**: Advanced Power BI model editing
- **DAX Studio**: DAX query and optimization
- **SQL Server Management Studio**: Database management

## Connection Patterns

### Standard .env Template
```bash
# Azure SQL
AZURE_SQL_SERVER=server.database.windows.net
AZURE_SQL_DATABASE=database_name
AZURE_SQL_USERNAME=username
AZURE_SQL_PASSWORD=password

# BigQuery
GCP_PROJECT_ID=project-id
GCP_SERVICE_ACCOUNT_PATH=path/to/service-account.json

# Snowflake
SNOWFLAKE_ACCOUNT=account_identifier
SNOWFLAKE_USER=username
SNOWFLAKE_PASSWORD=password
SNOWFLAKE_WAREHOUSE=warehouse_name
SNOWFLAKE_DATABASE=database_name

# Azure Key Vault
KEY_VAULT_NAME=vault-name
KEY_VAULT_URI=https://vault-name.vault.azure.net/
```

## Performance Optimization

### SQL Optimization
- Index frequently filtered/joined columns
- Use appropriate data types (smaller when possible)
- Avoid SELECT *, specify needed columns
- Use partitioning for large tables
- Update statistics regularly

### Power BI Optimization
- Remove unused columns early in Power Query
- Use aggregations for large datasets
- Implement incremental refresh
- Optimize DAX with variables
- Monitor query performance in DAX Studio

### Pipeline Optimization
- Run pipelines incrementally (delta loads)
- Parallel processing where possible
- Optimize data movement (minimize)
- Use appropriate compute sizes
- Schedule during off-peak hours

## Security Standards

### Authentication
- Azure AD / Entra ID for Azure resources
- Service principals for automated processes
- Managed Identity where possible
- Service accounts for BigQuery/Snowflake

### Data Protection
- Encryption at rest (default in Azure)
- Encryption in transit (HTTPS/TLS)
- Row-level security in Power BI
- Column-level security in databases
- Regular access reviews

---

*Reference this guide when making technology decisions or setting up new projects.*

