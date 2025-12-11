# Data Tune Solutions - Quick Reference Guide

## 🎯 Common Tasks

### Start a New Client Project
```powershell
cd "C:\Users\shane\Cursor Projects\projects"
mkdir client-name-project
cd client-name-project
```

Then ask Claude: *"Set up a new project for [Client Name] using our template"*

### Find SQL Patterns
- **Date transformations**: `data-tune-core/sql-library/common-transforms/date_transformations.sql`
- **Data quality checks**: `data-tune-core/sql-library/data-quality-checks/validation_queries.sql`
- **All patterns**: `data-tune-core/sql-library/README.md`

### Find DAX Measures
- **Time intelligence**: `data-tune-core/powerbi-resources/dax-measures/time-intelligence.dax`
- **Best practices**: `data-tune-core/powerbi-resources/README.md`

### Reference Documentation
- **Business context**: `data-tune-core/docs/business-context.md`
- **Standard procedures**: `data-tune-core/docs/standard-procedures.md`
- **Tech stack guide**: `data-tune-core/docs/tech-stack-guide.md`

## 💬 Working with Claude

### Ask Claude to...

**Reference Your Patterns**:
- "Use our date transformation pattern to create a fiscal calendar"
- "Write a data quality check following our standard template"
- "Create a YoY DAX measure like in our library"

**Create from Templates**:
- "Set up a new Azure SQL pipeline project for Acme Corp"
- "Create a README for the XYZ project"
- "Generate a data dictionary template"

**Add to Library**:
- "Save this SQL pattern to our common transforms library"
- "Add this DAX measure to our time intelligence collection"
- "Document this approach in our best practices"

**Get Help**:
- "What's the best way to connect to Snowflake in our stack?"
- "Show me our standard data quality checks"
- "How do we handle incremental loads?"

## 🔧 Git Commands (After Installing Git)

### Initial Setup
```powershell
# Configure Git
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Initialize data-tune-core repo
cd "C:\Users\shane\Cursor Projects\data-tune-core"
git init
git add .
git commit -m "Initial commit"
```

### Daily Usage
```powershell
# Check status
git status

# Add changes
git add .

# Commit with message
git commit -m "Added new SQL pattern for customer segmentation"

# View history
git log --oneline
```

### For Each New Project
```powershell
cd "C:\Users\shane\Cursor Projects\projects\client-project"
git init
git add .
git commit -m "Initial project setup"
```

## 📁 File Organization Rules

### ✅ DO Commit to Git
- SQL scripts (`.sql`)
- DAX measures (`.dax`)
- M queries (`.m`)
- Documentation (`.md`)
- Python scripts (`.py`)
- Configuration templates (`.template`)

### ❌ DON'T Commit
- `.pbix` files (too large, binary)
- `.env` files (contain secrets)
- Data files (`.csv`, `.xlsx`, `.parquet`)
- Credentials or connection strings
- Log files

### 💾 Dev vs Prod Pattern for Power BI
- **Development**: `ClientProject-Dev.pbix` (local, not committed)
- **Production**: Deploy to Power BI Service (not version controlled)
- **What to commit**: Extracted DAX measures as `.dax` files

## 🔍 Finding Things

### Need SQL Pattern?
1. Check `data-tune-core/sql-library/README.md` for index
2. Browse subdirectories: `common-transforms/`, `data-quality-checks/`, `performance-patterns/`
3. Ask Claude: "Show me our SQL patterns for [topic]"

### Need DAX Measure?
1. Look in `data-tune-core/powerbi-resources/dax-measures/`
2. Ask Claude: "Show me our time intelligence measures"

### Need to Understand Our Approach?
1. Read `data-tune-core/docs/business-context.md`
2. Check `data-tune-core/docs/standard-procedures.md`

## 🚀 Project Workflow

### 1. Project Start
- [ ] Create project directory in `projects/`
- [ ] Copy template structure
- [ ] Create `.env` from `.env.template`
- [ ] Initialize Git (optional)
- [ ] Document requirements

### 2. Development
- [ ] Build SQL scripts
- [ ] Create Power BI reports (dev version)
- [ ] Extract DAX measures
- [ ] Run data quality checks
- [ ] Document as you go

### 3. Testing
- [ ] Test with full data volume
- [ ] Run all quality checks
- [ ] Verify performance
- [ ] Get stakeholder approval

### 4. Deployment
- [ ] Deploy to production
- [ ] Set up scheduled refresh
- [ ] Configure monitoring
- [ ] Complete runbook
- [ ] Knowledge transfer

### 5. Maintenance
- [ ] Monitor daily refreshes
- [ ] Review quality metrics
- [ ] Update documentation
- [ ] Save reusable patterns back to core library

## 🔗 Useful Links

### Azure Resources
- Azure Portal: https://portal.azure.com
- Azure Data Factory: https://adf.azure.com
- Power BI Service: https://app.powerbi.com

### Documentation
- DAX Reference: https://dax.guide
- Power Query M: https://docs.microsoft.com/power-query
- T-SQL Reference: https://docs.microsoft.com/sql

### Learning
- SQLBI: https://sqlbi.com
- Guy in a Cube: https://youtube.com/guyinacube
- Power BI Community: https://community.powerbi.com

## 💡 Pro Tips

1. **Start with sample data** - Test your logic on small datasets first
2. **Document as you build** - Future you will thank present you
3. **Save successful patterns** - Add working code to the core library
4. **Use Claude effectively** - Reference specific files and patterns
5. **Version control everything** - Except data, credentials, and .pbix files
6. **Test incrementally** - Don't wait until the end to test
7. **Keep security in mind** - Never commit credentials

## 📞 When You Need Help

### From Claude
- "Explain how [pattern/approach] works"
- "Debug this SQL query"
- "Optimize this DAX measure"
- "Create [component] following our standards"

### From Documentation
- Check `data-tune-core/docs/` for methodology
- Review `SETUP-NEXT-STEPS.md` for setup issues
- Browse SQL and DAX libraries for examples

---

**Keep this file handy for quick reference!**

*Last updated: December 10, 2025*

