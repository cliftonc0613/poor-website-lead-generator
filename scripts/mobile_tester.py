#!/usr/bin/env python3
"""
Mobile Responsiveness Tester
Test websites for mobile-friendly design using various methods
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import logging

class MobileTester:
    """Test websites for mobile responsiveness and mobile-friendly features"""
    
    def __init__(self, use_selenium=False):
        self.use_selenium = use_selenium
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15'
        })
        self.setup_logging()
        
        if use_selenium:
            self.setup_selenium()
    
    def setup_logging(self):
        """Configure logging"""
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def setup_selenium(self):
        """Setup Selenium WebDriver for browser testing"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.logger.info("Selenium WebDriver initialized")
        except Exception as e:
            self.logger.error(f"Failed to initialize Selenium: {e}")
            self.use_selenium = False
            self.driver = None
    
    def check_mobile_meta_tags(self, url):
        """Check for mobile-friendly meta tags"""
        issues = []
        mobile_indicators = {
            'viewport': False,
            'mobile_optimized': False,
            'apple_mobile_capable': False,
            'responsive_design': False
        }
        
        try:
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Check for viewport meta tag
            viewport_meta = soup.find('meta', attrs={'name': 'viewport'})
            if viewport_meta:
                mobile_indicators['viewport'] = True
                content = viewport_meta.get('content', '').lower()
                if 'width=device-width' in content:
                    mobile_indicators['responsive_design'] = True
            else:
                issues.append("No viewport meta tag")
            
            # Check for mobile-optimized meta tag
            mobile_meta = soup.find('meta', attrs={'name': 'MobileOptimized'})
            if mobile_meta:
                mobile_indicators['mobile_optimized'] = True
            
            # Check for Apple mobile web app meta tags
            apple_meta = soup.find('meta', attrs={'name': 'apple-mobile-web-app-capable'})
            if apple_meta:
                mobile_indicators['apple_mobile_capable'] = True
            
            # Check for CSS media queries (basic check)
            style_tags = soup.find_all('style')
            link_tags = soup.find_all('link', rel='stylesheet')
            
            has_media_queries = False
            for tag in style_tags:
                if tag.string and '@media' in tag.string:
                    has_media_queries = True
                    break
            
            if not has_media_queries:
                issues.append("No CSS media queries found")
            
            return mobile_indicators, issues
            
        except Exception as e:
            return mobile_indicators, [f"Error checking meta tags: {str(e)}"]
    
    def test_mobile_simulation(self, url):
        """Test website using mobile user agent simulation"""
        issues = []
        
        try:
            # Desktop request
            desktop_headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            desktop_response = requests.get(url, headers=desktop_headers, timeout=10)
            desktop_size = len(desktop_response.content)
            
            # Mobile request
            mobile_headers = {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15'
            }
            
            mobile_response = requests.get(url, headers=mobile_headers, timeout=10)
            mobile_size = len(mobile_response.content)
            
            # Analyze differences
            size_ratio = mobile_size / desktop_size if desktop_size > 0 else 1
            
            if abs(size_ratio - 1) < 0.1:
                issues.append("Same content served to mobile and desktop")
            
            # Check for mobile-specific elements
            mobile_soup = BeautifulSoup(mobile_response.content, 'html.parser')
            
            # Look for horizontal scrolling indicators
            if mobile_soup.find('table', {'width': True}):
                table_widths = [int(t.get('width', 0)) for t in mobile_soup.find_all('table', {'width': True})]
                if any(w > 400 for w in table_widths):
                    issues.append("Fixed-width tables may cause horizontal scrolling")
            
            return issues
            
        except Exception as e:
            return [f"Error in mobile simulation: {str(e)}"]
    
    def test_selenium_responsive(self, url):
        """Test responsiveness using Selenium with different screen sizes"""
        if not self.use_selenium or not self.driver:
            return ["Selenium not available"]
        
        issues = []
        screen_sizes = [
            (375, 667, "iPhone"),      # iPhone 6/7/8
            (414, 896, "iPhone XR"),   # iPhone XR/11
            (768, 1024, "iPad"),       # iPad
            (1920, 1080, "Desktop")    # Desktop
        ]
        
        try:
            self.driver.get(url)
            time.sleep(2)  # Wait for page to load
            
            measurements = {}
            
            for width, height, device in screen_sizes:
                self.driver.set_window_size(width, height)
                time.sleep(1)
                
                # Get page dimensions
                body_width = self.driver.execute_script("return document.body.scrollWidth")
                body_height = self.driver.execute_script("return document.body.scrollHeight")
                viewport_width = self.driver.execute_script("return window.innerWidth")
                
                measurements[device] = {
                    'viewport_width': viewport_width,
                    'body_width': body_width,
                    'body_height': body_height,
                    'has_horizontal_scroll': body_width > viewport_width
                }
                
                # Check for horizontal scrolling
                if body_width > viewport_width + 20:  # Allow small margin
                    issues.append(f"Horizontal scrolling on {device} ({body_width}px > {viewport_width}px)")
            
            # Check if mobile versions are too tall (poor responsive design)
            mobile_height = measurements.get('iPhone', {}).get('body_height', 0)
            desktop_height = measurements.get('Desktop', {}).get('body_height', 0)
            
            if mobile_height > desktop_height * 2:
                issues.append("Mobile version significantly taller than desktop (poor responsive design)")
            
            return issues
            
        except WebDriverException as e:
            return [f"Selenium error: {str(e)}"]
        except Exception as e:
            return [f"Error in responsive test: {str(e)}"]
    
    def google_mobile_friendly_test(self, url):
        """
        Use Google Mobile-Friendly Test API (if available)
        Note: This requires API key setup
        """
        # This is a placeholder for Google's Mobile-Friendly Test API
        # You would need to set up the API and get an API key
        
        api_url = "https://searchconsole.googleapis.com/v1/urlTestingTools/mobileFriendlyTest:run"
        
        # Placeholder response - implement with actual API
        return {
            'mobile_friendly': None,
            'issues': ['API not configured'],
            'note': 'Configure Google Search Console API for automated testing'
        }
    
    def comprehensive_mobile_test(self, url):
        """Run all mobile tests and compile results"""
        results = {
            'url': url,
            'mobile_friendly_score': 100,
            'issues': [],
            'recommendations': []
        }
        
        self.logger.info(f"Testing mobile responsiveness for: {url}")
        
        # Test 1: Meta tags
        meta_indicators, meta_issues = self.check_mobile_meta_tags(url)
        results['meta_tags'] = meta_indicators
        results['issues'].extend(meta_issues)
        
        # Deduct points for missing meta tags
        if not meta_indicators['viewport']:
            results['mobile_friendly_score'] -= 30
            results['recommendations'].append("Add viewport meta tag")
        
        if not meta_indicators['responsive_design']:
            results['mobile_friendly_score'] -= 20
            results['recommendations'].append("Use responsive design with width=device-width")
        
        # Test 2: User agent simulation
        simulation_issues = self.test_mobile_simulation(url)
        results['issues'].extend(simulation_issues)
        
        if simulation_issues:
            results['mobile_friendly_score'] -= 10 * len(simulation_issues)
        
        # Test 3: Selenium responsive test (if available)
        if self.use_selenium:
            selenium_issues = self.test_selenium_responsive(url)
            results['issues'].extend(selenium_issues)
            
            if selenium_issues:
                results['mobile_friendly_score'] -= 15 * len(selenium_issues)
        
        # Calculate final score
        results['mobile_friendly_score'] = max(0, results['mobile_friendly_score'])
        results['is_mobile_friendly'] = results['mobile_friendly_score'] >= 70
        
        # Add recommendations based on issues
        if 'horizontal scrolling' in str(results['issues']).lower():
            results['recommendations'].append("Fix horizontal scrolling issues")
        
        if 'media queries' in str(results['issues']).lower():
            results['recommendations'].append("Implement CSS media queries for responsive design")
        
        return results
    
    def cleanup(self):
        """Clean up resources"""
        if self.use_selenium and self.driver:
            self.driver.quit()

def main():
    """Example usage of mobile tester"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Test website mobile responsiveness')
    parser.add_argument('url', help='Website URL to test')
    parser.add_argument('--selenium', action='store_true', help='Use Selenium for advanced testing')
    parser.add_argument('--output', help='Output JSON filename')
    
    args = parser.parse_args()
    
    tester = MobileTester(use_selenium=args.selenium)
    
    try:
        results = tester.comprehensive_mobile_test(args.url)
        
        print(f"\n{'='*50}")
        print(f"MOBILE RESPONSIVENESS TEST RESULTS")
        print(f"{'='*50}")
        print(f"URL: {results['url']}")
        print(f"Mobile-Friendly Score: {results['mobile_friendly_score']}/100")
        print(f"Is Mobile-Friendly: {'✅ YES' if results['is_mobile_friendly'] else '❌ NO'}")
        
        if results['issues']:
            print(f"\n🚨 ISSUES FOUND:")
            for issue in results['issues']:
                print(f"  • {issue}")
        
        if results['recommendations']:
            print(f"\n💡 RECOMMENDATIONS:")
            for rec in results['recommendations']:
                print(f"  • {rec}")
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\nResults saved to: {args.output}")
    
    finally:
        tester.cleanup()

if __name__ == "__main__":
    main()