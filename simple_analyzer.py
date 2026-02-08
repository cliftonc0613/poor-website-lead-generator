#!/usr/bin/env python3
"""
Simple Website Analyzer - Built-in modules only
Analyzes websites for quality issues using only Python standard library
"""

import urllib.request
import urllib.parse
import urllib.error
import re
import csv
import json
from datetime import datetime
import time
import ssl
import html.parser

class SimpleHTMLParser(html.parser.HTMLParser):
    """Simple HTML parser to extract basic information"""
    
    def __init__(self):
        super().__init__()
        self.title = ""
        self.meta_tags = []
        self.in_title = False
        self.text_content = ""
        
    def handle_starttag(self, tag, attrs):
        if tag == 'title':
            self.in_title = True
        elif tag == 'meta':
            self.meta_tags.append(dict(attrs))
    
    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
    
    def handle_data(self, data):
        if self.in_title:
            self.title += data.strip()
        self.text_content += data.lower() + " "

class SimpleWebsiteAnalyzer:
    """Simple website analyzer using only built-in Python modules"""
    
    def __init__(self):
        # Disable SSL verification for testing (not recommended for production)
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
        
    def analyze_website(self, url):
        """Analyze a single website for quality issues"""
        result = {
            'url': url,
            'quality_score': 100,
            'issues': [],
            'business_name': '',
            'phone': '',
            'email': '',
            'status': 'analyzed',
            'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        try:
            # Ensure URL has protocol
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            print(f"Analyzing: {url}")
            
            # Try HTTPS first, fallback to HTTP
            try:
                response = self.fetch_url(url)
            except:
                if url.startswith('https://'):
                    url = url.replace('https://', 'http://')
                    try:
                        response = self.fetch_url(url)
                        result['issues'].append("HTTPS not available")
                        result['quality_score'] -= 20
                    except Exception as e:
                        result['status'] = 'error'
                        result['issues'] = [f'Site not accessible: {str(e)}']
                        result['quality_score'] = 0
                        return result
                else:
                    result['status'] = 'error'
                    result['issues'] = [f'Site not accessible']
                    result['quality_score'] = 0
                    return result
            
            # Parse HTML
            parser = SimpleHTMLParser()
            try:
                parser.feed(response)
                parser.close()
            except Exception as e:
                result['issues'].append(f"HTML parsing error: {str(e)}")
                result['quality_score'] -= 10
            
            # Extract business name
            if parser.title:
                result['business_name'] = parser.title[:100]  # Limit length
            
            # Security check
            if not url.startswith('https://'):
                result['issues'].append("No HTTPS")
                result['quality_score'] -= 20
            
            # Check for mobile viewport
            has_viewport = False
            for meta in parser.meta_tags:
                if meta.get('name', '').lower() == 'viewport':
                    has_viewport = True
                    break
            
            if not has_viewport:
                result['issues'].append("No mobile viewport")
                result['quality_score'] -= 15
            
            # Check text content
            text = parser.text_content
            
            # Check for outdated copyright
            current_year = datetime.now().year
            for year in range(2015, current_year - 1):
                if f"© {year}" in text or f"copyright {year}" in text:
                    result['issues'].append(f"Outdated copyright: {year}")
                    result['quality_score'] -= 10
                    break
            
            # Check for placeholder content
            if 'lorem ipsum' in text:
                result['issues'].append("Contains Lorem ipsum")
                result['quality_score'] -= 25
            
            # Check for under construction
            construction_phrases = [
                'under construction', 'coming soon', 'website under development',
                'page under construction'
            ]
            for phrase in construction_phrases:
                if phrase in text:
                    result['issues'].append("Under construction")
                    result['quality_score'] -= 30
                    break
            
            # Extract contact information
            phone_pattern = re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b')
            email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
            
            phone_match = phone_pattern.search(text)
            email_match = email_pattern.search(text)
            
            if phone_match:
                result['phone'] = phone_match.group(0)
            if email_match:
                result['email'] = email_match.group(0)
            
            if not phone_match and not email_match:
                result['issues'].append("No contact info found")
                result['quality_score'] -= 20
            
            # Final scoring
            result['quality_score'] = max(0, result['quality_score'])
            result['needs_redesign'] = result['quality_score'] < 50
            result['is_hot_lead'] = result['quality_score'] < 30
            
        except Exception as e:
            result['status'] = 'error'
            result['issues'] = [f'Analysis error: {str(e)}']
            result['quality_score'] = 0
        
        return result
    
    def fetch_url(self, url):
        """Fetch URL content with error handling"""
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        try:
            with urllib.request.urlopen(req, context=self.ssl_context, timeout=10) as response:
                content = response.read().decode('utf-8', errors='ignore')
                return content
        except urllib.error.HTTPError as e:
            raise Exception(f"HTTP {e.code}")
        except urllib.error.URLError as e:
            raise Exception(f"URL Error: {e.reason}")
        except Exception as e:
            raise Exception(f"Connection error: {str(e)}")
    
    def batch_analyze(self, urls, delay=2):
        """Analyze multiple websites with rate limiting"""
        results = []
        total = len(urls)
        
        print(f"Starting analysis of {total} websites...")
        
        for i, url in enumerate(urls, 1):
            print(f"Processing {i}/{total}: {url}")
            
            result = self.analyze_website(url)
            results.append(result)
            
            # Rate limiting
            if i < total:
                time.sleep(delay)
        
        return results
    
    def export_to_csv(self, results, filename='leads.csv'):
        """Export results to CSV file"""
        if not results:
            print("No results to export")
            return
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'url', 'business_name', 'quality_score', 'issues', 'needs_redesign',
                'is_hot_lead', 'phone', 'email', 'status', 'analysis_date'
            ]
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for result in results:
                # Convert issues list to string
                result_copy = result.copy()
                result_copy['issues'] = '; '.join(result['issues'])
                writer.writerow(result_copy)
        
        print(f"Exported {len(results)} results to {filename}")
    
    def print_summary(self, results):
        """Print analysis summary"""
        if not results:
            print("No results to summarize")
            return
        
        total = len(results)
        successful = len([r for r in results if r['status'] == 'analyzed'])
        hot_leads = len([r for r in results if r.get('is_hot_lead', False)])
        needs_redesign = len([r for r in results if r.get('needs_redesign', False)])
        
        avg_score = sum(r['quality_score'] for r in results) / total if total > 0 else 0
        
        print(f"\n{'='*50}")
        print("ANALYSIS SUMMARY")
        print(f"{'='*50}")
        print(f"Total websites analyzed: {total}")
        print(f"Successful analyses: {successful}")
        print(f"Hot leads (score < 30): {hot_leads} ({round(hot_leads/total*100, 1)}%)")
        print(f"Need redesign (score < 50): {needs_redesign}")
        print(f"Average quality score: {round(avg_score, 1)}")
        
        # Show hot leads
        if hot_leads > 0:
            print(f"\n🔥 HOT LEADS FOUND:")
            for result in results:
                if result.get('is_hot_lead', False):
                    print(f"  • {result['url']} - Score: {result['quality_score']} - {result['business_name']}")

def main():
    """Main function for command line usage"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 simple_analyzer.py <url1> [url2] [url3] ...")
        print("   or: python3 simple_analyzer.py --file urls.txt")
        print("\nExample:")
        print("  python3 simple_analyzer.py https://example.com http://business.net")
        print("  python3 simple_analyzer.py --file examples/sample_urls.txt")
        return
    
    analyzer = SimpleWebsiteAnalyzer()
    urls = []
    
    if sys.argv[1] == '--file' and len(sys.argv) > 2:
        # Read URLs from file
        try:
            with open(sys.argv[2], 'r') as f:
                urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        except FileNotFoundError:
            print(f"Error: File {sys.argv[2]} not found")
            return
    else:
        # URLs from command line
        urls = sys.argv[1:]
    
    if not urls:
        print("No URLs to analyze")
        return
    
    # Analyze websites
    results = analyzer.batch_analyze(urls)
    
    # Export to CSV
    analyzer.export_to_csv(results, 'analysis_results.csv')
    
    # Print summary
    analyzer.print_summary(results)

if __name__ == "__main__":
    main()