# DIY Task List - When NOT to Use Claude

## The Golden Rule

**If you can do it yourself in under 5 minutes with no thinking required, don't use Claude.**

Every task you do yourself = tokens saved = more capacity for complex work.

---

## 🚫 Never Use Claude For...

### 1. File Operations

**Don't use Claude:**
- ❌ Renaming files
- ❌ Moving files to different directories
- ❌ Copying files
- ❌ Creating empty files/folders
- ❌ Deleting files

**Do it yourself:**
- Windows Explorer / Mac Finder (right-click operations)
- VS Code / Cursor file explorer (drag and drop)
- PowerShell / Terminal commands

**Time cost:** 15-30 seconds  
**Token savings:** 200-500 tokens per operation

**Example:**
```powershell
# Create new directory
mkdir data-tune-core/sql-library/new-folder

# Rename file
mv old-name.sql new-name.sql

# Copy template
cp template.sql new-project.sql
```

---

### 2. Reading Documentation

**Don't use Claude:**
- ❌ "What's in the README?"
- ❌ "Show me what's in the workflow guide"
- ❌ "Read me the contents of X file"

**Do it yourself:**
- Just open and read the file (it's free!)
- Use Cursor's file search (Ctrl+P or Cmd+P)
- Browse directories in the explorer

**Time cost:** 30 seconds to 2 minutes  
**Token savings:** 500-2,000 tokens per file

**When to use Claude:** Ask for explanation of something you DON'T understand after reading it yourself.

---

### 3. Simple Git Commands

**Don't use Claude:**
- ❌ "Check git status"
- ❌ "Stage all files"
- ❌ "Show commit history"
- ❌ "Create a branch"

**Do it yourself:**
```powershell
# Check status
git status

# Stage files
git add .

# Commit
git commit -m "Your message"

# View history
git log --oneline

# Create branch
git branch feature-name
```

**Time cost:** 10 seconds  
**Token savings:** 200-400 tokens per command

**When to use Claude:** Complex git problems (merge conflicts, rebasing, recovering lost commits)

---

### 4. Installing Packages

**Don't use Claude:**
- ❌ "Install pandas"
- ❌ "Add pyodbc to requirements"
- ❌ "Update npm packages"

**Do it yourself:**
```powershell
# Python
pip install package-name

# Add to requirements.txt
echo "package-name==1.2.3" >> requirements.txt

# Node/npm
npm install package-name
```

**Time cost:** 30 seconds  
**Token savings:** 300-600 tokens

**When to use Claude:** Dependency conflicts, version compatibility issues, complex setup

---

### 5. Simple Search Operations

**Don't use Claude:**
- ❌ "Find all files with X in the name"
- ❌ "Where is function Y defined?"
- ❌ "Show me all TODO comments"

**Do it yourself:**
- Use Cursor's search (Ctrl+Shift+F or Cmd+Shift+F)
- Use file search (Ctrl+P or Cmd+P)
- Use symbol search (Ctrl+T or Cmd+T)

**Time cost:** 15-60 seconds  
**Token savings:** 500-2,000 tokens

**When to use Claude:** Understanding complex code relationships, architectural questions

---

### 6. Copy/Paste Operations

**Don't use Claude:**
- ❌ "Copy this function to another file"
- ❌ "Duplicate this block of code"
- ❌ "Move this section down"

**Do it yourself:**
- Select → Copy (Ctrl+C) → Paste (Ctrl+V)
- Drag and drop in editor
- Cut and paste (Ctrl+X, Ctrl+V)

**Time cost:** 10-20 seconds  
**Token savings:** 300-800 tokens

**When to use Claude:** Code needs modification while copying, or integration with existing code

---

### 7. Simple Text Edits

**Don't use Claude:**
- ❌ Fixing obvious typos
- ❌ Changing one variable name in one place
- ❌ Adding a single comment
- ❌ Deleting a line
- ❌ Simple find/replace

**Do it yourself:**
- Click and type
- Use Cursor's find/replace (Ctrl+H or Cmd+H)
- Multi-cursor editing (Alt+Click or Option+Click)

**Time cost:** 15-30 seconds  
**Token savings:** 200-600 tokens

**When to use Claude:** Renaming across multiple files, refactoring logic, complex changes

---

### 8. Looking Up Information

**Don't use Claude:**
- ❌ "What's the syntax for SQL JOIN?"
- ❌ "How do I write a for loop in Python?"
- ❌ "What does git rebase do?"

**Do it yourself:**
- Google it (free and instant)
- Check official docs
- Use Stack Overflow
- Reference your own documentation

**Time cost:** 1-3 minutes  
**Token savings:** 1,000-3,000 tokens

**When to use Claude:** "How does this pattern apply to MY specific codebase?" or custom implementation

---

### 9. Creating from Templates

**Don't use Claude:**
- ❌ "Create a new README from template"
- ❌ "Make a new SQL file with standard header"
- ❌ "Set up basic project structure"

**Do it yourself:**
- Copy your template files
- Rename and fill in the blanks
- Use your project-templates directory

**Time cost:** 2-3 minutes  
**Token savings:** 500-1,500 tokens

**When to use Claude:** Template needs significant customization or complex logic

---

### 10. Basic Formatting

**Don't use Claude:**
- ❌ "Add indentation"
- ❌ "Format this code"
- ❌ "Add line breaks"
- ❌ "Organize imports"

**Do it yourself:**
- Use Cursor's auto-format (Shift+Alt+F or Shift+Option+F)
- Adjust indentation with Tab/Shift+Tab
- Organize imports (built-in tool)

**Time cost:** 5-10 seconds  
**Token savings:** 200-500 tokens

**When to use Claude:** Restructuring code logic, not just formatting

---

## ✅ When You SHOULD Use Claude

Don't be too extreme - Claude is valuable for:

### Complex Tasks
- Writing new functions/logic
- Debugging non-obvious issues
- Architectural decisions
- Code refactoring
- Integration between systems

### Knowledge Work
- Understanding unfamiliar code
- Explaining complex patterns
- Best practice recommendations
- Design pattern suggestions

### Time-Intensive Tasks
- Writing boilerplate code (100+ lines)
- Creating multiple related files
- Data transformations
- Test case generation

### Quality Assurance
- Code review
- Security audit
- Performance optimization
- Error handling improvements

---

## 🎯 The 5-Minute Rule

Before asking Claude anything, ask yourself:

```
Can I do this in under 5 minutes?
        ↓
    YES → Do it yourself (save tokens)
        ↓
     NO → Will Claude save me >10 minutes?
        ↓
    YES → Use Claude (worth the tokens)
        ↓
     NO → Consider if task is really necessary
```

---

## 📊 Monthly Token Savings from DIY

Let's say you use Claude for an average project month:

### Scenario A: Using Claude for Everything

| Task | Times/Month | Tokens Each | Total |
|------|-------------|-------------|-------|
| File operations | 30 | 300 | 9,000 |
| Reading docs | 20 | 1,000 | 20,000 |
| Git commands | 25 | 300 | 7,500 |
| Package installs | 10 | 400 | 4,000 |
| Simple searches | 40 | 800 | 32,000 |
| Text edits | 50 | 400 | 20,000 |
| Formatting | 30 | 300 | 9,000 |

**Total wasted:** ~101,500 tokens/month

---

### Scenario B: DIY for Simple Tasks

| Task | Times/Month | Your Time | Tokens Saved |
|------|-------------|-----------|--------------|
| DIY file ops | 30 | 15 min | 9,000 |
| DIY read docs | 20 | 40 min | 20,000 |
| DIY git | 25 | 8 min | 7,500 |
| DIY installs | 10 | 5 min | 4,000 |
| DIY searches | 40 | 40 min | 32,000 |
| DIY edits | 50 | 25 min | 20,000 |
| DIY formatting | 30 | 5 min | 9,000 |

**Total time invested:** ~2.5 hours/month  
**Total tokens saved:** ~101,500 tokens/month  
**Result:** 101,500 extra tokens for complex work!

---

## 💡 Building Good Habits

### Week 1: Awareness
Track every time you ask Claude for something simple. Note:
- What did you ask?
- Could you have done it yourself?
- How long would it have taken you?

### Week 2-3: Practice
Consciously do simple tasks yourself:
- File operations → Windows Explorer / Finder
- Simple edits → Direct typing
- Searches → Cursor's built-in search

### Week 4+: Habit
You'll naturally:
- Reserve Claude for complex work
- Handle simple tasks without thinking
- Maximize your API budget

---

## 🔧 Tools That Are Free (Use These First)

### Built into Cursor:
- File search (Ctrl/Cmd + P)
- Text search (Ctrl/Cmd + Shift + F)
- Symbol search (Ctrl/Cmd + T)
- Find/replace (Ctrl/Cmd + H)
- Multi-cursor editing (Alt/Option + Click)
- Auto-format (Shift + Alt/Option + F)
- Git integration (built-in UI)

### Built into Your OS:
- File Explorer / Finder
- PowerShell / Terminal
- Text editors (Notepad, TextEdit)

### Online (Free):
- Google / Stack Overflow
- Official documentation sites
- GitHub search
- Regex testers

**All of these are FREE. Use them before using Claude.**

---

## 📋 Quick Reference: DIY vs Claude

Print this table:

| Task Category | DIY If... | Use Claude If... |
|---------------|-----------|------------------|
| **File operations** | Basic move/rename/copy | Need to modify multiple files with logic |
| **Reading** | Just need to see content | Need explanation/analysis |
| **Git** | Basic commands | Resolving conflicts/complex operations |
| **Search** | Finding text/files | Understanding relationships/architecture |
| **Editing** | Single line, obvious change | Logic changes, multi-file refactoring |
| **Formatting** | Spacing, indentation | Code restructuring |
| **Learning** | Syntax lookup | Applying patterns to your codebase |
| **Creating** | Copying templates | Custom implementation with logic |

---

## 🎯 Your Action Items

**This Week:**
1. Print the "5-Minute Rule" section
2. Keep it visible while working
3. Track DIY tasks for 3 days
4. Calculate tokens saved

**Next Week:**
1. Identify your most common simple tasks
2. Create keyboard shortcuts for them
3. Practice DIY until it's automatic

**Month 2:**
1. Review your token usage
2. Compare to Month 1
3. Celebrate the savings!

---

## ❓ FAQ

### "But Claude is so convenient!"

**True**, but convenience on simple tasks burns your budget fast. Save Claude for when you really need it.

**Analogy:** Don't use a taxi to walk 2 blocks. Save it for the 20-mile trip.

---

### "Won't DIY slow me down?"

**Short term:** Maybe 2-3 minutes per day  
**Long term:** No - you'll get faster, and you'll have budget for complex tasks

**Plus:** You learn the codebase better by working directly with it.

---

### "What if I'm not sure if something is 'simple'?"

**Use the 5-Minute Rule:**
- Try it yourself
- If you're stuck after 5 minutes → ask Claude
- If you complete it → you saved tokens!

Over time, you'll calibrate what's "simple" for you.

---

## ✅ Success Metrics

Track these for 1 month:

**Before DIY habits:**
- Total tokens used: ______
- Average task cost: ______
- Number of tasks: ______

**After DIY habits:**
- Total tokens used: ______ (should be lower)
- Average task cost: ______ (should be lower)
- Number of tasks: ______ (should be higher!)

**Goal:** Same or more work done with fewer tokens by handling simple tasks yourself.

---

**Bottom Line:** Every simple task you handle yourself frees up tokens for complex work where Claude really shines. Master the basics, reserve Claude for the advanced stuff.

---

*DIY isn't about avoiding Claude - it's about using Claude strategically for maximum value.*

**Last updated:** December 12, 2025

