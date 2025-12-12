# Emergency Stop Protocol - When Things Go Wrong

## Overview

Sometimes you need to stop Claude mid-execution. This guide covers how to interrupt work, what happens when you stop, and how to recover or restart.

---

## 🛑 How to Stop Claude

### Simple Stop Commands

Just type any of these:

- **"STOP"**
- **"Cancel"**
- **"Hold on"**
- **"Wait"**
- **"Pause"**

Claude will:
1. ✅ Stop immediately
2. ✅ Save current progress to `tasks/todo.md`
3. ✅ List what's completed and what's pending
4. ✅ Wait for your direction

**No work is lost** - everything done up to that point is saved.

---

## 🚨 When to Use Emergency Stop

### Scenario 1: Wrong Direction

**You realize:** Claude is working on the wrong thing

**Example:**
- You asked for "validation" but Claude is adding a whole new module
- You meant file X but Claude is editing file Y

**What to do:**
```
"STOP - I meant something different"
```

**Then:** Clarify what you actually wanted

---

### Scenario 2: Cost Escalation

**You notice:** Claude is reading way more files than expected

**Example:**
- Task was supposed to be simple
- Token count is climbing rapidly
- Claude is exploring areas you didn't expect

**What to do:**
```
"STOP - This is getting too expensive"
```

**Then:** Provide more specific context to reduce scope

---

### Scenario 3: Unexpected Changes

**You see:** Claude modified something you didn't expect

**Example:**
- Diff shows changes to files you didn't mention
- Approach seems overly complex
- Something important was deleted

**What to do:**
```
"STOP - Don't touch those other files"
```

**Then:** Clarify scope boundaries

---

### Scenario 4: You Need to Think

**You realize:** You need to make a decision before Claude proceeds

**Example:**
- Claude's plan revealed something you need to consider
- You want to check with a colleague
- You need to verify something first

**What to do:**
```
"STOP - I need to verify something first"
```

**Then:** Come back when ready

---

### Scenario 5: Better Idea Mid-Task

**You think of:** A better approach while Claude is working

**Example:**
- You remember a pattern that would work better
- You realize there's an easier way
- You found existing code that does this

**What to do:**
```
"STOP - I found a better approach"
```

**Then:** Share the new approach

---

## 🔄 What Happens After You Stop

### Claude Will Provide Stop Summary

```markdown
🛑 STOPPED - Current Status

**Completed:**
✅ Created migration file (003_add_field.sql)
✅ Updated db_helper.py (get_all_clients function)

**In Progress:**
⚠️ Was updating gui_clients.py (partially done)

**Pending:**
- Update gui_timesheet.py
- Test changes
- Update documentation

**Files Modified:**
- database/migrations/003_add_field.sql (new file)
- src/db_helper.py (lines 45-67 modified)
- src/gui_clients.py (lines 23-45 modified, INCOMPLETE)

**Your Options:**
1. CONTINUE - Resume from where we stopped
2. REVISE - Adjust the pending items
3. ROLLBACK - Undo changes made so far
4. EXPLAIN - Why did you stop / what's the issue?
```

---

## 🎯 Your 4 Options After Stopping

### Option 1: CONTINUE (Resume Work)

**When to use:**
- You just needed to pause briefly
- Everything looks good, just needed a break
- You verified something and want to proceed

**How:**
```
"Continue - looks good"
```

Claude will pick up exactly where it stopped.

---

### Option 2: REVISE (Change the Plan)

**When to use:**
- You want to adjust remaining work
- You want to skip some pending items
- You thought of a better approach for the rest

**How:**
```
"Revise plan: Skip the timesheet update, just finish the client GUI and docs"
```

Claude will:
- Mark skipped items as cancelled
- Update the plan
- Continue with revised scope

---

### Option 3: ROLLBACK (Undo Changes)

**When to use:**
- Claude went in wrong direction
- Changes are not what you wanted
- You want to start over with better context

**How:**
```
"Rollback - undo all changes"
```

Claude will:
- Use Git to revert changes
- Delete any new files created
- Restore to state before task started

**Note:** Only works if you're using Git! (You should be)

---

### Option 4: EXPLAIN (Understand the Issue)

**When to use:**
- You're not sure why Claude did something
- You want to understand current state
- You need clarification before deciding

**How:**
```
"Explain: Why did you modify gui_clients.py?"
```

Claude will explain the rationale, then you can choose to continue, revise, or rollback.

---

## 🚦 Decision Flowchart

```
You stop Claude
      ↓
Do you understand what Claude was doing?
      ↓
  NO → "Explain" (get clarification)
      ↓
  YES → Are the completed changes correct?
      ↓
  YES → Do you want to change remaining work?
      ↓
  NO → "Continue" (resume as planned)
      ↓
  YES → "Revise" (adjust plan and continue)
      ↓
      
If changes are WRONG → "Rollback" (undo everything)
```

---

## 🔧 Partial Completion Handling

### What if Claude Was Mid-File?

**Claude will tell you:**
```
⚠️ gui_clients.py is partially updated:
- Lines 23-35: Completed (new form fields)
- Lines 36-45: Incomplete (validation not added)
```

**Your options:**
1. **Continue:** Claude finishes lines 36-45
2. **Rollback file:** Undo gui_clients.py changes, keep others
3. **Manual fix:** You finish it yourself, Claude moves to next item

**How to choose:**
```
"Rollback just gui_clients.py, keep the other changes"
```

or

```
"I'll finish gui_clients.py myself. Mark it complete and move to next item."
```

---

## 🔍 Verifying Changes Before Continuing

### Quick Review Checklist

Before deciding to continue, check:

```
□ Look at Git diff (what changed?)
□ Review modified files list
□ Check if new files make sense
□ Verify nothing unexpected was touched
□ Confirm direction is correct
```

**In Cursor:**
- Open Source Control panel (Ctrl+Shift+G)
- Review changed files
- Click files to see diffs
- Takes 30 seconds, prevents problems

---

## 💾 Using Git for Safety

### Why Git Matters for Emergency Stops

**With Git:**
- ✅ Can rollback cleanly
- ✅ Can see exactly what changed
- ✅ Can undo specific files
- ✅ Easy recovery

**Without Git:**
- ❌ Rollback is manual
- ❌ Hard to see all changes
- ❌ Easy to miss something
- ❌ Risk of partial state

**Best practice:** Always commit clean state before starting a task with Claude.

```powershell
# Before starting task
git add .
git commit -m "Clean state before adding new feature"

# Now if you need to rollback
git reset --hard HEAD
```

---

## 🤖 When Claude Auto-Stops

Claude will stop automatically if:

### 1. Plan is Wrong

**Scenario:** Mid-execution, Claude realizes the approach won't work

**Claude says:**
```
🛑 AUTO-STOP: Issue Detected

I was updating db_helper.py but realized the database schema doesn't 
have the field I was trying to use. The migration hasn't been run yet.

**Problem:** Need to run migration before updating application code

**Recommendation:** 
1. Rollback current changes
2. First: Run migration script
3. Then: Update application code

What would you like to do?
```

---

### 2. Unexpected Errors

**Scenario:** Code changes cause errors Claude didn't anticipate

**Claude says:**
```
🛑 AUTO-STOP: Error Encountered

While testing the changes, I encountered an error:
"Column 'Industry' does not exist in table 'Clients'"

**Completed:** Code changes
**Problem:** Database is out of sync with code

**Options:**
1. Rollback code changes
2. Run database migration first
3. Explain the issue in detail

What would you like to do?
```

---

### 3. Cost Overrun

**Scenario:** Task is costing 2x+ the original estimate

**Claude says:**
```
🛑 AUTO-STOP: Cost Threshold Exceeded

Original estimate: ~3,000 tokens
Current usage: ~6,500 tokens (still pending work)

**Why:** The codebase structure was more complex than initial assessment

**Completed:** 
✅ Database changes (2,000 tokens)
✅ Main helper updates (1,500 tokens)

**Remaining:**
- Update 5 GUI files (~5,000 tokens estimated)
- Testing (~1,000 tokens)

**Options:**
1. Continue with remaining work (~6,000 more tokens)
2. Revise scope (maybe update fewer files)
3. I'll finish the GUI updates myself

What would you like to do?
```

---

## 📋 Stop Protocol Checklist

**When you stop Claude:**

1. ✅ Read the stop summary carefully
2. ✅ Check Git diff / modified files list
3. ✅ Verify completed work is correct
4. ✅ Decide: Continue / Revise / Rollback / Explain
5. ✅ Provide clear direction for next step

**Don't:**
- ❌ Panic - nothing is lost
- ❌ Ignore partial completions
- ❌ Assume you need to rollback everything
- ❌ Continue without reviewing changes

---

## 💡 Real Examples

### Example 1: Wrong Scope

**Your task:**
> "Add email validation to the contact form"

**You notice:** Claude is updating 4 different forms

**You:**
> "STOP - Only need the contact form, not all forms"

**Claude:**
```
🛑 STOPPED

Completed:
✅ gui_contacts.py (email validation added)

Was working on:
⚠️ gui_clients.py (partially done)

Pending:
- gui_invoices.py
- gui_settings.py

Rollback gui_clients.py changes and mark others as cancelled?
```

**You:**
> "Yes, rollback clients and cancel the others. Just the contacts form is what I needed."

**Result:** Saved ~4,000 tokens, got exactly what you wanted

---

### Example 2: Cost Escalation

**Your task:**
> "Fix the timesheet calculation bug"

**You notice:** Claude has read 8 files and is still searching

**You:**
> "STOP - This is taking too long. The bug is in gui_timesheet.py line 145"

**Claude:**
```
🛑 STOPPED

Completed exploration:
- Read 8 files (~6,000 tokens)
- Found 3 potential issues

Now that you've specified the location:
- Can proceed directly to fix (~500 tokens)

Continue with targeted fix, or rollback and start over with context?
```

**You:**
> "Let's just continue with the fix now that you're here"

**Result:** Saved additional exploration, completed efficiently

---

### Example 3: Better Approach Found

**Your task:**
> "Create customer segmentation query from scratch"

**Mid-execution you remember:** There's already a similar query in the library

**You:**
> "STOP - I just remembered we have a similar pattern in sql-library/analytics/"

**Claude:**
```
🛑 STOPPED

Completed:
✅ Basic query structure (50 lines)

Found in library:
📁 sql-library/analytics/customer_analysis.sql 
   (Very similar to what we're building)

Options:
1. Continue with current approach
2. Rollback and use library pattern instead (simpler + consistent)

Which would you prefer?
```

**You:**
> "Rollback and use the library pattern"

**Result:** Simpler solution, follows your standards, less code to maintain

---

## 🎯 Best Practices

1. **Don't hesitate to stop** - Better to stop early than let it go wrong
2. **Review changes immediately** - Easier to assess when fresh
3. **Use clear stop commands** - "STOP" is unambiguous
4. **Explain your reasoning** - Helps Claude understand for next time
5. **Commit before major tasks** - Makes rollback clean and easy

---

## 📊 When Stops Are Actually Good

Stopping isn't a failure - it's intelligent course correction:

- ✅ Saves tokens when direction is wrong
- ✅ Prevents compounding mistakes
- ✅ Teaches Claude about your preferences
- ✅ Keeps you in control
- ✅ Results in better final solution

**Don't feel bad about stopping.** It's a feature, not a bug.

---

## 🔗 Related Guides

- **Cost Savings Cheat Sheet** - How to avoid needing stops
- **Warning System Guide** - Catching issues before starting
- **Claude Workflow Guide** - Normal task flow

---

**Bottom Line:** Emergency stop is your safety net. Use it freely. Claude saves state, you review, you decide next steps. You're always in control.

---

*Stopping is smart project management. Don't hesitate when something feels wrong.*

**Last updated:** December 12, 2025

