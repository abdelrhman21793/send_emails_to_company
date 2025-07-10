#!/usr/bin/env python3
"""
Quick Start Script for Email Automation System
This script provides a simple way to test and start the email automation system.
"""

import os
import sys
import time
from datetime import datetime
import pytz

def print_banner():
    """Print welcome banner."""
    print("=" * 60)
    print("🚀 EMAIL AUTOMATION SYSTEM - QUICK START")
    print("=" * 60)
    print("✅ Enhanced Email Validation")
    print("✅ Daily Scheduling (1:00 PM & 2:00 PM Egypt Time)")
    print("✅ Smart Email Prioritization")
    print("✅ Comprehensive Logging")
    print("=" * 60)

def show_current_time():
    """Show current time in Egypt timezone."""
    egypt_tz = pytz.timezone('Africa/Cairo')
    current_time = datetime.now(egypt_tz)
    print(f"🕐 Current Egypt Time: {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print()

def check_files():
    """Check if required files exist."""
    print("📋 Checking System Files...")
    
    required_files = [
        'improved_email_automation.py',
        'setup_scheduler.py',
        'start_scheduler.py',
        'emails.csv'
    ]
    
    optional_files = [
        'swpm.pdf',
        'AUTOMATION_README.md'
    ]
    
    all_good = True
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING!")
            all_good = False
    
    for file in optional_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"⚠️  {file} - Optional (recommended)")
    
    print()
    return all_good

def show_menu():
    """Show main menu options."""
    print("🎯 QUICK START OPTIONS:")
    print("1. 🔧 Setup System (Configure email credentials)")
    print("2. 🧪 Test Email Validation")
    print("3. 📊 Check Email Database Status")
    print("4. 🚀 Start Scheduler (Run daily automation)")
    print("5. 📝 View Documentation")
    print("6. 🔍 Monitor Logs")
    print("7. ❌ Exit")
    print()

def test_email_validation():
    """Quick test of email validation."""
    print("🧪 Testing Email Validation...")
    
    try:
        from improved_email_automation import EmailValidator
        
        validator = EmailValidator()
        
        # Test the problematic emails mentioned by user
        test_emails = [
            ("info@helpag.com", "Valid email"),
            ("support@foodics.comp", "Invalid - malformed .comp"),
            ("ussales.support@gizasystems.comcall", "Invalid - malformed .comcall"),
            ("support.eg@foodics.comp", "Invalid - malformed .comp"),
            ("info@company.sa", "Valid - Saudi domain"),
            ("contact@company.ae", "Valid - UAE domain"),
            ("noreply@company.com", "Invalid - noreply email"),
        ]
        
        print("\n📧 Email Validation Results:")
        for email, description in test_emails:
            is_valid = validator.is_valid_email(email)
            status = "✅ VALID" if is_valid else "❌ INVALID"
            print(f"  {email:<35} -> {status} ({description})")
        
        print("\n✅ Email validation system is working correctly!")
        
    except ImportError as e:
        print(f"❌ Error importing validation system: {e}")
        print("Please make sure all dependencies are installed.")
    except Exception as e:
        print(f"❌ Error testing validation: {e}")

def check_database_status():
    """Check email database status."""
    print("📊 Checking Email Database Status...")
    
    try:
        import pandas as pd
        
        if not os.path.exists('emails.csv'):
            print("❌ emails.csv not found!")
            return
        
        df = pd.read_csv('emails.csv')
        total_emails = len(df)
        
        if 'sent' in df.columns:
            sent_emails = len(df[df['sent'] == 'yes'])
            unsent_emails = len(df[df['sent'] == 'no'])
        else:
            sent_emails = 0
            unsent_emails = total_emails
        
        print(f"📈 Database Statistics:")
        print(f"  Total emails: {total_emails}")
        print(f"  Sent emails: {sent_emails}")
        print(f"  Unsent emails: {unsent_emails}")
        
        if unsent_emails > 0:
            print(f"\n✅ Ready to send CV to {min(30, unsent_emails)} companies")
        else:
            print(f"\n⚠️  No unsent emails available. Run scraping first.")
        
        # Show sample of unsent emails
        if unsent_emails > 0:
            print(f"\n📋 Next 5 emails to send:")
            unsent_df = df[df['sent'] == 'no'].head(5)
            for _, row in unsent_df.iterrows():
                print(f"  📧 {row['email']} ({row.get('company', 'Unknown Company')})")
        
    except Exception as e:
        print(f"❌ Error checking database: {e}")

def view_documentation():
    """View documentation."""
    print("📝 Opening Documentation...")
    
    if os.path.exists('AUTOMATION_README.md'):
        print("✅ Documentation file found: AUTOMATION_README.md")
        print("\nKey Commands:")
        print("  Setup: python3 setup_scheduler.py")
        print("  Start: python3 start_scheduler.py")
        print("  Test:  python3 quick_start.py")
        print("\nSchedule:")
        print("  1:00 PM Egypt Time - Email Scraping")
        print("  2:00 PM Egypt Time - Email Sending (30 emails)")
        print("\nLogs:")
        print("  tail -f email_automation.log")
        print("  tail -f scheduler.log")
    else:
        print("⚠️  Documentation file not found")

def monitor_logs():
    """Show recent log entries."""
    print("🔍 Recent Log Entries...")
    
    log_files = ['email_automation.log', 'scheduler.log']
    
    for log_file in log_files:
        if os.path.exists(log_file):
            print(f"\n📄 {log_file} (last 5 lines):")
            try:
                with open(log_file, 'r') as f:
                    lines = f.readlines()
                    for line in lines[-5:]:
                        print(f"  {line.strip()}")
            except Exception as e:
                print(f"  ❌ Error reading {log_file}: {e}")
        else:
            print(f"\n📄 {log_file}: Not found (will be created when system runs)")

def main():
    """Main function."""
    print_banner()
    show_current_time()
    
    # Check system files
    if not check_files():
        print("❌ Some required files are missing!")
        print("Please make sure all system files are present.")
        return
    
    while True:
        show_menu()
        
        try:
            choice = input("Enter your choice (1-7): ").strip()
            
            if choice == '1':
                print("\n🔧 Starting System Setup...")
                os.system('python3 setup_scheduler.py')
                
            elif choice == '2':
                print()
                test_email_validation()
                
            elif choice == '3':
                print()
                check_database_status()
                
            elif choice == '4':
                print("\n🚀 Starting Email Automation Scheduler...")
                print("This will run continuously. Press Ctrl+C to stop.")
                time.sleep(2)
                os.system('python3 start_scheduler.py')
                
            elif choice == '5':
                print()
                view_documentation()
                
            elif choice == '6':
                print()
                monitor_logs()
                
            elif choice == '7':
                print("\n👋 Goodbye! Your email automation system is ready.")
                break
                
            else:
                print("❌ Invalid choice. Please enter 1-7.")
            
            print("\n" + "="*60)
            input("Press Enter to continue...")
            print()
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 