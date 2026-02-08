# Poor Website Detection Methods for Home Services in Upstate South Carolina

## Executive Summary

This guide provides zero-cost, scalable methods for identifying HVAC, plumbing, and landscaping businesses in the Greenville, Spartanburg, and Anderson areas who have poor websites and need web development services.

## 1. Google Search Operator Patterns

### Core Search Operators for Finding Poor Websites

**Basic Operators:**
- `site:` - Search within specific domains
- `inurl:` - Find terms in URLs
- `filetype:` - Target specific file types
- `intitle:` - Search page titles
- `-` (minus) - Exclude terms

### Targeted Search Queries for Upstate SC Home Services

**HVAC Services:**
```
"HVAC" OR "heating" OR "air conditioning" Greenville SC -site:facebook.com -site:linkedin.com -site:yelp.com inurl:index.html
"HVAC repair" Spartanburg SC filetype:html
"heating and cooling" Anderson SC inurl:default
intitle:"under construction" HVAC Greenville
"air conditioning" Greenville SC inurl:~
```

**Plumbing Services:**
```
"plumber" OR "plumbing" Greenville SC -site:angi.com -site:homeadvisor.com inurl:index.htm
"plumbing repair" Spartanburg SC filetype:htm
"emergency plumber" Anderson SC inurl:placeholder
intitle:"coming soon" plumbing Upstate SC
"drain cleaning" Greenville SC inurl:template
```

**Landscaping Services:**
```
"landscaping" OR "lawn care" Greenville SC -site:thumbtack.com inurl:default.html
"tree service" Spartanburg SC filetype:asp
"lawn mowing" Anderson SC inurl:demo
intitle:"website under construction" landscaping Greenville
"yard work" Upstate SC inurl:test
```

### Advanced Search Patterns for Poor Website Indicators

**Outdated Technology Indicators:**
```
site:*.com inurl:frontpage "landscaping" Greenville SC
site:*.com inurl:dreamweaver "HVAC" Spartanburg
site:*.com inurl:geocities "plumber" Anderson SC
"last updated 2015..2020" plumbing Greenville
filetype:swf HVAC Spartanburg
```

**Broken/Incomplete Sites:**
```
intitle:"404" OR "page not found" "HVAC contractor" Greenville
"this page is under construction" plumbing Spartanburg
"welcome to your new website" landscaping Anderson
intitle:"default page" OR "placeholder" home services Greenville
"lorem ipsum" HVAC OR plumbing OR landscaping Upstate SC
```

## 2. Free Web Analysis Techniques

### Google Lighthouse (Automated Quality Assessment)

**Command Line Usage:**
```bash
npm install -g lighthouse
lighthouse https://example-hvac-site.com --output=json --output-path=./report.json
```

**Key Metrics to Flag Poor Sites:**
- Performance Score < 50
- Accessibility Score < 70
- SEO Score < 60
- Mobile-Friendly: No

### PageSpeed Insights API (Free)

**Python Implementation:**
```python
import requests
import json

def check_pagespeed(url):
    api_url = f"https://www.googleapis.com/pagespeed/insights/v5/runPagespeed?url={url}&strategy=mobile"
    response = requests.get(api_url)
    data = response.json()
    
    scores = {
        'performance': data['lighthouseResult']['categories']['performance']['score'] * 100,
        'accessibility': data['lighthouseResult']['categories']['accessibility']['score'] * 100,
        'seo': data['lighthouseResult']['categories']['seo']['score'] * 100
    }
    return scores

# Flag sites with poor scores
poor_site_threshold = {
    'performance': 40,
    'accessibility': 70,
    'seo': 60
}
```

### Mobile Responsiveness Detection

**Free Tools:**
- Google Mobile-Friendly Test API
- Responsive Design Checker (responsive-website-checker.netlify.app)
- Browser DevTools automation

**Python Mobile Test:**
```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def check_mobile_responsive(url):
    options = Options()
    options.add_argument('--headless')
    
    # Desktop test
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1920, 1080)
    driver.get(url)
    desktop_height = driver.execute_script("return document.body.scrollHeight")
    
    # Mobile test
    driver.set_window_size(375, 667)  # iPhone size
    mobile_height = driver.execute_script("return document.body.scrollHeight")
    
    driver.quit()
    
    # Poor responsive design indicators
    height_ratio = mobile_height / desktop_height
    return height_ratio > 2.0  # Suggests poor mobile optimization
```

## 3. Specific Indicators of Outdated/Broken Websites

### Technical Indicators

**Critical Red Flags:**
- No HTTPS (HTTP only)
- Flash content present
- Table-based layouts
- Inline styles everywhere
- No viewport meta tag
- Broken images (404 errors)
- Non-functional contact forms
- Missing or broken SSL certificates

**Design Age Indicators:**
- Copyright dates older than 3 years
- "Best viewed in Internet Explorer" notices
- Visitor counters
- Animated GIFs as primary media
- Comic Sans or other outdated fonts
- Gradient backgrounds
- "Under construction" graphics

### Content Quality Issues

**Poor Content Signals:**
- Lorem ipsum placeholder text
- Duplicate content across pages
- No local address or phone number
- Stock photos without context
- Spelling and grammar errors
- No recent updates (check copyright year)

### Python Detection Script

```python
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

def analyze_website_quality(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        quality_issues = []
        
        # Check for HTTPS
        if not url.startswith('https://'):
            quality_issues.append('No HTTPS')
        
        # Check for mobile viewport
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        if not viewport:
            quality_issues.append('No mobile viewport meta tag')
        
        # Check for outdated copyright
        copyright_text = soup.get_text().lower()
        current_year = datetime.now().year
        for year in range(2015, current_year - 2):
            if f"© {year}" in copyright_text or f"copyright {year}" in copyright_text:
                quality_issues.append(f'Outdated copyright: {year}')
        
        # Check for lorem ipsum
        if 'lorem ipsum' in soup.get_text().lower():
            quality_issues.append('Contains placeholder text')
        
        # Check for Flash content
        if soup.find('object') or soup.find('embed'):
            quality_issues.append('Uses Flash/embedded objects')
        
        # Check for table layouts
        layout_tables = soup.find_all('table')
        if len(layout_tables) > 3:  # Threshold for layout vs data tables
            quality_issues.append('Likely table-based layout')
        
        # Check for broken images
        images = soup.find_all('img')
        broken_images = 0
        for img in images:
            if img.get('src'):
                try:
                    img_response = requests.head(img['src'], timeout=5)
                    if img_response.status_code == 404:
                        broken_images += 1
                except:
                    broken_images += 1
        
        if broken_images > 0:
            quality_issues.append(f'{broken_images} broken images')
        
        return quality_issues
    
    except Exception as e:
        return [f'Error analyzing site: {str(e)}']
```

## 4. Local Business Directory Analysis for Website Quality

### Key Directories for Upstate SC

**Primary Directories:**
- Greenville Chamber of Commerce (web.greenvillechamber.org)
- VisitGreenvilleSC Business Directory
- South Carolina Chamber of Commerce
- SBD Pro (sbdpro.com/local/south-carolina)
- SCIWAY Business Directory
- Greenville.com Business Directory

### Directory Scraping Script

```python
import requests
from bs4 import BeautifulSoup
import csv
import time

def scrape_greenville_chamber():
    """Scrape Greenville Chamber directory for HVAC/Plumbing/Landscaping"""
    base_url = "https://web.greenvillechamber.org/search"
    categories = ['HVAC', 'plumbing', 'landscaping', 'lawn care']
    
    businesses = []
    
    for category in categories:
        search_url = f"{base_url}?q={category}"
        try:
            response = requests.get(search_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Parse business listings (adjust selectors based on site structure)
            listings = soup.find_all('div', class_='business-listing')
            
            for listing in listings:
                business = {
                    'name': listing.find('h3').text if listing.find('h3') else 'N/A',
                    'category': category,
                    'website': None
                }
                
                # Extract website URL
                website_link = listing.find('a', href=re.compile(r'http'))
                if website_link:
                    business['website'] = website_link['href']
                
                businesses.append(business)
            
            time.sleep(2)  # Be respectful to the server
            
        except Exception as e:
            print(f"Error scraping {category}: {e}")
    
    return businesses

def analyze_directory_websites(businesses):
    """Analyze websites from directory scraping"""
    poor_websites = []
    
    for business in businesses:
        if business.get('website'):
            print(f"Analyzing {business['name']}...")
            quality_issues = analyze_website_quality(business['website'])
            
            if len(quality_issues) > 3:  # Threshold for "poor" website
                business['quality_issues'] = quality_issues
                poor_websites.append(business)
    
    return poor_websites
```

### Google My Business Analysis

**Using Search to Find GMB Listings:**
```python
def find_gmb_listings_with_poor_websites(location, service_type):
    """Find Google My Business listings and check their websites"""
    search_query = f"{service_type} near {location}"
    
    # Use SerpAPI (has free tier) or similar service
    # This would require API key but has generous free limits
    
    # Alternative: Use requests with Google search (be mindful of rate limits)
    search_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
    
    # Extract business websites from search results
    # Analyze each website for quality issues
```

## 5. Automation Approaches Using Free Tools

### Complete Automation Pipeline

**1. Lead Generation Script:**
```python
import requests
from bs4 import BeautifulSoup
import csv
import json
from datetime import datetime
import time

class BusinessWebsiteAnalyzer:
    def __init__(self):
        self.poor_websites = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def google_search_businesses(self, query, num_results=20):
        """Search Google for businesses and extract websites"""
        businesses = []
        
        # Use DuckDuckGo or other search APIs for automated queries
        # This is more ethical than scraping Google directly
        
        return businesses
    
    def batch_analyze_websites(self, urls):
        """Analyze multiple websites for quality issues"""
        results = []
        
        for url in urls:
            print(f"Analyzing: {url}")
            
            # Check basic accessibility
            try:
                response = self.session.get(url, timeout=10)
                if response.status_code == 200:
                    quality_score = self.calculate_quality_score(url)
                    results.append({
                        'url': url,
                        'quality_score': quality_score,
                        'needs_redesign': quality_score < 50
                    })
                else:
                    results.append({
                        'url': url,
                        'quality_score': 0,
                        'needs_redesign': True,
                        'error': f'HTTP {response.status_code}'
                    })
            except Exception as e:
                results.append({
                    'url': url,
                    'quality_score': 0,
                    'needs_redesign': True,
                    'error': str(e)
                })
            
            time.sleep(2)  # Rate limiting
        
        return results
    
    def calculate_quality_score(self, url):
        """Calculate overall quality score (0-100)"""
        score = 100
        
        try:
            response = self.session.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Deduct points for various issues
            if not url.startswith('https://'):
                score -= 20
            
            if not soup.find('meta', attrs={'name': 'viewport'}):
                score -= 15
            
            if 'lorem ipsum' in soup.get_text().lower():
                score -= 25
            
            # Check copyright date
            current_year = datetime.now().year
            text = soup.get_text().lower()
            for year in range(2015, current_year - 2):
                if str(year) in text:
                    score -= 10
                    break
            
            # Check for modern elements
            if not soup.find('meta', attrs={'charset': True}):
                score -= 10
            
            # Check page title
            title = soup.find('title')
            if not title or len(title.text) < 10:
                score -= 15
            
        except Exception as e:
            score = 0
        
        return max(0, score)
    
    def export_leads(self, results, filename='poor_websites_leads.csv'):
        """Export poor website leads to CSV"""
        poor_sites = [r for r in results if r.get('needs_redesign', False)]
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['url', 'quality_score', 'error', 'date_analyzed']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for site in poor_sites:
                writer.writerow({
                    'url': site['url'],
                    'quality_score': site['quality_score'],
                    'error': site.get('error', ''),
                    'date_analyzed': datetime.now().strftime('%Y-%m-%d')
                })
        
        print(f"Exported {len(poor_sites)} leads to {filename}")
```

**2. Scheduled Analysis with Cron:**
```bash
# Add to crontab for daily analysis
0 9 * * * /usr/bin/python3 /path/to/business_analyzer.py --location "Greenville SC" --services "HVAC,plumbing,landscaping"
```

### Integration with Free APIs

**Free APIs to Enhance Analysis:**
- PageSpeed Insights API (100 requests/day free)
- Google My Business API (limited free tier)
- Clearbit Logo API (free tier for basic company data)
- Hunter.io email finder (free tier)

**Sample Integration:**
```python
def enhance_lead_data(business_url):
    """Enhance business data using free APIs"""
    enhanced_data = {'website': business_url}
    
    # Get PageSpeed data
    try:
        pagespeed_url = f"https://www.googleapis.com/pagespeed/insights/v5/runPagespeed?url={business_url}"
        response = requests.get(pagespeed_url)
        if response.status_code == 200:
            data = response.json()
            enhanced_data['mobile_score'] = data['lighthouseResult']['categories']['performance']['score'] * 100
    except:
        pass
    
    # Extract business name and contact info from website
    try:
        response = requests.get(business_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract phone numbers
        phone_pattern = re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b')
        phones = phone_pattern.findall(soup.get_text())
        if phones:
            enhanced_data['phone'] = phones[0]
        
        # Extract business name from title or h1
        title = soup.find('title')
        if title:
            enhanced_data['business_name'] = title.text.strip()
        
    except:
        pass
    
    return enhanced_data
```

## Prioritized Workflow

### Phase 1: Quick Discovery (Week 1)
1. **Google Search Operators** - Use advanced search queries to identify 50-100 potential leads
2. **Directory Scraping** - Extract businesses from 3-4 key local directories
3. **Basic Quality Check** - Run automated analysis on collected URLs

### Phase 2: Deep Analysis (Week 2)
1. **Lighthouse Automation** - Run comprehensive quality analysis
2. **Mobile Responsiveness** - Test all sites for mobile-friendliness
3. **Lead Scoring** - Rank opportunities by quality issues severity

### Phase 3: Lead Enhancement (Week 3-4)
1. **Contact Data Extraction** - Parse websites for phone/email
2. **Business Verification** - Confirm they're active businesses
3. **Opportunity Sizing** - Estimate potential project value

### Daily Automation Schedule
```
9:00 AM  - Run new Google searches for fresh leads
10:00 AM - Analyze new websites found
11:00 AM - Update lead database
2:00 PM  - Re-analyze existing leads for changes
3:00 PM  - Generate daily report
```

## Implementation Costs

**Total Cost: $0**
- All tools and APIs used have generous free tiers
- Python and related libraries are open source
- Cloud compute can use free tiers (Heroku, Google Cloud, AWS)

**Time Investment:**
- Initial setup: 8-12 hours
- Daily maintenance: 30 minutes
- Weekly analysis: 2 hours

## Expected Results

**Lead Volume:**
- 50-100 new leads per week
- 20-30% conversion rate to qualified prospects
- 10-15 businesses with critical website issues per week

**Quality Indicators for High-Value Prospects:**
- Businesses with websites scoring < 30/100
- No mobile optimization
- HTTPS missing
- Copyright older than 3 years
- Broken functionality (forms, images, links)

This comprehensive approach provides a scalable, zero-cost method for identifying home services businesses in Upstate South Carolina who desperately need website improvements.