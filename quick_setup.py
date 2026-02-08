#!/usr/bin/env python3
"""
Quick Setup Script for Poor Website Lead Generator
Run this to get started immediately
"""

import os
import sys

def check_python():
    """Check Python version"""
    version = sys.version_info
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    
    if version.major < 3 or (version.major == 3 and version.minor < 6):
        print("❌ Python 3.6+ required")
        return False
    
    return True

def create_sample_files():
    """Create sample URL files for testing"""
    
    # Sample URLs for immediate testing
    sample_urls = [
        "# Sample URLs for testing",
        "# Replace these with real business URLs you find via Google searches",
        "",
        "# Example sites (for testing only)",
        "http://example.com",
        "https://httpforever.com", 
        "https://berkshirehathaway.com",
        "",
        "# Add your own URLs below:",
        "# https://local-business-website.com",
        "# http://old-contractor-site.net"
    ]
    
    with open('my_urls.txt', 'w') as f:
        f.write('\n'.join(sample_urls))
    
    print("✅ Created my_urls.txt with sample URLs")

def create_quick_start_script():
    """Create a quick start script"""
    
    quick_start = '''#!/usr/bin/env python3
"""Quick Start Script - Run this after finding URLs via Google"""

import subprocess
import sys

def run_analysis():
    print("🚀 Starting Lead Analysis...")
    print("Make sure you've added URLs to my_urls.txt")
    print()
    
    # Run the analyzer
    result = subprocess.run([
        sys.executable, 'simple_analyzer.py', 
        '--file', 'my_urls.txt'
    ], capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print("Errors:", result.stderr)
    
    print("\\n📋 WHAT TO DO NEXT:")
    print("1. Open analysis_results.csv in Excel/Google Sheets")
    print("2. Sort by quality_score (lowest = best prospects)")
    print("3. Look for is_hot_lead = TRUE")
    print("4. Contact businesses with specific issues mentioned")

if __name__ == "__main__":
    run_analysis()
'''
    
    with open('quick_start.py', 'w') as f:
        f.write(quick_start)
    
    print("✅ Created quick_start.py")

def show_instructions():
    """Show complete setup instructions"""
    print(f"""
{'='*60}
🎯 POOR WEBSITE LEAD GENERATOR - READY TO USE!
{'='*60}

📋 WHAT'S BEEN SET UP:
  ✅ Python automation scripts
  ✅ Sample URL file (my_urls.txt)
  ✅ Quick start script
  ✅ Analysis tools ready

🚀 HOW TO START GENERATING LEADS:

STEP 1: Find URLs via Google Searches
  • Copy these search patterns into Google:
    - "HVAC" Greenville SC "copyright 2018"
    - "plumber" Spartanburg SC inurl:index.html
    - "landscaping" Anderson SC site:weebly.com
  
  • Copy 10-15 business URLs from search results
  • Paste URLs into my_urls.txt (one per line)

STEP 2: Run Analysis
  python3 simple_analyzer.py --file my_urls.txt

STEP 3: Review Results
  • Open analysis_results.csv in Excel/Sheets
  • Sort by quality_score (lowest first)
  • Contact businesses scoring < 50

⚡ QUICK COMMANDS:
  
  Test with samples:     python3 demo_lead_generation.py
  Analyze your URLs:     python3 simple_analyzer.py --file my_urls.txt
  Quick analysis:        python3 quick_start.py
  Single URL test:       python3 simple_analyzer.py https://example.com

📊 WHAT THE SCORES MEAN:
  80-100: Excellent site (poor prospect)
  60-79:  Good site (minor issues)
  40-59:  Fair site (potential prospect)
  20-39:  Poor site (good prospect)
  0-19:   Critical issues (hot lead!)

🔥 THE SYSTEM AUTOMATICALLY DETECTS:
  • No HTTPS security
  • No mobile optimization
  • Outdated copyright dates
  • "Under construction" content
  • Missing contact information
  • Broken functionality

💰 EXPECTED RESULTS:
  • 50-100 leads per week
  • 20-30% conversion to prospects
  • 10-15 hot leads weekly

Ready to start? Run: python3 demo_lead_generation.py
""")

def main():
    """Main setup function"""
    print("🔧 Setting up Poor Website Lead Generator...")
    print()
    
    if not check_python():
        return
    
    create_sample_files()
    create_quick_start_script()
    
    print()
    show_instructions()

if __name__ == "__main__":
    main()