#!/usr/bin/env python3
"""
Script to clean up malformed emails from the CSV file and add proper email validation.
"""

import pandas as pd
import re
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def is_valid_email(email: str) -> bool:
    """Validate email format using regex."""
    if not email or '@' not in email:
        return False
    
    # Basic email validation pattern
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # Check basic format
    if not re.match(email_pattern, email):
        return False
    
    # Additional checks for common malformed patterns
    domain = email.split('@')[1]
    
    # Check for malformed domains
    malformed_patterns = [
        r'\.comp$',  # ends with .comp instead of .com
        r'\.comcall$',  # ends with .comcall
        r'\.comfull$',  # ends with .comfull
        r'\.comgiza$',  # ends with .comgiza
        r'\.com\.sa\.sa$',  # double extensions
        r'\.com\.ae\.ae$',  # double extensions
    ]
    
    for pattern in malformed_patterns:
        if re.search(pattern, domain):
            return False
    
    # Check for minimum domain length
    if len(domain) < 4:  # e.g., a.co
        return False
    
    return True

def fix_common_email_issues(email: str) -> str:
    """Fix common email formatting issues."""
    # Remove extra spaces
    email = email.strip()
    
    # Fix common domain issues
    fixes = {
        '.comp': '.com',
        '.comcall': '.com',
        '.comfull': '.com',
        '.comgiza': '.com',
        '.com.sa.sa': '.com.sa',
        '.com.ae.ae': '.com.ae',
    }
    
    for wrong, right in fixes.items():
        if email.endswith(wrong):
            email = email.replace(wrong, right)
            logger.info(f"Fixed email: {email}")
    
    return email

def clean_emails_csv(csv_file: str = "emails.csv"):
    """Clean up malformed emails in the CSV file."""
    try:
        # Read the CSV file
        df = pd.read_csv(csv_file)
        logger.info(f"Loaded {len(df)} emails from {csv_file}")
        
        # Track statistics
        original_count = len(df)
        invalid_emails = []
        fixed_emails = []
        
        # Process each email
        for index, row in df.iterrows():
            email = str(row['email'])
            
            # Try to fix common issues first
            fixed_email = fix_common_email_issues(email)
            
            # Check if email is valid
            if not is_valid_email(fixed_email):
                invalid_emails.append({
                    'original': email,
                    'fixed': fixed_email,
                    'company': row['company'],
                    'index': index
                })
                logger.warning(f"Invalid email found: {email} -> {fixed_email}")
            else:
                # Update the email if it was fixed
                if fixed_email != email:
                    df.at[index, 'email'] = fixed_email
                    fixed_emails.append({
                        'original': email,
                        'fixed': fixed_email,
                        'company': row['company']
                    })
        
        # Remove invalid emails
        if invalid_emails:
            logger.info(f"Removing {len(invalid_emails)} invalid emails:")
            for invalid in invalid_emails:
                logger.info(f"  - {invalid['original']} ({invalid['company']})")
            
            # Drop invalid email rows
            invalid_indices = [item['index'] for item in invalid_emails]
            df = df.drop(invalid_indices).reset_index(drop=True)
        
        # Save the cleaned CSV
        df.to_csv(csv_file, index=False)
        
        # Report results
        final_count = len(df)
        logger.info(f"Email cleanup completed:")
        logger.info(f"  - Original emails: {original_count}")
        logger.info(f"  - Fixed emails: {len(fixed_emails)}")
        logger.info(f"  - Removed invalid emails: {len(invalid_emails)}")
        logger.info(f"  - Final count: {final_count}")
        
        if fixed_emails:
            logger.info("Fixed emails:")
            for fixed in fixed_emails:
                logger.info(f"  - {fixed['original']} -> {fixed['fixed']} ({fixed['company']})")
        
        return {
            'original_count': original_count,
            'fixed_count': len(fixed_emails),
            'removed_count': len(invalid_emails),
            'final_count': final_count
        }
        
    except Exception as e:
        logger.error(f"Error cleaning emails: {str(e)}")
        return None

def main():
    """Main function to clean emails."""
    print("=" * 60)
    print("Email Cleanup Tool")
    print("=" * 60)
    
    print("This tool will:")
    print("1. Fix common email formatting issues (.comp -> .com, etc.)")
    print("2. Remove completely invalid email addresses")
    print("3. Update the emails.csv file")
    
    confirm = input("\nDo you want to proceed? (y/N): ").strip().lower()
    if confirm != 'y' and confirm != 'yes':
        print("Operation cancelled.")
        return 0
    
    # Clean the emails
    result = clean_emails_csv()
    
    if result:
        print(f"\n✅ Email cleanup completed successfully!")
        print(f"📊 Summary:")
        print(f"  - Original emails: {result['original_count']}")
        print(f"  - Fixed emails: {result['fixed_count']}")
        print(f"  - Removed invalid: {result['removed_count']}")
        print(f"  - Final count: {result['final_count']}")
        
        if result['fixed_count'] > 0 or result['removed_count'] > 0:
            print(f"\n🔄 Your emails.csv file has been updated with clean email addresses.")
    else:
        print("❌ Email cleanup failed.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 