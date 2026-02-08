#!/usr/bin/env python3
"""
Command Interface for Poor Website Lead Generator
Simple command system for automated analysis
"""

import sys
import os
import re
from simple_analyzer import SimpleWebsiteAnalyzer
from datetime import datetime

class CommandInterface:
    """Handle commands for website analysis"""
    
    def __init__(self):
        self.analyzer = SimpleWebsiteAnalyzer()
        
    def process_command(self, command_text):
        """Process a command and return results"""
        
        command_text = command_text.strip().lower()
        
        # Analyze URLs if they're provided
        urls = self.extract_urls(command_text)
        if urls:
            return self.analyze_urls(urls)
        
        # Handle search-style commands
        if any(term in command_text for term in ['hvac', 'plumbing', 'landscaping', 'contractor']):
            return self.handle_search_command(command_text)
        
        # Default help
        return self.show_help()
    
    def extract_urls(self, text):
        """Extract URLs from text"""
        url_pattern = re.compile(r'https?://[^\s]+')
        urls = url_pattern.findall(text)
        
        # Also look for domain-like patterns
        domain_pattern = re.compile(r'\b[a-zA-Z0-9-]+\.[a-zA-Z]{2,}\b')
        domains = domain_pattern.findall(text)
        
        # Add http:// to domains that don't have protocol
        for domain in domains:
            if not any(domain in url for url in urls):
                urls.append(f"https://{domain}")
        
        return urls
    
    def analyze_urls(self, urls):
        """Analyze provided URLs and return formatted results"""
        
        print(f"🔍 Analyzing {len(urls)} URLs...")
        
        results = self.analyzer.batch_analyze(urls, delay=1)
        
        # Save to CSV
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"analysis_{timestamp}.csv"
        self.analyzer.export_to_csv(results, filename)
        
        # Format results for display
        output = self.format_results(results, filename)
        
        return output
    
    def handle_search_command(self, command):
        """Handle search-related commands"""
        
        service_type = ""
        location = "Greenville SC"
        
        if "hvac" in command:
            service_type = "HVAC"
        elif "plumbing" in command or "plumber" in command:
            service_type = "plumbing"
        elif "landscaping" in command or "lawn care" in command:
            service_type = "landscaping"
        elif "contractor" in command:
            service_type = "contractor"
        
        if "spartanburg" in command:
            location = "Spartanburg SC"
        elif "anderson" in command:
            location = "Anderson SC"
        
        return f"""🔍 SEARCH RECOMMENDATIONS FOR: {service_type} in {location}

📋 COPY THESE GOOGLE SEARCHES:

1. "{service_type}" {location} "copyright 2018"
2. "{service_type}" {location} "copyright 2019"
3. "{service_type}" {location} inurl:index.html
4. intitle:"under construction" {service_type} {location}
5. "{service_type}" {location} site:wix.com
6. "{service_type}" {location} site:weebly.com

💡 WORKFLOW:
1. Copy a search above and paste into Google
2. Collect 10-15 business URLs from results
3. Send me: "analyze [URL1] [URL2] [URL3]..."

Example: "analyze https://business1.com https://business2.net"
"""
    
    def format_results(self, results, filename):
        """Format analysis results for display"""
        
        if not results:
            return "❌ No results to display"
        
        output = [f"📊 ANALYSIS RESULTS ({len(results)} websites)"]
        output.append("=" * 50)
        
        hot_leads = []
        good_prospects = []
        
        for result in results:
            score = result['quality_score']
            name = result['business_name'] or 'Unknown Business'
            url = result['url']
            
            if score < 30:
                hot_leads.append(result)
                output.append(f"🔥 HOT LEAD: {name} (Score: {score})")
            elif score < 50:
                good_prospects.append(result)
                output.append(f"💡 GOOD PROSPECT: {name} (Score: {score})")
            else:
                output.append(f"✅ UNLIKELY: {name} (Score: {score})")
            
            output.append(f"   🌐 {url}")
            
            if result['phone']:
                output.append(f"   📞 {result['phone']}")
            if result['email']:
                output.append(f"   📧 {result['email']}")
            
            if result['issues']:
                issues = ', '.join(result['issues'][:3])  # Show first 3 issues
                output.append(f"   ⚠️  Issues: {issues}")
            
            output.append("")
        
        # Summary
        output.append(f"📈 SUMMARY:")
        output.append(f"   🔥 Hot Leads (score < 30): {len(hot_leads)}")
        output.append(f"   💡 Good Prospects (score < 50): {len(good_prospects)}")
        output.append(f"   📄 Full results saved to: {filename}")
        
        return "\n".join(output)
    
    def show_help(self):
        """Show help message"""
        
        return """🎯 POOR WEBSITE LEAD GENERATOR - COMMAND INTERFACE

📋 SUPPORTED COMMANDS:

🌐 ANALYZE URLS:
  • analyze https://business1.com https://business2.net
  • check https://hvaccompany.com
  • test business-website.org

🔍 GET SEARCH PATTERNS:
  • find hvac in greenville
  • search plumber spartanburg  
  • look for landscaping anderson

💡 EXAMPLES:
  
  You: "analyze https://oldschoolhvac.com https://quickplumbing.net"
  Me: [Runs analysis and shows results]
  
  You: "find hvac greenville"
  Me: [Shows Google search patterns to use]
  
  You: "check business.com"
  Me: [Analyzes single website]

⚡ QUICK REFERENCE:
  Hot Lead (score < 30): 🔥 Contact immediately
  Good Prospect (< 50): 💡 Solid opportunity  
  Unlikely (> 50): ✅ Good website already

Ready for commands!"""

def main():
    """Command line interface"""
    
    interface = CommandInterface()
    
    if len(sys.argv) < 2:
        print(interface.show_help())
        return
    
    # Join all arguments as the command
    command = ' '.join(sys.argv[1:])
    
    result = interface.process_command(command)
    print(result)

# Function for external use
def run_command(command_text):
    """Function to call from other scripts"""
    interface = CommandInterface()
    return interface.process_command(command_text)

if __name__ == "__main__":
    main()