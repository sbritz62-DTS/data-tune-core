# Claude Workflow Guide - Data Tune Solutions

## Overview

This guide explains how to work with Claude AI in the Data Tune Solutions workspace, following our established workflow rules for consistent, high-quality development.

## The Workflow Process

### Phase 1: Planning (Before Any Work)

When you give Claude a task, Claude will:

1. **Analyze the Problem**
   - Read relevant files in the codebase
   - Understand the context and requirements
   - Identify what needs to change

2. **Create a Plan**
   - Write a detailed plan to `tasks/todo.md`
   - Break down the task into specific, simple todo items
   - Each item should be focused and minimal in scope

3. **Self-Critique the Plan** ⚠️ (NEW - Always Required)
   - Review own plan for issues, inefficiencies, or risks
   - Check for cost optimization opportunities
   - Identify missing context or unclear requirements
   - Estimate token costs
   - Flag concerns for your review

4. **Get Your Approval**
   - Present the plan AND self-critique to you
   - Wait for your verification before proceeding
   - Make adjustments if needed

**Example Todo List**:
```markdown
## Task: Add Customer Segmentation Query
- [ ] Read existing customer queries for patterns
- [ ] Create new SQL file in sql-library/common-transforms/
- [ ] Write basic customer segmentation query
- [ ] Add inline comments explaining logic
- [ ] Test query with sample data
- [ ] Update sql-library README with new pattern
```

### Phase 2: Execution (After Approval)

Once you approve the plan, Claude will:

1. **Work Through Todo Items**
   - Complete one item at a time
   - Check off items in `tasks/todo.md` as completed
   - Keep changes simple and focused

2. **Silent Execution** (Cost-Optimized)
   - No intermediate check-ins unless blocked
   - No step-by-step progress updates during work
   - Focus purely on implementing the approved plan

3. **Focus on Simplicity**
   - Each change impacts as little code as possible
   - No unnecessary complexity
   - Minimal side effects

### Phase 3: Review (After Completion)

When the task is complete, Claude will:

1. **Add Review Section** to `tasks/todo.md`
   - Summary of changes made
   - List of files created/modified
   - Any important notes or considerations
   - Actual token usage vs. estimate

2. **Final Check**
   - All todo items checked off
   - Code tested and working
   - Documentation updated
   - No bugs introduced

## Core Principles

### 1. Simplicity Above All
- Every change should be as simple as humanly possible
- Impact only the necessary code
- Avoid complex or massive changes
- Small, focused modifications

**Good Example**:
```sql
-- Simple, focused change: Add one new column
ALTER TABLE Customers
ADD Segment VARCHAR(20);
```

**Bad Example**:
```sql
-- Too complex: Changing multiple things at once
ALTER TABLE Customers
ADD Segment VARCHAR(20),
ADD LastPurchaseDate DATE,
ADD TotalSpend DECIMAL(10,2),
DROP COLUMN OldField;
-- Also includes 50 lines of additional changes
```

### 2. No Lazy Work
- **Never use temporary fixes** or workarounds
- **Always find the root cause** of bugs
- **Fix problems completely**, not just symptoms
- **Senior developer mindset**: thorough and professional

**Example**:
- ❌ Lazy: "Add WHERE 1=1 to make the query work"
- ✅ Proper: "The JOIN condition was incorrect, fixed the relationship between Customer and Orders tables"

### 3. Minimal Code Impact
- Changes should only affect what's necessary
- Don't refactor unrelated code
- Keep modifications isolated
- Goal: Don't introduce new bugs

**Checklist for Each Change**:
- [ ] Does this change only affect what's needed?
- [ ] Have I avoided modifying unrelated code?
- [ ] Is this the simplest possible solution?
- [ ] Could this introduce bugs elsewhere?

## Task Management with tasks/todo.md

### File Location
`C:\Users\shane\Cursor Projects\tasks\todo.md`

### Format

```markdown
## Task: [Descriptive Task Name]
**Date**: 2024-01-15
**Status**: In Progress

### Plan
Brief description of the approach and why this solution was chosen.

### Todo Items
- [x] Completed item
- [x] Another completed item
- [ ] In progress item
- [ ] Pending item

### Progress Notes
- 14:30 - Created SQL file with basic structure
- 14:45 - Added customer segmentation logic
- 15:00 - Tested with sample data, working correctly

### Review
**Summary**: Created customer segmentation query using RFM (Recency, Frequency, Monetary) analysis. Query categorizes customers into High Value, Medium Value, and Low Value segments.

**Files Changed**:
- `data-tune-core/sql-library/common-transforms/customer_segmentation.sql` (new)
- `data-tune-core/sql-library/README.md` (updated documentation)

**Notes**: Pattern can be adapted for different segment definitions. Consider adding parameters for customizable thresholds in future enhancement.
```

## Example Workflow Session

### Your Request
"I need a SQL query to identify customers who haven't purchased in 90 days"

### Claude's Response (Planning Phase)

**Claude creates plan in `tasks/todo.md`**:
```markdown
## Task: Create Inactive Customer Identification Query
**Date**: 2024-01-15
**Status**: Planning

### Plan
Create a simple SQL query in the common-transforms library that identifies customers with no purchases in the last 90 days. Will use a LEFT JOIN pattern to find customers without recent orders.

### Todo Items
- [ ] Review existing customer queries for naming patterns
- [ ] Create `inactive_customers.sql` in common-transforms/
- [ ] Write query with clear comments
- [ ] Add parameterization for days threshold
- [ ] Test logic with sample data scenario
- [ ] Update SQL library README
```

**Claude asks**: "I've created a plan with 6 simple steps. Does this approach look good to you?"

### You Approve
"Yes, looks good!"

### Claude Executes

**Update 1**: "✓ Reviewed existing patterns - will follow our standard CTE approach"

**Update 2**: "✓ Created inactive_customers.sql with clear structure"

**Update 3**: "✓ Query complete with 90-day default, parameterizable"

**Update 4**: "✓ Added inline comments explaining the logic"

**Update 5**: "✓ Tested scenario: 1000 customers, 50 inactive - query works correctly"

**Update 6**: "✓ Updated README with new pattern"

### Claude Completes with Review

```markdown
### Review
**Summary**: Created SQL query to identify inactive customers (no purchases in 90+ days). Uses simple LEFT JOIN pattern with date filtering. Parameterized for flexible day thresholds.

**Files Changed**:
- `sql-library/common-transforms/inactive_customers.sql` (new, 25 lines)
- `sql-library/README.md` (added entry in common patterns section)

**Notes**: Query is performant for large datasets. Consider adding index on Orders.OrderDate if this becomes a frequent query. Pattern can be adapted for different time periods or customer attributes.
```

## Best Practices

### For You (The User)
1. **Review the plan** before approving - make sure it matches your expectations
2. **Ask questions** if anything is unclear
3. **Provide feedback** on approach if you have preferences
4. **Keep tasks focused** - break large projects into smaller tasks

### For Claude
1. **Always create a plan first** - never jump straight to coding
2. **Get explicit approval** before making changes
3. **Keep explanations concise** - high-level only
4. **Update todo.md in real-time** - check off items as completed
5. **Prioritize simplicity** - every single time
6. **Find root causes** - no lazy fixes
7. **Minimize impact** - touch as little code as possible

## Quality Checklist

Before completing any task, verify:

- [ ] All todo items checked off
- [ ] Changes are as simple as possible
- [ ] Only necessary code was modified
- [ ] Root causes addressed (no temporary fixes)
- [ ] Code is tested and working
- [ ] Documentation updated
- [ ] Review section completed in todo.md
- [ ] No bugs introduced

## Common Scenarios

### Scenario 1: Bug Fix
1. **Plan**: Investigate root cause, identify exact issue, propose minimal fix
2. **Execute**: Fix only what's broken, test thoroughly
3. **Review**: Document what caused the bug and how it was fixed

### Scenario 2: New Feature
1. **Plan**: Break feature into smallest possible components
2. **Execute**: Build incrementally, one piece at a time
3. **Review**: Document feature usage and any considerations

### Scenario 3: Refactoring
1. **Plan**: Identify specific improvements, one at a time
2. **Execute**: Make changes in isolation, test after each
3. **Review**: Explain benefits and any behavior changes

## Tips for Success

1. **Start Small**: Even large projects are just many small tasks
2. **One Thing at a Time**: Don't mix multiple concerns in one task
3. **Simple Wins**: The simplest solution is usually the best
4. **Verify Plans**: Spend time reviewing plans - it saves debugging later
5. **Document Well**: Future you will appreciate good documentation

## Self-Critique Details

### What Claude Reviews in Self-Critique

**Cost Efficiency:**
- Estimated token usage
- Ways to reduce costs (specify files, reference patterns, etc.)
- Warning if task will exceed 3,000 tokens

**Approach Validation:**
- Is this the simplest solution?
- Are there existing patterns to follow?
- Any risks or potential issues?

**Missing Context:**
- What information would make this more efficient?
- Any ambiguities in the requirements?
- Clarifications that would improve the plan?

**Scope Check:**
- Is this one focused task or multiple bundled tasks?
- Should anything be split out?
- Any unnecessary work included?

### Self-Critique Format

```markdown
### Self-Critique ⚠️

**Cost Estimate:** ~X,XXX tokens

**Issues Found:**
- [Any problems, inefficiencies, or risks]

**Optimization Opportunities:**
- [How the task could be more efficient]

**Questions/Clarifications:**
- [What would make this clearer/better/cheaper]

**Recommendation:** Proceed / Optimize First / Need Input
```

### Your Response to Self-Critique

**If Claude recommends "Optimize First":**
- Provide the missing details
- Result: 40-70% token savings

**If Claude recommends "Need Input":**
- Answer the questions/clarify requirements
- Result: Better solution, fewer revisions

**If Claude recommends "Proceed":**
- Review the plan, approve if good
- Result: Efficient execution

---

## Cost Protection Features

### Automatic Warnings

Claude will warn before starting if:
- Would need to read 5+ files
- Estimated cost >3,000 tokens
- Missing file names or context
- Task mixes 3+ unrelated changes
- Request seems exploratory/research-based
- Large files (>500 lines) without specific sections

See **Warning System Guide** for details.

### Emergency Stop

You can stop Claude anytime:
- Say "STOP", "Cancel", "Hold on", or "Wait"
- Claude saves progress and gives you options
- Continue / Revise / Rollback / Explain

See **Emergency Stop Protocol** for details.

---

## Communication Policy

### Before Execution (Full Communication)
- ✅ Warning if cost/efficiency concerns
- ✅ Complete plan with self-critique
- ✅ Wait for approval

### During Execution (Silent)
- ❌ No intermediate check-ins
- ❌ No progress updates
- ✅ Only speaks if blocked or error occurs

### After Execution (Full Summary)
- ✅ Comprehensive review
- ✅ All changes listed
- ✅ Token usage reported
- ✅ Important notes highlighted

---

## Related Guides

- **Cost Savings Cheat Sheet** - Quick reference for efficient prompts
- **Cost Reality Check** - Understanding token economics
- **Warning System Guide** - How cost warnings work
- **DIY Task List** - When NOT to use Claude (save tokens)
- **Emergency Stop Protocol** - Stopping and recovering mid-task

---

## Questions?

If you're ever unsure about the workflow:
- Check `tasks/todo.md` for current status
- Review this guide for process reminders
- Ask Claude to explain the plan before approving
- Request adjustments if approach doesn't feel right
- Use "STOP" if something seems wrong

---

**Remember**: Quality over speed. Simple over complex. Complete over temporary. Cost-conscious always.

*Updated: December 12, 2025*

