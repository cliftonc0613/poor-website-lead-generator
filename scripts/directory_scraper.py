#!/usr/bin/env python3
"""
Directory Scraper for Local Business Directories
Extracts business information from Upstate SC business directories
"""

import requests
from bs4 import BeautifulSoup
import csv
import time
import re
from urllib.parse import urljoin, urlparse
import logging

class DirectoryScraper:
    """Scrape local business directories for HVAC, plumbing, and landscaping businesses"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.businesses = []
        self.setup_logging()
    
    def setup_logging(self):
        """Configure logging"""
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def scrape_yellowpages(self, location="Greenville SC", categories=None):
        """
        Scrape YellowPages for business listings
        Note: This is for educational purposes - respect robots.txt
        """
        if categories is None:
            categories = ['HVAC', 'Plumbing', 'Landscaping']
        
        businesses = []
        base_url = "https://www.yellowpages.com/search"
        
        for category in categories:
            self.logger.info(f"Scraping YellowPages for {category} in {location}")
            
            params = {
                'search_terms': category,
                'geo_location_terms': location
            }
            
            try:
                response = self.session.get(base_url, params=params, timeout=10)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Parse business listings (adjust selectors as needed)
                listings = soup.find_all('div', class_='result')
                
                for listing in listings[:20]:  # Limit to first 20 results
                    business = self.extract_business_info_yp(listing, category)
                    if business:
                        businesses.append(business)
                
                time.sleep(3)  # Be respectful to servers
                
            except Exception as e:
                self.logger.error(f"Error scraping {category}: {e}")
        
        self.businesses.extend(businesses)
        return businesses
    
    def extract_business_info_yp(self, listing, category):
        """Extract business information from YellowPages listing"""
        try:
            business = {'category': category, 'source': 'YellowPages'}
            
            # Business name
            name_elem = listing.find('a', class_='business-name')
            business['name'] = name_elem.text.strip() if name_elem else 'N/A'
            
            # Phone number
            phone_elem = listing.find('div', class_='phones')
            if phone_elem:
                phone_text = phone_elem.text.strip()
                phone_match = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', phone_text)
                business['phone'] = phone_match.group(0) if phone_match else ''
            else:
                business['phone'] = ''
            
            # Website URL
            website_elem = listing.find('a', href=re.compile(r'http'))
            if website_elem:
                business['website'] = website_elem.get('href', '')
            else:
                business['website'] = ''
            
            # Address
            address_elem = listing.find('div', class_='street-address')
            business['address'] = address_elem.text.strip() if address_elem else ''
            
            return business if business['name'] != 'N/A' else None
            
        except Exception as e:
            self.logger.error(f"Error extracting business info: {e}")
            return None
    
    def scrape_google_search(self, query, max_results=20):
        """
        Scrape Google search results for businesses
        Note: Use this sparingly and consider using search APIs instead
        """
        businesses = []
        
        # This is a simplified example - in practice, use Google Custom Search API
        # or other legitimate search APIs
        
        self.logger.info(f"Manual search recommended for: {query}")
        self.logger.info("Consider using Google Custom Search API for automated searches")
        
        return businesses
    
    def scrape_chamber_directory(self, chamber_url=None):
        """
        Scrape local chamber of commerce directory
        Customize this based on the specific chamber website structure
        """
        if not chamber_url:
            chamber_url = "https://web.greenvillechamber.org"
        
        businesses = []
        
        try:
            # This is a template - adjust based on actual chamber website structure
            search_path = "/search"  # Adjust based on actual URL structure
            
            categories = ['HVAC', 'Plumbing', 'Landscaping', 'Lawn Care']
            
            for category in categories:
                self.logger.info(f"Searching chamber directory for {category}")
                
                # Construct search URL (adjust based on actual chamber site)
                search_url = f"{chamber_url}{search_path}?q={category}"
                
                response = self.session.get(search_url, timeout=10)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract businesses (customize selectors for specific site)
                business_cards = soup.find_all('div', class_='business-card')
                
                for card in business_cards:
                    business = self.extract_chamber_business(card, category)
                    if business:
                        businesses.append(business)
                
                time.sleep(2)
        
        except Exception as e:
            self.logger.error(f"Error scraping chamber directory: {e}")
        
        self.businesses.extend(businesses)
        return businesses
    
    def extract_chamber_business(self, card_elem, category):
        """Extract business info from chamber directory listing"""
        try:
            business = {'category': category, 'source': 'Chamber Directory'}
            
            # Customize these selectors based on actual chamber website
            name_elem = card_elem.find('h3') or card_elem.find('h2')
            business['name'] = name_elem.text.strip() if name_elem else 'N/A'
            
            # Look for website links
            website_link = card_elem.find('a', href=re.compile(r'http.*\.(com|net|org|biz)'))
            business['website'] = website_link.get('href', '') if website_link else ''
            
            # Extract phone if available
            phone_pattern = re.compile(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')
            card_text = card_elem.get_text()
            phone_match = phone_pattern.search(card_text)
            business['phone'] = phone_match.group(0) if phone_match else ''
            
            return business if business['name'] != 'N/A' else None
            
        except Exception as e:
            self.logger.error(f"Error extracting chamber business info: {e}")
            return None
    
    def export_businesses(self, filename='directory_businesses.csv'):
        """Export scraped businesses to CSV"""
        if not self.businesses:
            self.logger.warning("No businesses to export")
            return
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'category', 'website', 'phone', 'address', 'source']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for business in self.businesses:
                writer.writerow(business)
        
        self.logger.info(f"Exported {len(self.businesses)} businesses to {filename}")
    
    def filter_businesses_with_websites(self):
        """Return only businesses that have websites listed"""
        return [b for b in self.businesses if b.get('website')]

def main():
    """Example usage of the directory scraper"""
    scraper = DirectoryScraper()
    
    # Example: Scrape multiple sources
    print("Scraping local business directories...")
    
    # 1. Chamber directory (customize URL and selectors)
    # scraper.scrape_chamber_directory()
    
    # 2. YellowPages (be respectful of rate limits)
    # scraper.scrape_yellowpages("Greenville SC")
    
    # For now, demonstrate the structure
    print("Directory scraper is ready!")
    print("Customize the scraping methods for your target directories.")
    print("Remember to:")
    print("- Check robots.txt files")
    print("- Use appropriate delays between requests")
    print("- Consider using official APIs when available")
    
    # Export any results
    scraper.export_businesses('scraped_businesses.csv')

if __name__ == "__main__":
    main()