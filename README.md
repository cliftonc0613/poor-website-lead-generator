# Poor Website Lead Generator

🎯 **Automated system for finding home services businesses with poor websites in Upstate South Carolina**

This repository contains everything you need to identify HVAC, plumbing, and landscaping businesses in the Greenville, Spartanburg, and Anderson areas who need website improvements.

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/cliftonc0613/poor-website-lead-generator.git
   cd poor-website-lead-generator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run manual search queries**
   - Use search patterns from `search_queries.md`
   - Test 5-10 websites manually first

4. **Start automation**
   ```bash
   python business_analyzer.py --location "Greenville SC" --services "HVAC,plumbing,landscaping"
   ```

## 📊 Expected Results

- **50-100 leads per week** using free tools
- **20-30% conversion rate** to qualified prospects  
- **10-15 critical cases weekly** (websites scoring <30/100)
- **$0 cost** - uses only free tools and APIs

## 🎯 What This Finds

**Automatic red flags for hot leads:**
- No HTTPS security
- Broken mobile responsiveness  
- Outdated copyright dates (pre-2022)
- "Lorem ipsum" placeholder text
- Flash content or broken functionality
- Missing contact information

## 📁 Repository Structure

```
├── README.md                           # This file
├── poor-website-detection-guide.md     # Complete research guide (18k+ words)
├── business_analyzer.py               # Main automation script
├── search_queries.md                  # Ready-to-use Google search patterns
├── requirements.txt                   # Python dependencies
├── scripts/
│   ├── directory_scraper.py           # Local business directory scraping
│   ├── mobile_tester.py               # Mobile responsiveness checker
│   └── lead_enhancer.py               # Contact data extraction
├── examples/
│   ├── sample_poor_websites.csv       # Example output format
│   └── search_results_sample.json     # Sample analysis results
└── docs/
    ├── implementation_guide.md         # Step-by-step setup
    └── api_setup.md                    # Free API configuration

```

## 🛠️ Tools & Technologies

**100% Free Stack:**
- Python (Beautiful Soup, Requests, Selenium)
- Google PageSpeed Insights API (100 requests/day free)
- Google Lighthouse CLI (unlimited)
- DuckDuckGo Search (ethical alternative to Google scraping)
- Local business directories (chamber of commerce, etc.)

## 📈 Quality Scoring System

**Website Quality Score (0-100):**
- `80-100`: Excellent (unlikely prospects)
- `60-79`: Good (minor issues only)
- `40-59`: Fair (potential prospects) 
- `20-39`: Poor (good prospects)
- `0-19`: Critical (hot leads!)

## 🎯 Target Market

**Geographic Focus:**
- Greenville, SC
- Spartanburg, SC  
- Anderson, SC
- Surrounding Upstate SC areas

**Business Types:**
- HVAC contractors
- Plumbing services
- Landscaping companies
- Lawn care services
- Related home services

## ⚡ Usage Examples

**Find businesses with broken HTTPS:**
```bash
python business_analyzer.py --check-ssl --location "Greenville SC"
```

**Analyze specific websites:**
```bash
python business_analyzer.py --urls urls.txt --output leads.csv
```

**Run comprehensive analysis:**
```bash
python business_analyzer.py --comprehensive --services "HVAC,plumbing" --min-score 30
```

## 📋 Implementation Phases

### Phase 1: Quick Discovery (Week 1)
- Use Google search operators for immediate results
- Manual analysis of 20-30 websites  
- Validate the scoring system

### Phase 2: Automation (Week 2)
- Set up Python automation pipeline
- Configure free APIs
- Test batch analysis

### Phase 3: Scale (Week 3+)
- Daily automated lead generation
- Enhanced contact data collection
- CRM integration

## 🤝 Contributing

This is a personal project for lead generation, but improvements are welcome:

1. Fork the repository
2. Create your feature branch
3. Submit a pull request

## 📞 Lead Generation Results

**Typical findings per week:**
- 15-20 businesses with no HTTPS
- 25-30 with broken mobile sites
- 10-15 with outdated content (2019-2021 copyrights)
- 5-10 with completely broken functionality

## ⚠️ Ethical Usage

- Respect robots.txt files
- Use reasonable rate limiting (2-3 seconds between requests)
- Don't overload business websites with analysis
- Use this data responsibly for legitimate business outreach

## 🔧 Setup Instructions

See `docs/implementation_guide.md` for detailed setup instructions.

## 📊 Sample Output

```csv
url,business_name,quality_score,issues,phone,location
https://example-hvac.com,ABC HVAC,15,"No HTTPS;Broken mobile;Old copyright","(864) 555-0123","Greenville SC"
https://bad-plumbing-site.com,XYZ Plumbing,22,"No mobile viewport;Lorem ipsum","(864) 555-0456","Spartanburg SC"
```

---

**🎯 Ready to start generating leads? Begin with the search queries in `search_queries.md` for immediate results!**