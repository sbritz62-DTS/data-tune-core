# Power BI Resources - Data Tune Solutions

## Overview

This directory contains reusable Power BI components including DAX measures, M/Power Query scripts, and Power BI themes.

## Directory Structure

```
powerbi-resources/
├── README.md                 # This file
├── dax-measures/             # Reusable DAX calculations
├── power-query/              # M language scripts
├── themes/                   # Custom Power BI themes
└── best-practices.md         # Power BI development guidelines
```

## DAX Measures Library

Common measures organized by category:
- Time intelligence (YoY, MoM, MTD, YTD)
- Statistical calculations
- Dynamic measures
- KPI calculations
- Ranking and filtering

### Usage Pattern
```dax
-- Copy measure to your model
-- Adjust table and column references
-- Test with your data
```

## Power Query (M) Scripts

Reusable Power Query transformations:
- Date table generation
- Data cleaning patterns
- Custom connectors
- API integration templates

### Usage Pattern
1. Open Power Query Editor
2. Create blank query
3. Open Advanced Editor
4. Paste M script
5. Adjust parameters

## Power BI Themes

Custom JSON themes for consistent branding:
- Corporate theme
- Dark mode theme
- Accessible color palettes

### Applying Themes
1. In Power BI Desktop: View → Themes → Browse for themes
2. Select `.json` file
3. Theme applies to all visuals

## Development Workflow

### 1. Extract Reusable Components
When you create a useful DAX measure or M query:
- Save it as a separate `.dax` or `.m` file
- Document parameters and usage
- Add to appropriate folder

### 2. Version Control Pattern
```
powerbi-resources/
├── dax-measures/
│   ├── time-intelligence.dax
│   └── sales-calculations.dax
```

**Do NOT version control:**
- `.pbix` files (too large, binary)
- Data cache files
- Personal workspace files

### 3. Extracting from .pbix
Use Tabular Editor or DAX Studio to:
- Export DAX measures
- Document data model
- Extract M queries

## Power BI Development Best Practices

### Model Optimization
- Use star schema where possible
- Prefer measures over calculated columns
- Remove unused columns early in Power Query
- Disable auto date/time hierarchy if not needed
- Use appropriate data types (smallest possible)

### DAX Best Practices
- Use variables for clarity and performance
- Avoid calculated columns when measures will work
- Use CALCULATE carefully (understand filter context)
- Test performance with DAX Studio
- Document complex measures with comments

### Power Query Best Practices
- Do transformations in Power Query when possible (not DAX)
- Reference queries for reusability
- Use parameters for flexibility
- Remove columns as early as possible
- Fold queries when connecting to databases

### Refresh Strategy
- Incremental refresh for large datasets
- Schedule during off-peak hours
- Monitor refresh history
- Set up failure notifications
- Document dependencies

## Common DAX Patterns

### Time Intelligence Template
```dax
-- Year-over-Year Comparison
Sales YoY = 
VAR CurrentSales = [Total Sales]
VAR PriorYearSales = 
    CALCULATE(
        [Total Sales],
        DATEADD('Date'[Date], -1, YEAR)
    )
RETURN
    DIVIDE(CurrentSales - PriorYearSales, PriorYearSales, 0)
```

### Dynamic Measures Template
```dax
-- Dynamic measure based on slicer selection
Dynamic Measure = 
SWITCH(
    SELECTEDVALUE('Measure Selection'[Measure]),
    "Sales", [Total Sales],
    "Profit", [Total Profit],
    "Quantity", [Total Quantity],
    BLANK()
)
```

## Common M Patterns

### Date Table Generation
```m
let
    StartDate = #date(2020, 1, 1),
    EndDate = #date(2030, 12, 31),
    DayCount = Duration.Days(Duration.From(EndDate - StartDate)) + 1,
    Source = List.Dates(StartDate, DayCount, #duration(1,0,0,0)),
    TableFromList = Table.FromList(Source, Splitter.SplitByNothing()),
    ChangedType = Table.TransformColumnTypes(TableFromList,{{"Column1", type date}}),
    RenamedColumns = Table.RenameColumns(ChangedType,{{"Column1", "Date"}})
in
    RenamedColumns
```

## Performance Optimization

### DAX Performance
- Use DAX Studio to analyze query plans
- Avoid iterating functions on large tables
- Use SUMMARIZE carefully (consider alternatives)
- Leverage relationship instead of LOOKUPVALUE
- Test with realistic data volumes

### Power Query Performance
- Query folding (push transformations to source)
- Reduce data early (filter, remove columns)
- Avoid complex custom columns if source can handle
- Use native connectors when available
- Monitor refresh times

### Model Performance
- Reduce model size (compression)
- Star schema (not snowflake when possible)
- Aggregations for large datasets
- Appropriate relationships (1:many, not many:many)
- Remove unused tables/columns

## Troubleshooting

### Common Issues
1. **Circular Dependency**: Check relationship directions and DAX CALCULATE filters
2. **Slow Refresh**: Check Power Query folding, reduce data volume
3. **Incorrect Totals**: Check filter context, use ALL/ALLSELECTED appropriately
4. **Memory Errors**: Reduce model size, use aggregations, incremental refresh

### Debugging Tools
- **DAX Studio**: Query analysis, performance tuning
- **Tabular Editor**: Advanced model editing
- **Performance Analyzer**: Visual performance testing
- **Query Diagnostics**: Power Query performance

## Resources & References

### Official Documentation
- [DAX Function Reference](https://dax.guide/)
- [Power Query M Reference](https://docs.microsoft.com/power-query/)
- [Power BI Best Practices](https://docs.microsoft.com/power-bi/)

### Community Resources
- SQLBI (Marco Russo & Alberto Ferrari)
- Guy in a Cube (YouTube)
- Power BI Community Forums

---

*Keep this library updated as you develop new patterns and solutions.*

