#!/usr/bin/env python3
"""
Main script for Naukri Job Scraper
"""

import os
import sys
import shutil
from datetime import datetime

# Import our configuration
from config import SEARCH_CONFIG, FILTERS, OUTPUT_CONFIG

# Import the scraper class
from naukri_scraper import NaukriJobScraper

def setup_directories():
    """Create necessary directories"""
    directories = ['data', 'historical_data', 'logs']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def cleanup_old_files():
    """Remove old historical files"""
    max_files = OUTPUT_CONFIG.get('max_historical_files', 30)
    hist_dir = 'historical_data'
    
    if not os.path.exists(hist_dir):
        return
    
    files = [f for f in os.listdir(hist_dir) if f.endswith(('.csv', '.json', '.txt'))]
    files.sort(key=lambda x: os.path.getctime(os.path.join(hist_dir, x)))
    
    while len(files) > max_files:
        oldest_file = files.pop(0)
        os.remove(os.path.join(hist_dir, oldest_file))
        print(f"Removed old file: {oldest_file}")

def main():
    # Setup
    setup_directories()
    cleanup_old_files()
    
    # Initialize scraper
    scraper = NaukriJobScraper()
    
    print("🚀 Starting Naukri.com job scraping...")
    print(f"Keywords: {', '.join(SEARCH_CONFIG['keywords'])}")
    
    # Search for jobs
    jobs = scraper.search_jobs(
        keywords_list=SEARCH_CONFIG['keywords'],
        location=SEARCH_CONFIG['location'],
        max_pages=SEARCH_CONFIG['max_pages'],
        delay=SEARCH_CONFIG['delay_between_requests']
    )
    
    print(f"\n📊 Found {len(jobs)} total jobs")
    
    # Filter jobs
    filtered_jobs = scraper.filter_jobs(jobs, FILTERS)
    print(f"📋 After filtering: {len(filtered_jobs)} relevant jobs")
    
    if filtered_jobs:
        # Generate timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = f"jobs_{timestamp}"
        
        # Save results
        csv_file, json_file = scraper.save_jobs(filtered_jobs, base_filename)
        
        # Generate summary
        summary = scraper.generate_summary_report(filtered_jobs)
        summary_file = f"summary_{timestamp}.txt"
        with open(summary_file, 'w') as f:
            f.write(summary)
        
        print(summary)
        print(f"\n✅ Results saved:")
        print(f"   📊 CSV: {csv_file}")
        print(f"   📄 JSON: {json_file}")
        print(f"   📋 Summary: {summary_file}")
        
        # Copy to historical directory
        if OUTPUT_CONFIG.get('create_historical_backup', True):
            for file in [csv_file, json_file, summary_file]:
                dest_path = os.path.join('historical_data', file)
                shutil.copy2(file, dest_path)
        
        # Create latest file links
        latest_files = {
            'latest_jobs.csv': csv_file,
            'latest_jobs.json': json_file,
            'latest_summary.txt': summary_file
        }
        
        for symlink, target in latest_files.items():
            if os.path.exists(symlink):
                os.remove(symlink)
            try:
                os.symlink(target, symlink)
            except OSError:
                # Fallback for Windows
                shutil.copy2(target, symlink)
                
    else:
        print("❌ No jobs found matching your criteria")

if __name__ == "__main__":
    main()
