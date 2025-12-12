# Cost-Savings Cheat Sheet

## 🚨 CHECK THIS BEFORE EVERY CLAUDE PROMPT

This one-page guide will save you 70-80% on API costs. **Print it. Keep it visible. Use it every time.**

---

## ✅ The 5-Second Checklist

Before typing your prompt, ask:

```
□ Can I do this myself in <5 minutes?
  → If YES: Don't use Claude (free to DIY)

□ Have I specified EXACT file names/locations?
  → BAD: "fix the database stuff"
  → GOOD: "fix line 45 in db_helper.py"

□ Did I reference an existing pattern to follow?
  → "Use pattern from time-intelligence.dax"
  → Prevents Claude from researching/exploring

□ Did I say "execute fully, report when done"?
  → Prevents expensive back-and-forth

□ Is this ONE focused task, not multiple tasks?
  → Split into separate prompts if needed
```

**If you checked all 5:** Your prompt will be cost-efficient ✅

---

## 🎯 Perfect Prompt Template

**Copy this structure:**

```
Task: [Single, specific action]

Files: [Exact file names or "create new"]
Pattern: [Reference existing example, or "new approach"]

Execution: Plan → Approval → Execute fully → Report when complete
Style: Concise responses, code-focused

[Any other context needed]
```

**Example:**
```
Task: Add Industry field to Clients table

Files: 
- Create database/migrations/003_add_industry_field.sql
- Update src/db_helper.py (get_all_clients and save_client functions)

Pattern: Follow migration 001 format

Execution: Plan → Approval → Execute fully → Report when complete
Style: Concise
```

---

## 💰 Cost Impact by Prompt Type

| Prompt Type | Token Cost | What Happens |
|-------------|-----------|--------------|
| ❌ "Fix the app" | ~15,000 | Reads 20+ files, explores codebase |
| ❌ "Add a feature" | ~10,000 | Unclear scope, multiple iterations |
| ⚠️ "Update db_helper.py" | ~3,500 | Reads 1 large file, may need context |
| ✅ "Add field to line 45 in db_helper.py" | ~800 | Reads specific section, direct action |
| ✅ "Follow pattern from X, update Y" | ~600 | Uses reference, minimal exploration |

**The difference:** Vague prompts cost 20-25x more than specific prompts

---

## 🚫 When NOT to Use Claude (Do It Yourself - It's Free!)

Don't waste API calls on:

- ✋ Renaming files
- ✋ Copying templates
- ✋ Creating empty files/folders
- ✋ Moving files around
- ✋ Running simple Git commands (`git status`, `git add .`)
- ✋ Reading documentation (just open the file)
- ✋ Installing packages (`pip install X`)
- ✋ Simple find/replace (use Cursor's search)

**Rule:** If it takes you <5 minutes and no thinking, do it yourself.

---

## ⚠️ Claude Will Warn You When...

Claude is configured to warn before proceeding if:

- 📁 Would need to read 5+ files
- 💰 Estimated cost >3,000 tokens  
- ❓ You didn't provide file names or context
- 🔀 Task mixes 3+ unrelated changes
- 🔍 Request seems exploratory (research mode)
- 📏 Files are >500 lines without specific line numbers

**When warned:** Provide the missing details - it'll save you 40-60% in tokens.

---

## 🛑 Emergency Stop

If Claude is doing something expensive/wrong:

1. Type: **"STOP"** or **"Cancel"**
2. Claude will pause and save progress
3. You can then: Continue / Revise / Roll back / Get explanation

**Claude auto-stops if:** Plan is wrong, errors occur, or cost will be 2x+ estimate

---

## 📊 Quick Cost Math

**Your monthly limit:** [Check your Cursor plan]

**Average costs:**
- Simple task (specific prompt): ~500-1,000 tokens
- Medium task (some context needed): ~2,000-3,500 tokens
- Complex task (multiple files): ~5,000-8,000 tokens
- Exploration task (vague prompt): ~10,000-20,000 tokens

**Example budget:**
- 100K tokens/month = 100-200 specific tasks OR 15-20 vague tasks
- Be specific = 10x more tasks per month

---

## 🎓 Learning Efficiently (Without Burning Tokens)

**Expensive way:** Ask Claude to explain everything
**Smart way:** 
- Read docs first (free)
- Ask specific questions about what you don't understand
- Request examples, not full tutorials
- Batch learning: "Explain X, Y, Z" instead of 3 separate asks

---

## 💡 Pro Tips

1. **Reference your pattern library:** "Use pattern from data-tune-core/sql-library/..."
2. **Specify exact sections:** "Lines 100-150 in X file"
3. **Batch related tasks:** Do 3 small things in one session
4. **Trust approved plans:** Don't ask for confirmation at each step
5. **Use Ask Mode for research:** Agent Mode costs more
6. **Keep prompts under 100 words:** Extra words = extra cost

---

## 🔄 Before and After Examples

### ❌ EXPENSIVE (15,000+ tokens)
> "The time tracking app isn't working right, can you help?"

**Why expensive:**
- No file specified (reads entire codebase)
- No description of problem (explores everything)
- No context (asks many clarifying questions)

---

### ✅ EFFICIENT (800 tokens)
> "Fix: In src/gui_timesheet.py line 67, total calculation is wrong. Should sum Monday-Friday only, currently sums all 7 days. Execute after plan approval."

**Why efficient:**
- Exact file and line number
- Clear problem description
- Specific fix needed
- No back-and-forth required

---

## 📌 Keep This Checklist Visible

Print this section and stick it next to your monitor:

```
Before prompting Claude:

1. [ ] Can I do this myself in <5 min?
2. [ ] Did I specify exact files?
3. [ ] Did I reference a pattern?
4. [ ] Is this ONE task?
5. [ ] Did I say "execute fully"?

If all YES → Prompt is cost-efficient ✅
```

---

## 🎯 Your Goal

**Bad habit:** Treat Claude like Google search (exploratory, vague)  
**Good habit:** Treat Claude like a senior developer (specific, directed)

**The shift:** 
- From: "How do I do X?" (expensive)
- To: "Do X in file Y following pattern Z" (cheap)

---

**Remember:** Specific prompts are 10-20x cheaper than vague ones. Every minute spent crafting a clear prompt saves you hours of API budget.

---

*Keep this cheat sheet handy. Review before every task. Save 70-80% on costs.*

**Last updated:** December 12, 2025

