# Implementation Guide

🚀 **Step-by-step guide to set up and use the Poor Website Lead Generator**

## Prerequisites

### System Requirements
- Python 3.8 or higher
- Internet connection
- 1GB available disk space
- Windows, macOS, or Linux

### Optional Requirements
- Chrome browser (for Selenium automation)
- ChromeDriver (for advanced browser testing)

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/cliftonc0613/poor-website-lead-generator.git
cd poor-website-lead-generator
```

### 2. Set Up Python Environment
```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Test Installation
```bash
# Test the main analyzer
python business_analyzer.py --help

# Test with sample URLs
python business_analyzer.py --urls examples/sample_urls.txt --summary
```

## Configuration

### Basic Configuration
No configuration required for basic functionality! The analyzer works out of the box.

### Optional API Setup
For enhanced features, configure these free APIs:

#### Google PageSpeed Insights API
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable PageSpeed Insights API
4. Create API key
5. Add to environment: `export PAGESPEED_API_KEY=your_key_here`

#### Google Custom Search API (for automated searches)
1. Set up Custom Search Engine at [CSE](https://cse.google.com/)
2. Get API key from Google Cloud Console
3. Add to environment: `export GOOGLE_SEARCH_API_KEY=your_key_here`

## Quick Start Workflow

### Phase 1: Manual Search (15 minutes)
1. **Open search_queries.md**
2. **Copy a search pattern:**
   ```
   "HVAC" Greenville SC "copyright 2018"
   ```
3. **Paste into Google** and run the search
4. **Collect 10-15 URLs** from the results
5. **Save URLs** to a text file (one per line)

### Phase 2: Analyze Websites (5 minutes)
```bash
# Analyze your collected URLs
python business_analyzer.py --urls my_urls.txt --output leads.csv --summary
```

### Phase 3: Review Results (10 minutes)
1. **Open leads.csv** in Excel or Google Sheets
2. **Sort by quality_score** (lowest first)
3. **Filter is_hot_lead = TRUE** for best prospects
4. **Review issues column** for specific problems

## Daily Usage Routine

### Morning (15 minutes)
1. **Run 3-5 search queries** from search_queries.md
2. **Collect 20-30 URLs** from different searches
3. **Save to daily_urls_YYYY-MM-DD.txt**

### Afternoon (20 minutes)
```bash
# Analyze morning's URLs
python business_analyzer.py --urls daily_urls_$(date +%Y-%m-%d).txt --output daily_leads_$(date +%Y-%m-%d).csv --summary

# Review hot leads (score < 30)
grep "TRUE.*TRUE" daily_leads_$(date +%Y-%m-%d).csv
```

### Weekly (30 minutes)
1. **Combine all daily CSV files**
2. **Remove duplicates**
3. **Create outreach priority list**
4. **Update search queries** based on results

## Advanced Usage

### Batch Processing Multiple URL Lists
```bash
# Process multiple files at once
for file in url_lists/*.txt; do
    python business_analyzer.py --urls "$file" --output "results/$(basename "$file" .txt).csv"
done
```

### Filter for Specific Issues
```bash
# Find only sites with HTTPS issues
python business_analyzer.py --urls urls.txt --output https_issues.csv
grep "No HTTPS" https_issues.csv

# Find sites with mobile problems
grep "mobile" https_issues.csv
```

### Automation with Cron (Linux/macOS)
```bash
# Add to crontab for daily automation
# Run every day at 9 AM
0 9 * * * cd /path/to/poor-website-lead-generator && python business_analyzer.py --urls daily_urls.txt --output daily_$(date +%Y%m%d).csv
```

## Troubleshooting

### Common Issues

#### "Connection refused" or timeouts
**Problem:** Website blocks or times out
**Solution:** Add longer delays between requests
```bash
python business_analyzer.py --urls urls.txt --delay 5
```

#### "No module named 'requests'"
**Problem:** Dependencies not installed
**Solution:** 
```bash
pip install -r requirements.txt
```

#### Empty results or all errors
**Problem:** URLs format issue
**Solution:** Ensure URLs include http:// or https://
```
# Good:
https://example.com
http://business.net

# Bad:
example.com
business
www.site.com
```

#### SSL certificate errors
**Problem:** Website has SSL issues
**Solution:** Script automatically handles this, but you can disable SSL verification

### Performance Issues

#### Slow analysis
- Reduce URL list size (20-30 URLs at a time)
- Increase delay between requests: `--delay 3`
- Check internet connection

#### High memory usage
- Process URLs in smaller batches
- Restart Python session periodically

## Output Formats

### CSV Fields Explanation
- **url**: Website address tested
- **business_name**: Extracted business name (from title/h1)
- **quality_score**: 0-100 quality score (lower = worse website)
- **issues**: List of specific problems found
- **needs_redesign**: TRUE if score < 50
- **is_hot_lead**: TRUE if score < 30 (critical issues)
- **phone**: Extracted phone number (if found)
- **email**: Extracted email address (if found)
- **status**: Analysis status (analyzed/error)
- **analysis_date**: When the analysis was performed

### Quality Score Breakdown
- **80-100**: Excellent website (unlikely prospect)
- **60-79**: Good website (minor issues)
- **40-59**: Fair website (potential prospect)
- **20-39**: Poor website (good prospect)
- **0-19**: Critical issues (hot lead!)

## Integration with CRM

### Salesforce
Import CSV using Salesforce Data Import Wizard:
1. Map 'business_name' to Account Name
2. Map 'phone' to Phone
3. Map 'email' to Email
4. Map 'quality_score' to Custom Field

### HubSpot
Use HubSpot's CSV import:
1. Create custom properties for quality_score and issues
2. Import with email as unique identifier
3. Set up workflows based on quality_score

### Excel/Google Sheets
Direct CSV import works perfectly:
1. Use conditional formatting for quality scores
2. Filter and sort by is_hot_lead
3. Create pivot tables for analysis

## Best Practices

### Search Strategy
1. **Start broad** then get specific
2. **Use multiple search operators** per session
3. **Focus on one geographic area** per day
4. **Keep track** of which searches work best

### Analysis Strategy
1. **Process 20-30 URLs** at a time for best performance
2. **Review results manually** before outreach
3. **Update search patterns** based on findings
4. **Keep historical data** to track patterns

### Outreach Strategy
1. **Prioritize hot leads** (score < 30) first
2. **Mention specific issues** in initial contact
3. **Provide value** before pitching services
4. **Track response rates** by issue type

## Scaling Up

### Multiple Markets
1. Create separate URL lists per geographic area
2. Modify search queries for each market
3. Run analysis in parallel for different regions

### Team Usage
1. Create shared folder structure
2. Use standardized naming conventions
3. Implement review process for lead quality

### Automated Pipeline
1. Set up daily cron jobs
2. Integrate with lead management system
3. Create automated email templates

## Support

### Getting Help
1. Check troubleshooting section above
2. Review log files for error details
3. Test with sample URLs first
4. Verify internet connection and dependencies

### Contributing Improvements
1. Fork the repository
2. Make improvements
3. Submit pull request
4. Include test cases

## Next Steps

Once you're comfortable with basic usage:

1. **Set up API integrations** for enhanced data
2. **Create automated workflows** for daily lead generation
3. **Integrate with your CRM** system
4. **Develop outreach templates** based on common issues
5. **Track conversion rates** to optimize search patterns

---

**🎯 Ready to start? Begin with Phase 1 above and generate your first leads in 30 minutes!**