# Python Utilities - Data Tune Solutions

## Overview

This directory will contain Python helper modules for data pipeline development. Currently set up for future use as Python capabilities are developed.

## Planned Structure

```
python-utils/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── azure_helpers.py            # Azure SDK utilities
├── bigquery_helpers.py         # BigQuery connection utilities
├── snowflake_helpers.py        # Snowflake connection utilities
├── data_quality/               # Data validation utilities
│   ├── validators.py
│   └── test_frameworks.py
└── transformers/               # Common transformation functions
    ├── date_utils.py
    └── string_utils.py
```

## Getting Started (Future)

### Setup Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Planned Capabilities

### 1. Azure Helpers
- Azure SQL connection management
- Key Vault secret retrieval
- Data Factory pipeline triggering
- Managed Identity authentication

### 2. BigQuery Helpers
- Service account authentication
- Query execution
- Data extraction to pandas
- Schema introspection

### 3. Snowflake Helpers
- Connection management
- Query execution
- Data loading utilities
- Stage management

### 4. Data Quality Framework
- Row count validation
- Null checks
- Duplicate detection
- Schema validation
- Custom business rule checks

### 5. Common Transformers
- Date parsing and formatting
- String cleaning
- Type conversions
- Standardization functions

## Usage Examples (Future)

### Azure SQL Connection
```python
from azure_helpers import get_sql_connection

# Using environment variables
conn = get_sql_connection()

# Using Key Vault
conn = get_sql_connection(use_key_vault=True)
```

### Data Quality Check
```python
from data_quality.validators import validate_row_counts

result = validate_row_counts(
    source_table='source.table',
    target_table='target.table',
    connection=conn
)

if not result.passed:
    print(f"Validation failed: {result.message}")
```

## Dependencies (Planned)

### Core Libraries
- `pandas`: Data manipulation
- `pyodbc`: SQL Server connections
- `sqlalchemy`: Database ORM
- `python-dotenv`: Environment variable management

### Cloud Connectors
- `azure-identity`: Azure authentication
- `azure-keyvault-secrets`: Key Vault access
- `google-cloud-bigquery`: BigQuery connector
- `snowflake-connector-python`: Snowflake connector

### Utilities
- `pytest`: Testing framework
- `black`: Code formatting
- `pylint`: Code linting

## Environment Variables

Create a `.env` file with:
```bash
# Azure
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
```

## Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_azure_helpers.py

# Run with coverage
pytest --cov=. tests/
```

## Contributing Notes

When adding new utilities:
1. Keep functions focused and reusable
2. Add docstrings with examples
3. Include error handling
4. Write unit tests
5. Update this README

---

*This directory is set up for future Python development. Start here when ready to add Python automation to data pipelines.*

