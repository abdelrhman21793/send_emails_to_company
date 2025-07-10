#!/usr/bin/env python3
"""
Setup script to configure email credentials and send CV to 30 companies.
"""

import sys
import os
import getpass
from email_automation import send_emails_batch
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Setup and send emails to exactly 30 companies."""
    
    print("=" * 60)
    print("Setup and Send CV to 30 Companies")
    print("=" * 60)
    
    # Check for CV file
    cv_files = [f for f in os.listdir('.') if f.endswith('.pdf')]
    if not cv_files:
        print("❌ No PDF files found in current directory.")
        print("Please make sure your CV is in PDF format in this directory.")
        return 1
    
    print(f"📄 Found PDF files: {', '.join(cv_files)}")
    
    # Let user choose CV file
    if len(cv_files) == 1:
        cv_path = cv_files[0]
        print(f"📄 Using CV file: {cv_path}")
    else:
        print("\nSelect your CV file:")
        for i, file in enumerate(cv_files, 1):
            print(f"  {i}. {file}")
        
        try:
            choice = int(input("Enter choice: ")) - 1
            cv_path = cv_files[choice]
            print(f"📄 Using CV file: {cv_path}")
        except (ValueError, IndexError):
            print("❌ Invalid choice.")
            return 1
    
    # Get email credentials
    print("\n📧 Email Setup:")
    print("Please enter your Gmail credentials (app password required)")
    print("For Gmail app password setup, visit: https://support.google.com/accounts/answer/185833")
    
    sender_email = input("Enter your Gmail address: ").strip()
    if not sender_email:
        print("❌ Email address is required.")
        return 1
    
    sender_password = getpass.getpass("Enter your Gmail app password: ").strip()
    if not sender_password:
        print("❌ Password is required.")
        return 1
    
    print(f"\n✅ Configuration ready:")
    print(f"📧 Email: {sender_email}")
    print(f"📄 CV: {cv_path}")
    print(f"📊 Target: 30 emails")
    
    # Confirm before sending
    confirm = input("\nDo you want to proceed with sending emails to 30 companies? (y/N): ").strip().lower()
    if confirm != 'y' and confirm != 'yes':
        print("Operation cancelled.")
        return 0
    
    print("\n📧 Starting email sending to 30 companies...")
    print("This will take approximately 5-10 minutes (with delays between emails)...")
    
    try:
        # Send emails to exactly 30 companies
        sent_count = send_emails_batch(
            sender_email,
            sender_password,
            cv_path,
            max_emails=30  # Exactly 30 emails
        )
        
        print(f"\n✅ Email sending completed!")
        print(f"📈 Successfully sent: {sent_count} emails")
        print(f"📊 Target was: 30 emails")
        
        if sent_count < 30:
            print(f"⚠️  Note: Only {sent_count} emails were sent")
            print("This could be due to:")
            print("  - Network errors")
            print("  - Invalid email addresses")
            print("  - No more unsent emails in the database")
        
        # Show some statistics
        print(f"\n📊 Email sending summary:")
        print(f"  - Emails processed: 30")
        print(f"  - Emails sent successfully: {sent_count}")
        print(f"  - Success rate: {(sent_count/30)*100:.1f}%")
        
    except Exception as e:
        logger.error(f"Error during email sending: {str(e)}")
        print(f"❌ Email sending failed: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 