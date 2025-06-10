# Configuration file for job scraper
import os

# Search Configuration
SEARCH_CONFIG = {
    'keywords': [
        'data scientist',
        'machine learning engineer',
        'AI engineer',
        'python data science',
        'data analyst',
        'ML engineer'
    ],
    'location': 'India',  # Change to your preferred location
    'max_pages': 3,
    'delay_between_requests': 2
}

# Filtering Criteria - CUSTOMIZE THESE FOR YOUR NEEDS
FILTERS = {
    'min_experience': 0,      # Minimum years of experience
    'max_experience': 5,      # Maximum years of experience
    'preferred_locations': [
        'Bangalore', 'Mumbai', 'Delhi', 'Hyderabad', 
        'Pune', 'Chennai', 'Gurgaon', 'Noida'
    ],
    'required_skills': [
        'python', 'machine learning', 'sql', 'pandas',
        'tensorflow', 'pytorch', 'data analysis'
    ],
    'exclude_companies': [
        # Add companies you want to avoid (uncomment and add names)
        # 'Company Name 1',
        # 'Company Name 2'
    ]
}

# Output Configuration
OUTPUT_CONFIG = {
    'save_to_git': True,
    'create_historical_backup': True,
    'max_historical_files': 30
}
