#!/usr/bin/env python3
"""
Improved Email Automation with Dynamic Company Discovery
Finds 30+ companies daily using multiple search strategies
"""

import logging
import sys
from email_automation import EmailSender, CSVManager
from dynamic_company_finder import DynamicCompanyFinder
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def scrape_companies_and_emails():
    """Scrape companies and extract emails using dynamic discovery."""
    logger.info("Starting dynamic company and email scraping")
    
    # Initialize the dynamic company finder
    finder = DynamicCompanyFinder()
    
    # Find companies with emails (targeting 30+ companies)
    companies_with_emails = finder.find_companies_with_emails(target_count=50)
    
    # Initialize CSV manager
    csv_manager = CSVManager()
    csv_manager.initialize_csv()
    
    # Process and save emails
    total_emails = 0
    total_companies = 0
    
    for company_data in companies_with_emails:
        company_name = company_data['name']
        company_url = company_data['website']
        emails = company_data['emails']
        
        for email in emails:
            csv_manager.add_email(email, company_name, company_url)
            total_emails += 1
            
        if emails:
            total_companies += 1
    
    # Save to CSV
    csv_manager.save_to_csv()
    
    logger.info(f"Scraped {total_emails} emails from {total_companies} companies")
    return total_emails

def send_unsent_emails():
    """Send emails to unsent recipients."""
    logger.info("Starting email sending batch")
    
    # Initialize email sender and CSV manager
    email_sender = EmailSender()
    csv_manager = CSVManager()
    
    # Get unsent emails
    unsent_emails = csv_manager.get_unsent_emails(limit=Config.MAX_SEND_EMAILS)
    
    if not unsent_emails:
        logger.info("No unsent emails found")
        return 0
    
    # Send emails
    sent_count = 0
    for email_data in unsent_emails:
        try:
            success = email_sender.send_email(
                email_data['email'],
                email_data['company'],
                Config.CV_PATH
            )
            
            if success:
                csv_manager.mark_as_sent(email_data['email'])
                sent_count += 1
                logger.info(f"✅ Sent email to {email_data['email']} ({email_data['company']})")
            else:
                logger.error(f"❌ Failed to send email to {email_data['email']}")
                
        except Exception as e:
            logger.error(f"Error sending email to {email_data['email']}: {str(e)}")
            continue
    
    # Save updated CSV
    csv_manager.save_to_csv()
    
    logger.info(f"Sent {sent_count} emails successfully")
    return sent_count

def show_statistics():
    """Show email database statistics."""
    csv_manager = CSVManager()
    stats = csv_manager.get_statistics()
    
    print(f"📊 Email Database Statistics:")
    print(f"   Total emails: {stats['total']}")
    print(f"   Sent emails: {stats['sent']}")
    print(f"   Unsent emails: {stats['unsent']}")
    print(f"   Send rate: {stats['send_rate']:.1f}%")
    
    # Show recent emails
    recent_emails = csv_manager.get_recent_emails(limit=5)
    if recent_emails:
        print(f"\n📧 Recent emails:")
        for email_data in recent_emails:
            status = "✅ Sent" if email_data['sent'] == 'yes' else "⏳ Pending"
            print(f"   {email_data['email']} ({email_data['company']}) - {status}")
    
    # Show company statistics
    company_stats = csv_manager.get_company_statistics()
    if company_stats:
        print(f"\n🏢 Top companies by email count:")
        for company, count in company_stats.items():
            print(f"   {company}: {count} emails")

def main():
    """Main function for improved email automation."""
    print("=" * 70)
    print("🚀 IMPROVED Email Automation - Software Project Manager Applications")
    print("=" * 70)
    
    # Validate configuration
    config_errors = Config.validate_config()
    if config_errors:
        print("❌ Configuration errors found:")
        for error in config_errors:
            print(f"   - {error}")
        return
    
    print("✅ Configuration validated successfully")
    
    # Show current settings
    print(f"\n⚙️  Current settings:")
    print(f"   - Max emails to scrape: {Config.MAX_SCRAPE_EMAILS}")
    print(f"   - Max emails to send: {Config.MAX_SEND_EMAILS}")
    print(f"   - CV file: {Config.CV_PATH}")
    print(f"   - CSV file: {Config.CSV_FILE}")
    print(f"   - Email delay: {Config.EMAIL_SEND_DELAY} seconds")
    
    # Interactive menu
    while True:
        print(f"\n🎯 What would you like to do?")
        print("   1. Find real companies and extract emails")
        print("   2. Send emails to unsent recipients")
        print("   3. Full automation (find + send)")
        print("   4. Show email database statistics")
        print("   5. Exit")
        
        try:
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == '1':
                print("\n🔍 Finding real companies...")
                scraped_count = scrape_companies_and_emails()
                print(f"✅ Found {scraped_count} emails from real companies!")
                
            elif choice == '2':
                print("\n📧 Sending emails...")
                sent_count = send_unsent_emails()
                print(f"✅ Sent {sent_count} emails successfully!")
                
            elif choice == '3':
                print("\n🚀 Starting full automation...")
                
                print("\n🔍 Step 1: Finding real companies...")
                scraped_count = scrape_companies_and_emails()
                print(f"✅ Found {scraped_count} emails from real companies!")
                
                print("\n📧 Step 2: Sending emails...")
                sent_count = send_unsent_emails()
                print(f"✅ Sent {sent_count} emails successfully!")
                
                print(f"\n🎉 Full automation completed!")
                print(f"   📊 Results: Found {scraped_count} emails, Sent {sent_count} emails")
                
            elif choice == '4':
                print()
                show_statistics()
                
            elif choice == '5':
                print("\n👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid choice. Please enter 1-5.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            continue

if __name__ == "__main__":
    main() 