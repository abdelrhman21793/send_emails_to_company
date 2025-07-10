#!/usr/bin/env python3
"""
Script to send CV emails to exactly 30 companies starting from the first unsent email.
"""

import sys
import os
from config import Config
from email_automation import send_emails_batch
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Send emails to exactly 30 companies."""
    
    print("=" * 60)
    print("Sending CV to 30 Companies")
    print("=" * 60)
    
    # Validate configuration
    config_errors = Config.validate_config()
    if config_errors:
        print("\n❌ Configuration errors found:")
        for error in config_errors:
            print(f"  - {error}")
        print("\nPlease fix these issues before running the script.")
        print("Make sure to set your email credentials in environment variables:")
        print("export SENDER_EMAIL='your_email@gmail.com'")
        print("export SENDER_PASSWORD='your_app_password'")
        return 1
    
    print("✅ Configuration validated successfully")
    print(f"📧 Sender email: {Config.SENDER_EMAIL}")
    print(f"📄 CV file: {Config.CV_PATH}")
    print(f"📊 Target: 30 emails")
    
    # Confirm before sending
    confirm = input("\nDo you want to proceed with sending emails to 30 companies? (y/N): ").strip().lower()
    if confirm != 'y' and confirm != 'yes':
        print("Operation cancelled.")
        return 0
    
    print("\n📧 Starting email sending to 30 companies...")
    
    try:
        # Send emails to exactly 30 companies
        sent_count = send_emails_batch(
            Config.SENDER_EMAIL,
            Config.SENDER_PASSWORD,
            Config.CV_PATH,
            max_emails=30  # Exactly 30 emails
        )
        
        print(f"\n✅ Email sending completed!")
        print(f"📈 Successfully sent: {sent_count} emails")
        print(f"📊 Target was: 30 emails")
        
        if sent_count < 30:
            print(f"⚠️  Note: Only {sent_count} emails were sent (possibly due to errors or no more unsent emails)")
        
    except Exception as e:
        logger.error(f"Error during email sending: {str(e)}")
        print(f"❌ Email sending failed: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 