#!/usr/bin/env python3
"""
Script to fix only the specific malformed emails mentioned by the user.
"""

import pandas as pd
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def fix_specific_malformed_emails(csv_file: str = "emails.csv"):
    """Fix only the specific malformed emails mentioned by the user."""
    try:
        # Read the CSV file
        df = pd.read_csv(csv_file)
        logger.info(f"Loaded {len(df)} emails from {csv_file}")
        
        # Specific fixes for the malformed emails mentioned
        specific_fixes = {
            '46001sales.support@gizasystems.comfull': '46001sales.support@gizasystems.com',
            '46001info@gizasystems.comgiza': '46001info@gizasystems.com',
            'ussales.support@gizasystems.comcall': 'ussales.support@gizasystems.com',
            'support.eg@foodics.comp': 'support.eg@foodics.com',
            'support@foodics.comp': 'support@foodics.com',
        }
        
        # Track changes
        fixed_count = 0
        removed_count = 0
        invalid_emails = []
        
        # Apply specific fixes
        for index, row in df.iterrows():
            email = str(row['email'])
            
            if email in specific_fixes:
                new_email = specific_fixes[email]
                df.at[index, 'email'] = new_email
                fixed_count += 1
                logger.info(f"Fixed: {email} -> {new_email}")
            
            # Check for other obviously malformed emails (basic validation)
            elif email and '@' in email:
                domain = email.split('@')[1] if '@' in email else ''
                # Only remove emails that are clearly malformed
                if (domain.endswith('.comp') or 
                    domain.endswith('.comcall') or 
                    domain.endswith('.comfull') or 
                    domain.endswith('.comgiza')):
                    invalid_emails.append(index)
                    logger.warning(f"Removing invalid email: {email}")
        
        # Remove invalid emails
        if invalid_emails:
            df = df.drop(invalid_emails).reset_index(drop=True)
            removed_count = len(invalid_emails)
        
        # Save the cleaned CSV
        df.to_csv(csv_file, index=False)
        
        # Report results
        final_count = len(df)
        logger.info(f"Email cleanup completed:")
        logger.info(f"  - Fixed emails: {fixed_count}")
        logger.info(f"  - Removed invalid emails: {removed_count}")
        logger.info(f"  - Final count: {final_count}")
        
        return {
            'fixed_count': fixed_count,
            'removed_count': removed_count,
            'final_count': final_count
        }
        
    except Exception as e:
        logger.error(f"Error fixing emails: {str(e)}")
        return None

def main():
    """Main function to fix malformed emails."""
    print("=" * 60)
    print("Fix Specific Malformed Emails")
    print("=" * 60)
    
    print("This tool will fix these specific malformed emails:")
    print("  - 46001sales.support@gizasystems.comfull -> 46001sales.support@gizasystems.com")
    print("  - 46001info@gizasystems.comgiza -> 46001info@gizasystems.com")
    print("  - ussales.support@gizasystems.comcall -> ussales.support@gizasystems.com")
    print("  - support.eg@foodics.comp -> support.eg@foodics.com")
    print("  - support@foodics.comp -> support@foodics.com")
    
    confirm = input("\nDo you want to proceed? (y/N): ").strip().lower()
    if confirm != 'y' and confirm != 'yes':
        print("Operation cancelled.")
        return 0
    
    # Fix the emails
    result = fix_specific_malformed_emails()
    
    if result:
        print(f"\n✅ Email fixes completed successfully!")
        print(f"📊 Summary:")
        print(f"  - Fixed emails: {result['fixed_count']}")
        print(f"  - Removed invalid: {result['removed_count']}")
        print(f"  - Final count: {result['final_count']}")
        
        if result['fixed_count'] > 0:
            print(f"\n🔄 Your emails.csv file has been updated with corrected email addresses.")
    else:
        print("❌ Email fixes failed.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 