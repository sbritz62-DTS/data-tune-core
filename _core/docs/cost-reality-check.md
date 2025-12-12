# Cost Reality Check - Understanding API Token Economics

## What This Guide Does

Provides real numbers so you understand **exactly** what costs what, helping you make informed decisions about when and how to use Claude.

---

## 💰 Token Basics

### What is a Token?

- Tokens are how AI usage is measured
- Roughly: 1 token ≈ 4 characters (or 0.75 words)
- Both your prompts AND Claude's responses count
- Reading files also counts as tokens

### Simple Math

```
100 tokens ≈ 75 words ≈ 1 paragraph
1,000 tokens ≈ 750 words ≈ 1 page of text
10,000 tokens ≈ 7,500 words ≈ 10 pages of text
```

---

## 📊 Real Cost Examples (Actual Tasks)

### Example 1: Simple File Edit ✅ LOW COST

**Task:** "Add ContactPhone field to line 15 in db_helper.py"

**What Happens:**
1. Claude reads db_helper.py (~200 lines) = ~800 tokens
2. Creates plan and self-critique = ~300 tokens
3. You approve (your message) = ~20 tokens
4. Claude makes the edit = ~150 tokens
5. Claude reports completion = ~200 tokens

**Total Cost:** ~1,470 tokens

---

### Example 2: Pattern-Following Task ✅ LOW COST

**Task:** "Create new DAX measure for YTD Sales following pattern in time-intelligence.dax"

**What Happens:**
1. Claude reads time-intelligence.dax (~50 lines) = ~400 tokens
2. Creates plan with self-critique = ~250 tokens
3. You approve = ~20 tokens
4. Claude creates new measure = ~100 tokens
5. Claude reports = ~150 tokens

**Total Cost:** ~920 tokens

---

### Example 3: Multi-File Update ⚠️ MEDIUM COST

**Task:** "Add Industry field to Clients table - update schema, migration, and db_helper.py"

**What Happens:**
1. Claude reads 3 existing files (~600 lines total) = ~2,400 tokens
2. Creates detailed plan with self-critique = ~500 tokens
3. You approve = ~30 tokens
4. Claude creates migration file = ~200 tokens
5. Claude updates db_helper.py = ~300 tokens
6. Claude reports with summary = ~400 tokens

**Total Cost:** ~3,830 tokens

---

### Example 4: Vague Exploration ❌ HIGH COST

**Task:** "Fix the bug in the app"

**What Happens:**
1. Claude asks clarifying questions = ~200 tokens
2. You respond with partial info = ~100 tokens
3. Claude reads 5 potential files (~2,000 lines) = ~8,000 tokens
4. Claude explores codebase patterns = ~2,000 tokens
5. Claude asks more questions = ~300 tokens
6. You provide more details = ~150 tokens
7. Claude reads 3 more files = ~4,000 tokens
8. Claude finally identifies issue = ~500 tokens
9. Creates plan = ~400 tokens
10. You approve = ~20 tokens
11. Makes fix = ~200 tokens
12. Reports completion = ~300 tokens

**Total Cost:** ~16,170 tokens (11x more expensive than Example 1!)

---

### Example 5: Research/Learning ❌ HIGH COST

**Task:** "How does data validation work in our app?"

**What Happens:**
1. Claude reads entire codebase searching for patterns = ~12,000 tokens
2. Claude reads validation-related files in detail = ~5,000 tokens
3. Claude analyzes patterns and connections = ~3,000 tokens
4. Claude writes comprehensive explanation = ~2,000 tokens

**Total Cost:** ~22,000 tokens

**Better approach (200 tokens):**
- You search codebase first (free)
- You find the validation file
- Ask: "Explain the validation logic in lines 50-100 of validators.py"

---

## 📈 Cost Breakdown by Activity

### File Reading Costs

| File Size | Approximate Token Cost |
|-----------|----------------------|
| Small (50 lines) | ~400 tokens |
| Medium (200 lines) | ~1,500 tokens |
| Large (500 lines) | ~3,500 tokens |
| Very Large (1000+ lines) | ~7,000+ tokens |

**Multiplier:** Reading 5 files = 5x the cost

**Cost-saving tip:** Specify line numbers when possible
- "Read lines 100-150" = ~400 tokens instead of ~1,500 tokens

---

### Conversation Costs

| Activity | Token Cost |
|----------|-----------|
| Your simple prompt (1 sentence) | ~20-50 tokens |
| Your detailed prompt (1 paragraph) | ~100-150 tokens |
| Claude's plan (simple task) | ~200-300 tokens |
| Claude's plan (complex task) | ~500-800 tokens |
| Claude's self-critique | ~150-400 tokens |
| Your approval message | ~10-30 tokens |
| Claude's progress update | ~100-200 tokens |
| Claude's final review (simple) | ~200-400 tokens |
| Claude's final review (complex) | ~500-800 tokens |
| Back-and-forth clarification (each round) | ~200-500 tokens |

---

### Code Generation Costs

| Task | Token Cost |
|------|-----------|
| Simple function (10-20 lines) | ~150-250 tokens |
| Medium function (50 lines) | ~400-600 tokens |
| Full file (200 lines) | ~1,500-2,000 tokens |
| SQL migration script | ~200-400 tokens |
| DAX measure | ~100-200 tokens |

---

## 🎯 Cost Comparison: Good vs. Bad Prompts

### Scenario: Add Email Validation

#### ❌ BAD PROMPT (Cost: ~8,500 tokens)
> "I need email validation"

**What Happens:**
- Reads entire GUI codebase (5 files, ~2,500 lines) = ~6,000 tokens
- Asks: "Which form needs validation?" = ~150 tokens
- You respond = ~50 tokens
- Reads form files again = ~1,500 tokens
- Creates plan = ~300 tokens
- Implements = ~300 tokens
- Reports = ~200 tokens

**Total:** ~8,500 tokens

---

#### ✅ GOOD PROMPT (Cost: ~1,100 tokens)
> "Add email validation to ContactEmail field in src/gui_clients.py line 67. Use regex pattern similar to existing validation on line 45."

**What Happens:**
- Reads gui_clients.py lines 40-75 = ~300 tokens
- Creates plan = ~200 tokens
- You approve = ~20 tokens
- Implements validation = ~150 tokens
- Tests = ~100 tokens
- Reports = ~200 tokens

**Total:** ~970 tokens

**Savings:** 87% cheaper! (~7,530 tokens saved)

---

## 📊 Monthly Budget Planning

### Understanding Your Limits

Most Cursor plans have token limits. Check your plan, then use this guide:

#### If you have 100,000 tokens/month:

**Vague Prompt Strategy:**
- Average cost: ~10,000 tokens/task
- **You can do:** ~10 tasks/month
- ⚠️ Run out quickly

**Specific Prompt Strategy:**
- Average cost: ~1,000 tokens/task
- **You can do:** ~100 tasks/month
- ✅ Lasts all month

**10x difference just from prompt quality!**

---

#### If you have 500,000 tokens/month:

**Vague Prompt Strategy:**
- ~50 tasks/month
- Still runs out if you're doing daily work

**Specific Prompt Strategy:**
- ~500 tasks/month
- ~20-25 tasks per workday
- ✅ Sustainable for heavy usage

---

### Weekly Budget Tracking

Keep a simple log:

```
Week 1:
- Mon: 3 tasks, ~3,500 tokens
- Tue: 5 tasks, ~6,200 tokens
- Wed: 2 tasks, ~2,100 tokens
...

Week total: ~15,000 tokens
Monthly pace: ~60,000 tokens (under budget ✅)
```

If you're on track to exceed limits, apply cost-saving strategies more strictly.

---

## 🚨 Hidden Costs to Avoid

### 1. **Re-reading Files**

**Scenario:** You ask Claude about a file, then ask another question about the same file.

**Cost:** Claude might re-read the entire file again = 2x cost

**Fix:** Batch questions: "In file X, explain Y and also show me Z"

---

### 2. **Exploring Without Direction**

**Scenario:** "Show me what we have for data validation"

**Cost:** Reads 10+ files to find all validation code = ~20,000 tokens

**Fix:** You search first (free), then: "Explain validation pattern in validators.py"

---

### 3. **Iterative Clarifications**

**Scenario:**
1. You: "Add a field" (vague)
2. Claude: "Which field, which table?" 
3. You: "Email field"
4. Claude: "Which table?"
5. You: "Clients table"
6. Claude: "Data type?"
...and so on

**Cost:** ~500 tokens per round, 5 rounds = ~2,500 tokens wasted

**Fix:** Give all details upfront: "Add Email VARCHAR(100) to Clients table"

---

### 4. **Mode Mismatch**

**Ask Mode:** Read-only, cheaper for research
**Agent Mode:** Can edit files, costs more

**Mistake:** Using Agent Mode when you just need an answer

**Fix:** 
- Research/learning → Ask Mode
- Implementation → Agent Mode

---

### 5. **Large File Operations**

**Scenario:** "Update the main app file" (file is 1,200 lines)

**Cost:** Reading = ~8,000 tokens, editing = ~2,000 tokens = ~10,000 tokens

**Fix:** "Update lines 450-475 in main app file" = ~1,500 tokens

---

## 💡 Cost-Saving Strategies Summary

### Strategy 1: Be Specific (Saves 70-80%)
- Name exact files
- Give line numbers
- Reference patterns
- Describe exact change needed

### Strategy 2: Batch Operations (Saves 40-50%)
- Do 3 related tasks in one prompt
- Ask multiple questions about same file at once
- Plan weekly work, execute in batches

### Strategy 3: Use Patterns (Saves 50-60%)
- Reference your pattern library
- "Follow example X" prevents research
- Build reusable templates

### Strategy 4: Reduce Back-and-Forth (Saves 30-40%)
- Give complete context upfront
- Trust approved plans
- Skip progress updates

### Strategy 5: Do Simple Tasks Yourself (Saves 100%)
- File renames, moves, simple edits
- If it takes you <5 minutes, don't use Claude

---

## 📈 Measuring Your Improvement

### Track Your Average Task Cost

**Week 1 (before optimization):**
- 20 tasks
- 180,000 tokens used
- **Average: 9,000 tokens/task**

**Week 4 (after using these guides):**
- 50 tasks
- 75,000 tokens used
- **Average: 1,500 tokens/task**

**Result:** 6x more productive, 58% less token usage

---

## 🎓 The Learning Curve

### Phase 1: Learning (Expensive)
- First 2-3 weeks using Claude
- Average: ~5,000 tokens/task
- You're learning what works

### Phase 2: Improving (Medium Cost)
- Weeks 4-8
- Average: ~2,500 tokens/task
- You're getting more specific

### Phase 3: Expert (Cheap)
- After 2 months
- Average: ~1,000 tokens/task
- You know exactly how to prompt

**Don't be discouraged if early tasks are expensive - you're investing in skills that will save you long-term.**

---

## 🔍 Real Example: Time Tracking App Project

Let's break down actual token usage from your time tracking app development:

### Phase 1: Database Setup (Efficient)
- Created schema, migrations, helper files
- **Estimated tokens:** ~5,000
- **Why efficient:** Clear requirements, specific files

### Phase 2: GUI Development (Medium)
- Built client management, timesheet screens
- **Estimated tokens:** ~12,000
- **Why medium:** Some exploration needed for UI patterns

### Phase 3: UI/UX Improvements (Efficient)
- Dark theme, contact fields, navigation redesign
- **Estimated tokens:** ~8,000
- **Why efficient:** Referenced existing patterns, specific changes

**Total Project:** ~25,000 tokens for a complete application

**If done with vague prompts:** Could have easily been 100,000+ tokens

**Savings:** 75% by being specific and following patterns

---

## ✅ Quick Reference: Is This Cost Worth It?

Before each task, ask:

| Question | If YES | If NO |
|----------|--------|-------|
| Will this save me >30 minutes? | Worth it ✅ | Skip it ❌ |
| Do I need code written? | Worth it ✅ | DIY ❌ |
| Is this complex/unfamiliar? | Worth it ✅ | Try yourself first ⚠️ |
| Can I be very specific? | Worth it ✅ | Clarify first ⚠️ |
| Have I used my DIY options? | Worth it ✅ | Do simpler stuff first ❌ |

---

## 🎯 Your Action Items

1. **Check your plan:** Look up your Cursor token limits
2. **Calculate capacity:** Divide limit by 1,500 = number of specific tasks
3. **Track usage:** Note tokens used per task for 1 week
4. **Optimize prompts:** Use cheat sheet to improve
5. **Measure improvement:** Compare week 1 vs. week 4

---

**Bottom Line:** Specific prompts with file names and pattern references are 10-20x cheaper than vague exploratory prompts. Small effort in crafting prompts = massive savings.

---

*Use this guide to understand the economics of AI assistance. Make informed decisions. Maximize your API budget.*

**Last updated:** December 12, 2025

