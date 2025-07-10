#!/usr/bin/env python3
"""
Simple runner script for email automation.
This script demonstrates how to use the email automation system.
"""

import sys
import os
from config import Config
from email_automation import scrape_companies_and_emails, send_emails_batch
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main function to run email automation."""
    
    print("=" * 60)
    print("Email Automation for Software Development Companies")
    print("=" * 60)
    
    # Validate configuration
    config_errors = Config.validate_config()
    if config_errors:
        print("\n❌ Configuration errors found:")
        for error in config_errors:
            print(f"  - {error}")
        print("\nPlease fix these issues before running the script.")
        print("Check the README.md for setup instructions.")
        return 1
    
    print("✅ Configuration validated successfully")
    
    # Show current settings
    print(f"\nCurrent settings:")
    print(f"  - Max emails to scrape: {Config.MAX_SCRAPE_EMAILS}")
    print(f"  - Max emails to send: {Config.MAX_SEND_EMAILS}")
    print(f"  - CV file: {Config.CV_PATH}")
    print(f"  - CSV file: {Config.CSV_FILE}")
    print(f"  - Search API: {Config.SEARCH_API_PREFERENCE}")
    
    # Ask user what to do
    print("\nWhat would you like to do?")
    print("1. Scrape companies and extract emails only")
    print("2. Send emails to unsent recipients only")
    print("3. Both scrape and send (full automation)")
    print("4. Show current CSV statistics")
    
    try:
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            run_scraping_only()
        elif choice == "2":
            run_sending_only()
        elif choice == "3":
            run_full_automation()
        elif choice == "4":
            show_csv_stats()
        else:
            print("Invalid choice. Please run the script again.")
            return 1
            
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return 1
    
    return 0

def run_scraping_only():
    """Run only the scraping functionality."""
    print("\n🔍 Starting company scraping...")
    
    try:
        scraped_count = scrape_companies_and_emails(Config.MAX_SCRAPE_EMAILS)
        print(f"\n✅ Scraping completed! Found {scraped_count} emails.")
        print(f"Results saved to {Config.CSV_FILE}")
        
    except Exception as e:
        logger.error(f"Error during scraping: {str(e)}")
        print(f"❌ Scraping failed: {str(e)}")

def run_sending_only():
    """Run only the email sending functionality."""
    print("\n📧 Starting email sending...")
    
    try:
        sent_count = send_emails_batch(
            Config.SENDER_EMAIL,
            Config.SENDER_PASSWORD,
            Config.CV_PATH,
            Config.MAX_SEND_EMAILS
        )
        print(f"\n✅ Email sending completed! Sent {sent_count} emails.")
        
    except Exception as e:
        logger.error(f"Error during email sending: {str(e)}")
        print(f"❌ Email sending failed: {str(e)}")

def run_full_automation():
    """Run both scraping and sending."""
    print("\n🚀 Starting full automation...")
    
    # Step 1: Scraping
    print("\n🔍 Step 1: Scraping companies...")
    try:
        scraped_count = scrape_companies_and_emails(Config.MAX_SCRAPE_EMAILS)
        print(f"✅ Scraping completed! Found {scraped_count} emails.")
    except Exception as e:
        logger.error(f"Error during scraping: {str(e)}")
        print(f"❌ Scraping failed: {str(e)}")
        return
    
    # Step 2: Sending
    print("\n📧 Step 2: Sending emails...")
    try:
        sent_count = send_emails_batch(
            Config.SENDER_EMAIL,
            Config.SENDER_PASSWORD,
            Config.CV_PATH,
            Config.MAX_SEND_EMAILS
        )
        print(f"✅ Email sending completed! Sent {sent_count} emails.")
    except Exception as e:
        logger.error(f"Error during email sending: {str(e)}")
        print(f"❌ Email sending failed: {str(e)}")
        return
    
    print(f"\n🎉 Full automation completed!")
    print(f"   - Scraped: {scraped_count} emails")
    print(f"   - Sent: {sent_count} emails")

def show_csv_stats():
    """Show statistics about the current CSV file."""
    if not os.path.exists(Config.CSV_FILE):
        print(f"\n❌ CSV file not found: {Config.CSV_FILE}")
        return
    
    try:
        import pandas as pd
        df = pd.read_csv(Config.CSV_FILE)
        
        total_emails = len(df)
        sent_emails = len(df[df['sent'] == 'yes'])
        unsent_emails = len(df[df['sent'] == 'no'])
        
        print(f"\n📊 CSV Statistics ({Config.CSV_FILE}):")
        print(f"  - Total emails: {total_emails}")
        print(f"  - Sent emails: {sent_emails}")
        print(f"  - Unsent emails: {unsent_emails}")
        
        if total_emails > 0:
            print(f"  - Send rate: {sent_emails/total_emails*100:.1f}%")
        
        # Show top companies
        if 'company' in df.columns and len(df) > 0:
            company_counts = df['company'].value_counts().head(5)
            print(f"\n🏢 Top companies by email count:")
            for company, count in company_counts.items():
                print(f"  - {company}: {count} emails")
        
    except Exception as e:
        logger.error(f"Error reading CSV: {str(e)}")
        print(f"❌ Error reading CSV: {str(e)}")

if __name__ == "__main__":
    sys.exit(main()) 