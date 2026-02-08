#!/usr/bin/env python3
"""
Demo Lead Generation Script
Shows how to find and analyze poor websites for potential leads
"""

from simple_analyzer import SimpleWebsiteAnalyzer
import time

def demo_lead_generation():
    """Demonstrate the complete lead generation process"""
    
    print("🎯 POOR WEBSITE LEAD GENERATION DEMO")
    print("="*50)
    print()
    
    # Sample URLs that might represent real businesses found via Google searches
    demo_urls = [
        "http://example.com",  # No HTTPS
        "https://httpforever.com",  # Likely poor mobile
        "https://berkshirehathaway.com",  # Berkshire Hathaway (famously simple site)
        "https://cliftonc0613.github.io/kicking-tree-lawn-care/",  # Your good site for comparison
    ]
    
    print("📋 URLS TO ANALYZE:")
    for i, url in enumerate(demo_urls, 1):
        print(f"  {i}. {url}")
    print()
    
    # Initialize analyzer
    analyzer = SimpleWebsiteAnalyzer()
    
    print("🔍 STARTING ANALYSIS...")
    print("(This simulates what happens when you find businesses via Google searches)")
    print()
    
    # Analyze websites
    results = analyzer.batch_analyze(demo_urls, delay=1)  # Faster for demo
    
    print("\n📊 DETAILED RESULTS:")
    print("-" * 80)
    
    for result in results:
        status_icon = "✅" if result['status'] == 'analyzed' else "❌"
        lead_icon = "🔥" if result.get('is_hot_lead') else "💡" if result.get('needs_redesign') else "✅"
        
        print(f"{status_icon} {lead_icon} {result['url']}")
        print(f"   Business: {result['business_name'] or 'Unknown'}")
        print(f"   Quality Score: {result['quality_score']}/100")
        
        if result['phone']:
            print(f"   📞 Phone: {result['phone']}")
        if result['email']:
            print(f"   📧 Email: {result['email']}")
            
        if result['issues']:
            print(f"   ⚠️  Issues: {', '.join(result['issues'])}")
        print()
    
    # Export results
    analyzer.export_to_csv(results, 'demo_leads.csv')
    
    # Show summary
    analyzer.print_summary(results)
    
    print(f"\n💾 RESULTS SAVED TO: demo_leads.csv")
    print(f"📈 NEXT STEPS:")
    print(f"  1. Open demo_leads.csv in Excel/Sheets")
    print(f"  2. Sort by quality_score (lowest first)")
    print(f"  3. Contact businesses with score < 50")
    print(f"  4. Mention specific issues in your outreach")

def show_google_search_demo():
    """Show how to use Google searches to find URLs"""
    print("\n🔍 HOW TO FIND URLS FOR ANALYSIS:")
    print("="*50)
    
    searches = [
        '"HVAC" Greenville SC "copyright 2018"',
        '"plumber" Spartanburg SC inurl:index.html',
        '"landscaping" Anderson SC site:weebly.com',
        'intitle:"under construction" contractor Greenville'
    ]
    
    print("📋 GOOGLE SEARCH PATTERNS:")
    for i, search in enumerate(searches, 1):
        print(f"  {i}. {search}")
    
    print(f"\n💡 WORKFLOW:")
    print(f"  1. Copy a search pattern above")
    print(f"  2. Paste into Google and search")
    print(f"  3. Copy 10-15 business URLs from results")
    print(f"  4. Save URLs to a text file (one per line)")
    print(f"  5. Run: python3 simple_analyzer.py --file your_urls.txt")

if __name__ == "__main__":
    demo_lead_generation()
    show_google_search_demo()