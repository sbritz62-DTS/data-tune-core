# Warning System Guide - Cost Protection Built In

## Overview

Claude is configured to **proactively warn you** when a prompt will be expensive or inefficient. This guide explains how the warning system works and what to do when you see a warning.

---

## 🚨 When Claude Will Warn You

Claude automatically checks every prompt against these triggers:

### Trigger 1: Multiple Files (5+ files)

**What triggers it:**
- Your prompt doesn't specify files, requiring Claude to search/read many files
- Your prompt mentions multiple components across the codebase
- Task requires reading >5 files to complete

**Example prompt that triggers:**
> "Add validation to all the forms"

**What Claude says:**
```
⚠️ COST OPTIMIZATION OPPORTUNITY

I can complete this task, but I'd need to read 8+ GUI files (~15,000 tokens) 
to find all forms and add validation.

To reduce cost by ~70%:
- Which specific form(s) need validation? (e.g., "gui_clients.py")
- Which fields? (e.g., "email and phone fields")
- Which validation pattern? (e.g., "use regex like on line 45")

Proceed with full exploration, or provide details first?
```

**Your options:**
1. Provide the details (recommended) = ~4,500 tokens instead of ~15,000
2. Say "proceed anyway" if you really need all forms checked

---

### Trigger 2: High Token Estimate (>3,000 tokens)

**What triggers it:**
- Claude calculates the task will cost more than 3,000 tokens
- Based on files to read, code to generate, conversation complexity

**Example prompt that triggers:**
> "Create a new reporting module with database queries and UI"

**What Claude says:**
```
⚠️ HIGH COST TASK

Estimated token usage: ~8,500 tokens

This task involves:
- Creating multiple new files (~3,000 tokens)
- Reading database schema and existing patterns (~2,500 tokens)
- UI development (~2,000 tokens)
- Planning and review (~1,000 tokens)

This is a complex task. Consider breaking it into phases:
Phase 1: Database queries only (~2,500 tokens)
Phase 2: UI for reports (~3,000 tokens)

Proceed with full task, or split into phases?
```

**Your options:**
1. Split into phases (recommended) = better control, easier to adjust
2. Proceed with full task if it's all interconnected

---

### Trigger 3: Missing Context (no file names)

**What triggers it:**
- Your prompt describes "what" but not "where"
- No file names or locations provided
- Claude would need to explore to find relevant files

**Example prompt that triggers:**
> "Fix the validation bug"

**What Claude says:**
```
⚠️ MISSING CONTEXT

I can help fix this bug, but answering these would save ~60% in tokens:

Required info:
- Which file has the bug? (e.g., "validators.py")
- Which function/line? (e.g., "line 67 in validate_email")
- What's the symptom? (e.g., "accepts invalid emails")

Without this, I'd need to:
1. Search codebase for validation code (~5,000 tokens)
2. Read multiple validation files (~4,000 tokens)
3. Identify the issue through testing (~2,000 tokens)

Total: ~11,000 tokens vs. ~2,000 tokens with details

Proceed with exploration, or provide context first?
```

**Your options:**
1. Provide context (strongly recommended) = 80% savings
2. Proceed if you genuinely don't know where the bug is

---

### Trigger 4: Mixed Tasks (3+ unrelated changes)

**What triggers it:**
- Your prompt asks for multiple unrelated things
- Changes affect different areas of the codebase
- No clear connection between tasks

**Example prompt that triggers:**
> "Add a new field to clients, fix the timesheet bug, and update the README"

**What Claude says:**
```
⚠️ TASK BUNDLING DETECTED

This prompt contains 3 separate tasks:
1. Database/schema change (Client field)
2. Bug fix (Timesheet)
3. Documentation update (README)

Cost impact:
- Together: ~7,500 tokens (context switching, reading multiple areas)
- Separately: ~2,000 + 1,500 + 500 = ~4,000 tokens (focused execution)

Recommendation: Split into 3 prompts for better efficiency and clarity.

Proceed with all together, or split into separate tasks?
```

**Your options:**
1. Split into 3 prompts (recommended) = 47% savings
2. Proceed together if they're actually related (e.g., all for one feature)

---

### Trigger 5: Exploratory Request (research/how-to)

**What triggers it:**
- Prompt asks "how does X work?" or "show me patterns"
- Request seems like research rather than implementation
- No specific action to take

**Example prompt that triggers:**
> "How does our authentication system work?"

**What Claude says:**
```
⚠️ RESEARCH MODE DETECTED

This appears to be a learning/research question rather than an implementation task.

Cost in Agent Mode: ~15,000 tokens
- Read all auth-related files
- Analyze patterns and connections
- Write comprehensive explanation

Alternative approaches:
1. Switch to Ask Mode (read-only, cheaper) = ~8,000 tokens
2. Be specific: "Explain the login flow in auth.py lines 50-100" = ~1,500 tokens
3. Search codebase yourself first (free), then ask specific questions

Which approach would you prefer?
```

**Your options:**
1. Switch to Ask Mode (recommended for research)
2. Make question specific (even better)
3. Proceed in Agent Mode if needed

---

### Trigger 6: Large File Without Line Numbers (>500 lines)

**What triggers it:**
- You reference a file that's large
- No specific line numbers or sections mentioned
- Claude would need to read entire file

**Example prompt that triggers:**
> "Update the db_helper.py file to add caching"

**What Claude says:**
```
⚠️ LARGE FILE OPERATION

File: db_helper.py (847 lines)
Reading entire file: ~6,000 tokens

To optimize (~75% savings):
- Which function(s) need caching? (e.g., "get_all_clients")
- Reference line numbers if you know them
- "Lines 200-250" = ~400 tokens instead of ~6,000 tokens

Or I can search for relevant sections (still cheaper than reading all).

How would you like to proceed?
```

**Your options:**
1. Specify sections/functions (recommended) = huge savings
2. Let Claude search for relevant parts = medium savings
3. Read whole file if truly necessary = full cost

---

## 📊 Warning Severity Levels

Warnings come in 3 levels:

### 🟢 INFO (Proceed, but here's a tip)
- Estimated cost: 1,000-3,000 tokens
- Suggestion for minor optimization
- Totally fine to proceed

**Example:**
> "ℹ️ Tip: This task would be 20% more efficient if you reference the pattern in X file"

---

### 🟡 WARNING (Consider optimizing)
- Estimated cost: 3,000-8,000 tokens
- Significant savings possible
- Recommended to optimize, but your call

**Example:**
> "⚠️ Cost: ~5,500 tokens. Could be ~2,000 tokens if you specify the file/section."

---

### 🔴 HIGH COST (Strongly recommend optimizing)
- Estimated cost: 8,000+ tokens
- Major savings possible (often 70-80%)
- Really should optimize unless necessary

**Example:**
> "🔴 HIGH COST: ~15,000 tokens. This is exploratory - could be ~2,000 tokens with specific file/context."

---

## 🎯 How to Respond to Warnings

### Option 1: Provide Missing Details (Recommended 90% of time)

**When Claude warns about missing context:**

Simply reply with the details:

```
"It's in src/gui_clients.py, line 67, the email validation function.
It's currently accepting emails without @ symbols."
```

Claude will then proceed with full context = much cheaper.

---

### Option 2: Proceed Anyway (When justified)

**Valid reasons to proceed:**
- You genuinely don't know where the issue is
- The exploration IS the task (e.g., "audit all validation")
- The files are interconnected and all need review
- It's complex enough that exploration is necessary

Reply with:
```
"Proceed anyway - I really do need full analysis"
```

---

### Option 3: Revise the Prompt (Best practice)

**When Claude warns about mixed tasks or complexity:**

Acknowledge and split:

```
"Good point. Let's just do task #1 first (add the client field).
I'll ask for the others separately."
```

---

### Option 4: Switch Modes (For research)

**When Claude suggests Ask Mode:**

Switch to Ask Mode (toggle in Cursor) and re-ask:

```
"Explain how authentication works in auth.py"
```

Ask Mode is cheaper for reading/understanding code.

---

## 📋 Warning Response Flowchart

```
Claude gives warning
       ↓
Do I have the details Claude is asking for?
       ↓
   YES → Provide them (saves 60-80%)
       ↓
    NO → Can I find them quickly (<5 min)?
       ↓
   YES → Search/find (free), then provide
       ↓
    NO → Is exploration really necessary?
       ↓
   YES → "Proceed anyway"
       ↓
    NO → Maybe I should clarify the task
```

---

## 💡 Real Examples: Before and After

### Example 1: Database Bug

**❌ Initial prompt (triggers warning):**
> "There's a bug with saving client data"

**⚠️ Claude's warning:**
> "Missing context. Which file, which function, what's the symptom? 
> Would need to read 5+ files (~8,000 tokens) to investigate."

**✅ Your optimized response:**
> "In src/db_helper.py, save_client() function around line 145. 
> New clients save fine, but updates aren't persisting to database."

**Result:** 1,800 tokens instead of 8,000 (77% savings)

---

### Example 2: Multiple Tasks

**❌ Initial prompt (triggers warning):**
> "Add dark mode, fix the invoice bug, and update the README with new features"

**⚠️ Claude's warning:**
> "3 unrelated tasks bundled. Together: ~9,000 tokens. Separately: ~4,500 tokens total."

**✅ Your decision:**
> "Good point. Let's just do the invoice bug fix first. I'll ask for dark mode separately."

**Result:** 1,500 tokens now + 2,000 later + 500 later = 4,000 total vs. 9,000 (56% savings)

---

### Example 3: Large File

**❌ Initial prompt (triggers warning):**
> "Add error handling to the database helper"

**⚠️ Claude's warning:**
> "db_helper.py is 850 lines (~6,000 tokens to read). 
> Which functions need error handling?"

**✅ Your optimized response:**
> "Just the save_client and save_timesheet functions (lines 140-200)"

**Result:** 600 tokens instead of 6,000 (90% savings)

---

## 🔧 Configuring Warning Sensitivity

The current thresholds are:

| Trigger | Threshold | Adjust? |
|---------|-----------|---------|
| Multiple files | 5+ files | Conservative (good for beginners) |
| High cost | 3,000+ tokens | Medium (balanced) |
| Large file | 500+ lines | Conservative (good for beginners) |
| Mixed tasks | 3+ unrelated | Medium (balanced) |

**These defaults are set for someone new to AI assistance.**

As you get more experienced, you might want to adjust:
- More experienced: Raise thresholds (fewer warnings)
- Very cost-conscious: Lower thresholds (more warnings)

To adjust, update `.cursorrules` file (ask Claude to help).

---

## ❓ FAQ

### "Won't all these warnings slow me down?"

**Short answer:** No - they save time overall.

**Why:** 
- Warnings take 5 seconds to read
- Providing context takes 30 seconds
- But saves you from burning through monthly limits in 2 weeks
- Teaches you to prompt better over time

After a few weeks, you'll naturally prompt in ways that avoid warnings.

---

### "What if I'm in a hurry?"

**Options:**
1. Say "proceed anyway" - Claude will execute immediately
2. Provide quick context - takes 30 seconds, saves 60%
3. Batch mode: "For the next 5 prompts, proceed without warnings"

You're in control. Warnings are suggestions, not blocks.

---

### "Can I disable warnings?"

**Yes, but not recommended** (especially as a beginner).

To disable: Update `.cursorrules` to remove warning requirements.

**Better approach:** As you get experienced, warnings will trigger less often naturally because you'll prompt more efficiently.

---

### "What if Claude's estimate is wrong?"

Estimates are based on typical patterns. Actual costs may vary by ±20%.

If you notice estimates are consistently off, Claude can adjust the estimation logic.

---

## 📊 Measuring Warning Effectiveness

Track this for 1 month:

**Week 1:**
- Warnings received: 15
- Times optimized: 5
- Times proceeded anyway: 10
- Average savings per optimization: ~3,000 tokens
- Total saved: ~15,000 tokens

**Week 4:**
- Warnings received: 3 (you're prompting better!)
- Times optimized: 2
- Times proceeded anyway: 1
- Average savings per optimization: ~2,500 tokens
- Total saved: ~5,000 tokens

**Plus:** Your prompts trigger fewer warnings because you've learned to be specific.

---

## ✅ Best Practices

1. **Read warnings carefully** - they often point to easy optimizations
2. **Provide context when asked** - 30 seconds = 60% savings
3. **Don't ignore patterns** - if you get same warning repeatedly, adjust habits
4. **Learn from warnings** - they teach you what Claude needs to be efficient
5. **Trust the estimates** - they're usually within 20% of actual costs

---

## 🎯 Your Action Plan

**Week 1: Learn from warnings**
- Read every warning
- Provide context when asked
- Note what triggers warnings

**Week 2-3: Adjust habits**
- Start including file names automatically
- Reference patterns proactively
- Break up complex tasks

**Week 4+: Mastery**
- Warnings become rare
- You prompt efficiently by default
- Costs drop 70-80%

---

**Bottom line:** Warnings are your cost-protection safety net. They prevent expensive mistakes and teach you to be more efficient. Embrace them, don't bypass them (at least while learning).

---

*The warning system is your partner in cost management. Let it help you.*

**Last updated:** December 12, 2025

