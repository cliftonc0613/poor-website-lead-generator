#!/usr/bin/env python3
"""
Poor Website Lead Generator - Business Analyzer
Automated system for finding home services businesses with poor websites
"""

import requests
from bs4 import BeautifulSoup
import csv
import json
import re
from datetime import datetime
import time
import argparse
from urllib.parse import urljoin, urlparse
import logging

class BusinessWebsiteAnalyzer:
    """Main class for analyzing business websites and generating leads"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.results = []
        self.setup_logging()
    
    def setup_logging(self):
        """Configure logging for the analyzer"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('business_analyzer.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def analyze_website(self, url):
        """
        Analyze a single website for quality issues
        Returns dict with quality score and detected issues
        """
        issues = []
        score = 100
        
        try:
            # Ensure URL has protocol
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            self.logger.info(f"Analyzing: {url}")
            
            # Basic connectivity test
            try:
                response = self.session.get(url, timeout=10, verify=False)
                status_code = response.status_code
            except requests.exceptions.SSLError:
                # Try HTTP if HTTPS fails
                try:
                    url = url.replace('https://', 'http://')
                    response = self.session.get(url, timeout=10)
                    status_code = response.status_code
                    issues.append("HTTPS not available")
                    score -= 20
                except:
                    return {
                        'url': url,
                        'quality_score': 0,
                        'issues': ['Site not accessible'],
                        'status': 'error'
                    }
            except Exception as e:
                return {
                    'url': url,
                    'quality_score': 0,
                    'issues': [f'Connection error: {str(e)}'],
                    'status': 'error'
                }
            
            if status_code != 200:
                issues.append(f"HTTP {status_code}")
                score -= 30
            
            # Parse HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Security checks
            if not url.startswith('https://'):
                issues.append("No HTTPS")
                score -= 20
            
            # Mobile responsiveness
            viewport = soup.find('meta', attrs={'name': 'viewport'})
            if not viewport:
                issues.append("No mobile viewport")
                score -= 15
            
            # Check for outdated copyright
            text_content = soup.get_text().lower()
            current_year = datetime.now().year
            
            for year in range(2015, current_year - 1):
                if f"© {year}" in text_content or f"copyright {year}" in text_content:
                    issues.append(f"Outdated copyright: {year}")
                    score -= 10
                    break
            
            # Placeholder content
            if 'lorem ipsum' in text_content:
                issues.append("Contains Lorem ipsum")
                score -= 25
            
            # Under construction indicators
            construction_phrases = [
                'under construction', 'coming soon', 'website under development',
                'site under construction', 'page under construction'
            ]
            
            for phrase in construction_phrases:
                if phrase in text_content:
                    issues.append("Under construction")
                    score -= 30
                    break
            
            # Old technology indicators
            if soup.find('object') or soup.find('embed'):
                issues.append("Uses Flash/embedded objects")
                score -= 25
            
            # Check for modern HTML structure
            if not soup.find('meta', attrs={'charset': True}):
                issues.append("No charset declaration")
                score -= 5
            
            # Page title quality
            title = soup.find('title')
            if not title or len(title.text.strip()) < 10:
                issues.append("Poor/missing page title")
                score -= 15
            
            # Contact information check
            phone_pattern = re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b')
            phones = phone_pattern.findall(text_content)
            email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
            emails = email_pattern.findall(text_content)
            
            if not phones and not emails:
                issues.append("No contact info found")
                score -= 20
            
            # Image analysis
            images = soup.find_all('img')
            broken_images = 0
            
            for img in images[:5]:  # Check first 5 images
                src = img.get('src')
                if src:
                    try:
                        img_url = urljoin(url, src)
                        img_response = self.session.head(img_url, timeout=5)
                        if img_response.status_code == 404:
                            broken_images += 1
                    except:
                        broken_images += 1
            
            if broken_images > 0:
                issues.append(f"{broken_images} broken images")
                score -= (broken_images * 5)
            
            # Extract business information
            business_info = self.extract_business_info(soup, text_content)
            
            result = {
                'url': url,
                'quality_score': max(0, score),
                'issues': issues,
                'status': 'analyzed',
                'needs_redesign': score < 50,
                'is_hot_lead': score < 30,
                'business_name': business_info.get('name', ''),
                'phone': business_info.get('phone', ''),
                'email': business_info.get('email', ''),
                'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error analyzing {url}: {str(e)}")
            return {
                'url': url,
                'quality_score': 0,
                'issues': [f'Analysis error: {str(e)}'],
                'status': 'error'
            }
    
    def extract_business_info(self, soup, text_content):
        """Extract business name, phone, and email from website"""
        info = {}
        
        # Business name extraction
        title = soup.find('title')
        if title:
            info['name'] = title.text.strip()
        
        h1 = soup.find('h1')
        if h1 and not info.get('name'):
            info['name'] = h1.text.strip()
        
        # Phone extraction
        phone_pattern = re.compile(r'\b(\d{3}[-.]?\d{3}[-.]?\d{4})\b')
        phone_match = phone_pattern.search(text_content)
        if phone_match:
            info['phone'] = phone_match.group(1)
        
        # Email extraction
        email_pattern = re.compile(r'\b([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})\b')
        email_match = email_pattern.search(text_content)
        if email_match:
            info['email'] = email_match.group(1)
        
        return info
    
    def batch_analyze(self, urls, delay=2):
        """Analyze multiple websites with rate limiting"""
        results = []
        total = len(urls)
        
        for i, url in enumerate(urls, 1):
            self.logger.info(f"Processing {i}/{total}: {url}")
            
            result = self.analyze_website(url)
            results.append(result)
            
            # Rate limiting
            if i < total:
                time.sleep(delay)
        
        self.results = results
        return results
    
    def export_to_csv(self, filename='poor_websites_leads.csv', hot_leads_only=False):
        """Export results to CSV file"""
        if not self.results:
            self.logger.warning("No results to export")
            return
        
        results_to_export = self.results
        if hot_leads_only:
            results_to_export = [r for r in self.results if r.get('is_hot_lead', False)]
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'url', 'business_name', 'quality_score', 'issues', 'needs_redesign',
                'is_hot_lead', 'phone', 'email', 'status', 'analysis_date'
            ]
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for result in results_to_export:
                # Convert issues list to string
                result_copy = result.copy()
                result_copy['issues'] = '; '.join(result['issues'])
                writer.writerow(result_copy)
        
        self.logger.info(f"Exported {len(results_to_export)} results to {filename}")
    
    def get_summary_stats(self):
        """Generate summary statistics from analysis results"""
        if not self.results:
            return {}
        
        total = len(self.results)
        successful = len([r for r in self.results if r['status'] == 'analyzed'])
        hot_leads = len([r for r in self.results if r.get('is_hot_lead', False)])
        needs_redesign = len([r for r in self.results if r.get('needs_redesign', False)])
        
        avg_score = sum(r['quality_score'] for r in self.results) / total if total > 0 else 0
        
        return {
            'total_analyzed': total,
            'successful_analysis': successful,
            'hot_leads': hot_leads,
            'needs_redesign': needs_redesign,
            'average_score': round(avg_score, 1),
            'hot_lead_percentage': round((hot_leads / total) * 100, 1) if total > 0 else 0
        }

def main():
    """Command line interface for the business analyzer"""
    parser = argparse.ArgumentParser(description='Analyze business websites for quality issues')
    
    parser.add_argument('--urls', help='File containing URLs to analyze (one per line)')
    parser.add_argument('--url', help='Single URL to analyze')
    parser.add_argument('--output', default='leads.csv', help='Output CSV filename')
    parser.add_argument('--delay', type=int, default=2, help='Delay between requests (seconds)')
    parser.add_argument('--hot-leads-only', action='store_true', help='Export only hot leads (score < 30)')
    parser.add_argument('--summary', action='store_true', help='Show summary statistics')
    
    args = parser.parse_args()
    
    analyzer = BusinessWebsiteAnalyzer()
    
    urls = []
    
    # Get URLs from various sources
    if args.url:
        urls = [args.url]
    elif args.urls:
        try:
            with open(args.urls, 'r') as f:
                urls = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"Error: File {args.urls} not found")
            return
    else:
        print("Error: Please provide either --url or --urls parameter")
        return
    
    if not urls:
        print("Error: No URLs to analyze")
        return
    
    print(f"Starting analysis of {len(urls)} websites...")
    
    # Analyze websites
    results = analyzer.batch_analyze(urls, delay=args.delay)
    
    # Export results
    analyzer.export_to_csv(args.output, hot_leads_only=args.hot_leads_only)
    
    # Show summary if requested
    if args.summary:
        stats = analyzer.get_summary_stats()
        print("\n" + "="*50)
        print("ANALYSIS SUMMARY")
        print("="*50)
        print(f"Total websites analyzed: {stats['total_analyzed']}")
        print(f"Successful analyses: {stats['successful_analysis']}")
        print(f"Hot leads (score < 30): {stats['hot_leads']} ({stats['hot_lead_percentage']}%)")
        print(f"Need redesign (score < 50): {stats['needs_redesign']}")
        print(f"Average quality score: {stats['average_score']}")
        print(f"\nResults exported to: {args.output}")

if __name__ == "__main__":
    main()