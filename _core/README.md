# Data Tune Solutions - Core Library

This repository contains shared resources, reusable code patterns, and documentation for Data Tune Solutions projects.

## 📁 Repository Structure

```
data-tune-core/
├── sql-library/              # Reusable SQL patterns
│   ├── common-transforms/    # Standard data transformation queries
│   ├── data-quality-checks/  # Validation and quality assurance queries
│   └── performance-patterns/ # Optimized query patterns
├── python-utils/             # Python helper modules (future)
├── powerbi-resources/        # DAX measures, M queries, themes
├── docs/                     # Business documentation
└── project-templates/        # Templates for new projects
```

## 🎯 Purpose

This core library serves as:
- **Code Repository**: Store and version control reusable SQL, DAX, and M code
- **Knowledge Base**: Document best practices and standard approaches
- **Project Templates**: Quick-start templates for new client projects
- **Reference Material**: Connection patterns, common transformations

## 🚀 Usage

### For New Projects
1. Reference this library when starting new client work
2. Copy relevant templates from `project-templates/`
3. Adapt SQL patterns from `sql-library/` as needed
4. Use DAX measures from `powerbi-resources/`

### Adding New Patterns
When you create a useful pattern or solve a common problem:
1. Extract the generic version
2. Add it to the appropriate folder
3. Document with comments explaining usage
4. Commit with descriptive message

## 🔧 Tech Stack

- **SQL**: T-SQL (SQL Server/Azure SQL)
- **Power BI**: DAX measures, M/Power Query
- **Cloud Platforms**: Azure, BigQuery, Snowflake
- **Python**: Helper utilities (future enhancement)

## 📝 Documentation

See the `docs/` folder for:
- Business context and methodology
- Standard operating procedures
- Connection guides for various platforms
- Project setup checklists

## 🔒 Security Notes

**NEVER commit:**
- Actual credentials or connection strings
- Client data files
- `.pbix` files (use dev/prod pattern instead)
- API keys or secrets

Use `.env` files and Azure Key Vault for sensitive information.

## 🔄 Git Workflow (Once GitHub is set up)

```bash
# Initial setup
git init
git add .
git commit -m "Initial commit"

# Regular workflow
git add <changed-files>
git commit -m "Descriptive message"
git push origin main
```

## ⚠️ TODO
- [ ] Install Git if not already installed
- [ ] Set up GitHub repository and connect remote
- [ ] Configure Git user.name and user.email
- [ ] Create initial commit

