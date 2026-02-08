#!/usr/bin/env python3
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
    
    print("\n📋 WHAT TO DO NEXT:")
    print("1. Open analysis_results.csv in Excel/Google Sheets")
    print("2. Sort by quality_score (lowest = best prospects)")
    print("3. Look for is_hot_lead = TRUE")
    print("4. Contact businesses with specific issues mentioned")

if __name__ == "__main__":
    run_analysis()
