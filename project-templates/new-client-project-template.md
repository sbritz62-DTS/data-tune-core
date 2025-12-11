# New Client Project Template - Data Tune Solutions

## Project Setup Checklist

### 1. Create Project Directory
```bash
cd "C:\Users\shane\Cursor Projects\projects"
mkdir client-name-project
cd client-name-project
```

### 2. Initialize Project Structure
```
client-name-project/
├── README.md                    # Project overview and documentation
├── .gitignore                   # Git ignore rules
├── .env.template                # Connection string templates
├── sql/                         # SQL scripts
│   ├── schema/                 # Table definitions
│   ├── stored-procedures/      # Stored procedures
│   ├── views/                  # View definitions
│   └── data-quality/           # Validation queries
├── powerbi/                     # Power BI resources
│   ├── dax-measures/           # Extracted DAX measures
│   ├── m-queries/              # Power Query scripts
│   └── documentation/          # Report documentation
├── docs/                        # Project documentation
│   ├── requirements.md         # Business requirements
│   ├── data-dictionary.md      # Data definitions
│   └── runbook.md              # Operations guide
└── scripts/                     # Helper scripts
    └── deployment/             # Deployment scripts
```

### 3. Initialize Git Repository
```bash
git init
git add .
git commit -m "Initial project setup for [Client Name]"
```

---

## README.md Template

```markdown
# [Client Name] - [Project Name]

## Project Overview
**Client**: [Client Name]
**Project Type**: [Data Pipeline / Power BI Dashboard / ETL Development]
**Start Date**: [Date]
**Status**: [Active / In Development / Completed]

## Business Objective
[Describe what problem this project solves]

## Data Sources
- **Source 1**: [Type] - [Connection info without credentials]
- **Source 2**: [Type] - [Connection info without credentials]

## Deliverables
- [ ] Data pipeline from [Source] to [Destination]
- [ ] Power BI dashboard with [key metrics]
- [ ] Documentation and runbook
- [ ] Knowledge transfer

## Tech Stack
- **Data Pipeline**: Azure Data Factory / SQL Stored Procedures
- **Database**: Azure SQL Database / Snowflake / BigQuery
- **Reporting**: Power BI
- **Orchestration**: [Tool]

## Data Refresh Schedule
- **Frequency**: [Daily at 6 AM EST / Hourly / On-demand]
- **Duration**: [Expected runtime]
- **Dependencies**: [Other pipelines or jobs]

## Setup Instructions

### Prerequisites
- Access to [data sources]
- Permissions for [Azure resources]
- Power BI Pro license

### Environment Variables
Copy `.env.template` to `.env` and fill in:
```bash
cp .env.template .env
# Edit .env with actual credentials (never commit this file)
```

### Deployment Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Architecture
[Brief description or link to architecture diagram]

## Key Metrics / KPIs
- [Metric 1]: [Definition]
- [Metric 2]: [Definition]

## Contacts
- **Project Owner**: [Name] - [Email]
- **Developer**: Data Tune Solutions
- **Business Stakeholder**: [Name] - [Email]

## Notes
[Any important project-specific notes]
```

---

## .gitignore Template

```gitignore
# Credentials & Secrets
.env
.env.*
*.env
secrets/
credentials.json
connection-strings.txt

# Data Files
*.csv
*.xlsx
*.xls
*.parquet
data/
!sample-data/

# Power BI
*.pbix
*.pbit

# Python
__pycache__/
venv/
*.pyc

# IDE
.vscode/
.idea/

# Logs
*.log
logs/

# Temp
temp/
tmp/
*.tmp

# Azure
local.settings.json

# OS
.DS_Store
Thumbs.db
desktop.ini
```

---

## .env.template

```bash
# Connection Strings Template
# Copy this to .env and fill in actual values
# NEVER commit the .env file

# === Azure SQL Database ===
AZURE_SQL_SERVER=server-name.database.windows.net
AZURE_SQL_DATABASE=database-name
AZURE_SQL_USERNAME=your-username
AZURE_SQL_PASSWORD=your-password

# === Azure Key Vault ===
KEY_VAULT_NAME=your-keyvault
KEY_VAULT_URI=https://your-keyvault.vault.azure.net/

# === BigQuery (if applicable) ===
GCP_PROJECT_ID=project-id
GCP_SERVICE_ACCOUNT_PATH=path/to/service-account.json

# === Snowflake (if applicable) ===
SNOWFLAKE_ACCOUNT=account.region
SNOWFLAKE_USER=username
SNOWFLAKE_PASSWORD=password
SNOWFLAKE_WAREHOUSE=warehouse-name
SNOWFLAKE_DATABASE=database-name

# === Power BI ===
POWERBI_WORKSPACE_ID=workspace-id
POWERBI_DATASET_ID=dataset-id

# === API Keys (if needed) ===
API_KEY=your-api-key
API_ENDPOINT=https://api.example.com
```

---

## docs/requirements.md Template

```markdown
# Project Requirements - [Client Name]

## Business Requirements

### Problem Statement
[What business problem are we solving?]

### Success Criteria
- [Measurable outcome 1]
- [Measurable outcome 2]

### Key Stakeholders
- **Primary**: [Name, Role]
- **Secondary**: [Name, Role]

## Functional Requirements

### Data Sources
1. **Source 1**
   - Type: [Database/API/File]
   - Location: [Connection details]
   - Refresh Frequency: [Real-time/Daily/Weekly]
   - Data Volume: [Approximate size]

### Data Transformations
1. [Transformation 1]: [Description]
2. [Transformation 2]: [Description]

### Reporting Requirements
- **Dashboard 1**: [Description]
  - Metrics: [List key metrics]
  - Filters: [List required filters]
  - Access: [Who should see this]

## Technical Requirements

### Performance
- Dashboard load time: < 5 seconds
- Data refresh: < 30 minutes
- Historical data: [Retention period]

### Security
- Row-level security: [Yes/No and details]
- Data encryption: [Requirements]
- Access control: [Who has access]

### Scalability
- Expected growth: [Data volume increase]
- User growth: [Number of users]

## Non-Functional Requirements
- Availability: [Uptime requirements]
- Support: [Support hours]
- Documentation: [Level of detail needed]

## Assumptions
- [Assumption 1]
- [Assumption 2]

## Constraints
- [Constraint 1]
- [Constraint 2]

## Out of Scope
- [Item 1]
- [Item 2]
```

---

## docs/data-dictionary.md Template

```markdown
# Data Dictionary - [Project Name]

## Table: [Table Name]
**Purpose**: [Description]
**Source**: [Source system]
**Refresh**: [Frequency]

| Column Name | Data Type | Description | Sample Values | Nullable | Notes |
|------------|-----------|-------------|---------------|----------|-------|
| CustomerID | INT | Unique customer identifier | 1001, 1002 | No | Primary Key |
| CustomerName | VARCHAR(100) | Full name | "John Doe" | No | |
| Email | VARCHAR(255) | Contact email | "john@example.com" | Yes | |
| CreatedDate | DATETIME | Account creation | 2024-01-01 | No | UTC timezone |

## Business Rules
- [Rule 1]: [Description]
- [Rule 2]: [Description]

## Relationships
- `CustomerID` → `Orders.CustomerID` (One-to-Many)

---

## Measure: [Measure Name]
**Definition**: [Business definition]
**DAX Formula**:
```dax
Total Sales = SUM(Sales[Amount])
```
**Usage**: [Where and how it's used]
```

---

## docs/runbook.md Template

```markdown
# Operations Runbook - [Project Name]

## Daily Operations

### Monitoring
- Check Power BI refresh status: [Link to workspace]
- Review data quality checks: [Location of logs]
- Monitor pipeline execution: [Azure Data Factory link]

### Scheduled Tasks
| Time | Task | Owner | Duration |
|------|------|-------|----------|
| 6:00 AM EST | Data Pipeline Run | Automated | 20 min |
| 7:00 AM EST | Power BI Refresh | Automated | 10 min |

## Troubleshooting

### Issue: Data Refresh Failed
**Symptoms**: Power BI shows old data
**Diagnosis**:
1. Check Azure Data Factory pipeline status
2. Review error logs in [location]
3. Verify source system availability

**Resolution**:
1. If source is down: Wait for source to recover, trigger manual refresh
2. If credentials expired: Update credentials in Key Vault
3. If data quality issue: Review validation logs, fix source data

### Issue: Slow Dashboard Performance
**Symptoms**: Report takes > 10 seconds to load
**Diagnosis**:
1. Run Performance Analyzer in Power BI Desktop
2. Check DAX query performance in DAX Studio
3. Review data model size

**Resolution**:
1. Optimize slow DAX measures
2. Remove unused columns/tables
3. Implement aggregations if needed

## Maintenance

### Weekly
- [ ] Review error logs
- [ ] Check data quality metrics
- [ ] Verify refresh success rate

### Monthly
- [ ] Review performance metrics
- [ ] Update documentation if changes made
- [ ] Archive old logs (keep last 90 days)

### Quarterly
- [ ] Review access permissions
- [ ] Optimize queries based on usage patterns
- [ ] Backup report definitions

## Deployment Process

### Deploying Changes
1. Test in development environment
2. Document changes
3. Get approval from stakeholder
4. Deploy to production during maintenance window
5. Verify deployment success
6. Update documentation

### Rollback Procedure
1. [Steps to rollback if deployment fails]

## Contacts

### Support Escalation
- **Level 1**: [Name] - [Email] - [Phone]
- **Level 2**: Data Tune Solutions - [Contact]
- **Level 3**: [Vendor] - [Support link]

## Change Log
| Date | Change | Changed By |
|------|--------|------------|
| 2024-01-01 | Initial deployment | Data Tune Solutions |
```

---

## Usage Instructions

1. **Copy this template** when starting a new project
2. **Customize** all bracketed placeholders [like this]
3. **Create the directory structure** as shown
4. **Initialize Git** and make initial commit
5. **Update** `.env.template` with actual connection requirements
6. **Fill in documentation** as you develop

## Next Steps After Setup

1. Document business requirements
2. Set up data source connections
3. Begin development
4. Update documentation as you build
5. Set up monitoring and alerts
6. Plan deployment and knowledge transfer

