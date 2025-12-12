# Data Tune Solutions - Workspace

Welcome to the Data Tune Solutions workspace! This is the central hub for all client projects, reusable patterns, documentation, and tools.

## 📁 Workspace Structure

```
Cursor Projects/
├── .cursorrules              ← MASTER rules (applies to all work)
├── .gitignore                ← Global git ignores
├── README.md                 ← This file
│
├── _core/                    ← Shared resources for all projects
│   ├── docs/                 ← Workflow guides, best practices, cost optimization
│   ├── sql-library/          ← Reusable SQL patterns and queries
│   ├── powerbi-resources/    ← DAX measures, Power BI templates
│   ├── python-utils/         ← Reusable Python scripts and utilities
│   └── templates/            ← Templates for new clients/projects
│
├── clients/                  ← All client work organized by client
│   ├── dts/                  ← Data Tune Solutions (internal projects)
│   │   ├── .cursorrules      ← DTS-specific rules
│   │   ├── README.md
│   │   └── time-tracking-app/   ← Individual projects
│   │
│   ├── 2ndcity/              ← Client: 2nd City
│   ├── zmc/                  ← Client: ZMC
│   ├── wci/                  ← Client: WCI
│   ├── inpro/                ← Client: InPro
│   └── purewafer/            ← Client: PureWafer
│
└── tasks/
    └── todo.md               ← Global task tracking
```

## 🎯 Getting Started

### For New Projects

1. **Create project folder:**
   ```
   clients/[client-name]/[project-name]/
   ```

2. **Copy templates:**
   - Copy `_core/templates/.cursorrules.project.template` → `.cursorrules` (customize)
   - Copy `_core/templates/README.project.template` → `README.md` (customize)

3. **Create project files:**
   - `src/` - Source code, scripts
   - `database/` - SQL scripts, migrations
   - `reports/` - Power BI files, dashboards
   - `docs/` - Additional documentation

### For New Clients

1. **Folder already created** in `clients/[client-name]/`
2. **Customize client files:**
   - Edit `clients/[client-name]/.cursorrules`
   - Edit `clients/[client-name]/README.md`
3. **Start projects** under that client folder

## 📚 Documentation

### Core Guides
- **[Cost Savings Cheat Sheet](/_core/docs/cost-savings-cheat-sheet.md)** - Quick reference for efficient AI prompting (70-80% savings!)
- **[Claude Workflow Guide](/_core/docs/claude-workflow-guide.md)** - Complete workflow process with self-critique
- **[Cost Reality Check](/_core/docs/cost-reality-check.md)** - Token economics and budget planning

### Safety & Optimization
- **[Warning System Guide](/_core/docs/warning-system-guide.md)** - How Claude protects your API budget
- **[DIY Task List](/_core/docs/diy-task-list.md)** - Tasks to handle yourself (save tokens!)
- **[Emergency Stop Protocol](/_core/docs/emergency-stop-protocol.md)** - How to stop/recover mid-task

### Standards & Best Practices
- **[Business Context](/_core/docs/business-context.md)** - Company philosophy and approach
- **[Tech Stack Guide](/_core/docs/tech-stack-guide.md)** - Azure, Power BI, SQL Server patterns
- **[Standard Procedures](/_core/docs/standard-procedures.md)** - Development workflows
- **[Quick Reference](/_core/QUICK-REFERENCE.md)** - Common tasks and commands

## 🔄 The Workflow

Every task follows this proven process:

### Phase 1: Planning
- Analyze the problem
- Create a detailed plan
- **Self-critique** the plan (cost, risks, scope)
- Get your approval

### Phase 2: Execution
- Work silently (no updates unless blocked)
- Batch operations to minimize API calls
- Keep changes simple and focused

### Phase 3: Review
- Comprehensive summary of changes
- Files created/modified list
- Actual token usage reported
- Important notes and learnings

## 💰 Cost Optimization

**Key Principles:**
- ✅ Always self-critique plans before starting
- ✅ Warn if task will cost >3,000 tokens or need 5+ files
- ✅ Use batch operations (group related changes)
- ✅ Reference existing patterns (sql-library, powerbi-resources)
- ✅ Execute silently after approval (no step-by-step updates)

**Result:** 70-80% reduction in API usage compared to typical prompting

## 🗂️ Using the Cascading .cursorrules

### 3-Level Hierarchy

**Level 1: Master** (Root `.cursorrules`)
- Core workflow, self-critique, cost optimization
- Applies to all work in the workspace

**Level 2: Client** (`clients/[client-name]/.cursorrules`)
- Imports master rules
- Adds client-specific preferences, tech stack, standards
- Applies to all projects under that client

**Level 3: Project** (`clients/[client-name]/[project-name]/.cursorrules`)
- Imports client rules
- Adds project-specific context and requirements
- Applies only to that specific project

### How It Works

- When you open the workspace root, Claude reads the master `.cursorrules`
- When you open a project folder, Claude reads that project's `.cursorrules` (which references the client and master rules)
- Each level adds context without duplicating information

## 📊 Templates Available

All templates are in `_core/templates/`:

- `.cursorrules.client.template` - Copy to new client folder
- `.cursorrules.project.template` - Copy to new project folder
- `README.client.template` - Client overview template
- `README.project.template` - Project documentation template

## 🚀 Quick Reference Commands

### Git Operations
```powershell
# Check status
git status

# Stage and commit
git add .
git commit -m "Descriptive message"

# View history
git log --oneline
```

### Creating a New Project
```powershell
# Navigate to client folder
cd clients/[client-name]/

# Create project folder
mkdir [project-name]
cd [project-name]

# Copy templates
copy ...\..\..\_core\templates\.cursorrules.project.template .cursorrules
copy ...\..\..\_core\templates\README.project.template README.md

# Edit files with your project info
```

## 📞 Getting Help

1. **Workflow questions?** See `_core/docs/claude-workflow-guide.md`
2. **Cost concerns?** See `_core/docs/cost-savings-cheat-sheet.md`
3. **Technical patterns?** See `_core/sql-library/`, `_core/powerbi-resources/`
4. **Client-specific info?** See `clients/[client-name]/README.md`
5. **Project status?** See `tasks/todo.md`

## 💡 Best Practices

### Before Starting Any Task
1. ✅ Check the cost-savings cheat sheet
2. ✅ Be specific about files and requirements
3. ✅ Reference existing patterns
4. ✅ Say "execute fully, report when done"

### When Prompting Claude
- Be specific (file names, line numbers, exact requirements)
- Reference patterns (use existing code as examples)
- Batch related changes together
- Ask for cost estimate if unsure

### Rate Limit Prevention
- Batch operations (5-10 related changes in one prompt)
- Use cascading .cursorrules (avoids re-context)
- Reference existing docs (don't re-read everything)
- Pause between major batches (let rate limits reset)

## 📈 Workspace Metrics

Track these to measure efficiency:

- **Tokens per task:** Should decrease over time (goal: <2,000)
- **Tasks per month:** Should increase as you get faster
- **Warnings received:** Should decrease as you learn to prompt better
- **Projects completed:** Should steadily grow

## 🔐 Security & Privacy

### What's Committed to Git
- ✅ Source code (.sql, .py, .dax, .m files)
- ✅ Documentation (.md files)
- ✅ Configuration templates
- ✅ Project structure and organization

### What's NOT Committed
- ❌ `.env` files (use `.env.template` instead)
- ❌ Actual client data (.csv, .xlsx, .parquet)
- ❌ `.pbix` files (use dev/prod pattern)
- ❌ Credentials or connection strings

## 🔄 Maintenance

### Regular Tasks
- Weekly: Review `tasks/todo.md` for completion
- Monthly: Check `_core/` for new reusable patterns
- Monthly: Audit `.cursorrules` files for updates needed
- Quarterly: Review client documentation for accuracy

### Updating .cursorrules
When you improve your workflow or find new patterns:
1. Update the relevant `.cursorrules` file
2. Document the change in a git commit
3. Notify affected clients if policy changes

## 📝 Documentation Standards

All projects should have:
- ✅ `README.md` - What the project does, how to use it
- ✅ `.cursorrules` - Project context and requirements
- ✅ Inline code comments - Explain complex logic
- ✅ Change log - Track updates and improvements

## 🎓 Learning Resources

### Data Engineering
- [SQLBI](https://sqlbi.com) - DAX and Power BI patterns
- [Guy in a Cube](https://youtube.com/guyinacube) - Power BI tutorials
- [Microsoft Learn](https://docs.microsoft.com) - Official Azure documentation

### Tools & Platforms
- [Azure Portal](https://portal.azure.com) - Cloud resources
- [Power BI Service](https://app.powerbi.com) - BI platform
- [DAX Guide](https://dax.guide) - DAX function reference

---

## 📊 Workspace Status

**Last Updated:** December 12, 2025  
**Clients Active:** 6 (DTS + 5 external)  
**Projects:** 1 (time-tracking-app)  
**Reusable Patterns:** See `_core/sql-library/` and `_core/powerbi-resources/`

**Next Steps:**
- Customize client `.cursorrules` files as work begins
- Add projects under appropriate client folders
- Build pattern library as you complete client work
- Track improvements in token efficiency

---

**Welcome to Data Tune Solutions! Build great data solutions, efficiently.** ✨


