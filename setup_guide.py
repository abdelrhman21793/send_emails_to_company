#!/usr/bin/env python3
"""
Setup Guide for Email Automation System
This script helps you configure the email automation system step by step.
"""

import os
import sys
import getpass

def main():
    """Main setup function."""
    print("=" * 70)
    print("Email Automation System - Setup Guide")
    print("=" * 70)
    
    print("\n🚀 Welcome to the Email Automation Setup!")
    print("This guide will help you configure the system step by step.\n")
    
    # Check prerequisites
    print("📋 Checking prerequisites...")
    
    # Check CV file
    cv_files = [f for f in os.listdir('.') if f.endswith('.pdf')]
    if cv_files:
        print(f"✅ CV file found: {cv_files[0]}")
        cv_path = cv_files[0]
    else:
        print("❌ No PDF CV file found in current directory")
        cv_path = input("Enter path to your CV file (or press Enter to skip): ").strip()
        if not cv_path:
            cv_path = "cv.pdf"
    
    # Check Python packages
    try:
        import requests, bs4, pandas
        print("✅ Required Python packages installed")
    except ImportError as e:
        print(f"❌ Missing packages: {e}")
        print("Run: pip install -r requirements.txt")
        return 1
    
    print("\n" + "=" * 50)
    print("GMAIL SETUP INSTRUCTIONS")
    print("=" * 50)
    
    print("""
To use Gmail for sending emails, you need to:

1. 🔐 Enable 2-Factor Authentication:
   - Go to https://myaccount.google.com/security
   - Enable 2-Step Verification
   
2. 📧 Generate App Password:
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and generate password
   - Copy the 16-character password (not your regular password!)
   
3. 📝 Configure Environment Variables:
   - Set SENDER_EMAIL to your Gmail address
   - Set SENDER_PASSWORD to the App Password (not regular password)
""")
    
    # Get user input
    print("\n" + "=" * 50)
    print("CONFIGURATION")
    print("=" * 50)
    
    email = input("Enter your Gmail address: ").strip()
    if email:
        print(f"✅ Email set to: {email}")
    else:
        print("⚠️  Email not provided - you'll need to set SENDER_EMAIL environment variable")
        email = "your_email@gmail.com"
    
    print("\nFor the App Password:")
    print("- Go to https://myaccount.google.com/apppasswords")
    print("- Generate a new app password for 'Mail'")
    print("- Copy the 16-character password")
    
    app_password = getpass.getpass("Enter your Gmail App Password (hidden): ").strip()
    if app_password:
        print("✅ App password provided")
    else:
        print("⚠️  App password not provided - you'll need to set SENDER_PASSWORD environment variable")
        app_password = "your_app_password"
    
    # Create environment setup script
    env_content = f"""#!/bin/bash
# Email Automation Environment Setup
# Run this script with: source setup_env.sh

export SENDER_EMAIL="{email}"
export SENDER_PASSWORD="{app_password}"
export CV_PATH="{cv_path}"
export CSV_FILE="emails.csv"
export LOG_FILE="email_automation.log"
export MAX_SCRAPE_EMAILS="50"
export MAX_SEND_EMAILS="30"
export REQUEST_DELAY="2"
export EMAIL_SEND_DELAY="10"

# Optional API Keys (for better search results)
# export SERPAPI_KEY="your_serpapi_key_here"
# export BING_SEARCH_KEY="your_bing_search_key_here"
export SEARCH_API_PREFERENCE="serpapi"

echo "Environment variables set for Email Automation!"
echo "CV Path: $CV_PATH"
echo "Email: $SENDER_EMAIL"
echo "Now you can run: python3 run_automation.py"
"""
    
    with open("setup_env.sh", "w") as f:
        f.write(env_content)
    
    print(f"\n✅ Created setup_env.sh")
    
    # Create test script
    test_content = f"""#!/usr/bin/env python3
import os
os.environ['SENDER_EMAIL'] = '{email}'
os.environ['SENDER_PASSWORD'] = '{app_password}'
os.environ['CV_PATH'] = '{cv_path}'

from email_automation import scrape_companies_and_emails

print("Testing email scraping...")
result = scrape_companies_and_emails(max_emails=5)
print(f"Found {{result}} emails")
"""
    
    with open("test_setup.py", "w") as f:
        f.write(test_content)
    
    print(f"✅ Created test_setup.py")
    
    print("\n" + "=" * 50)
    print("NEXT STEPS")
    print("=" * 50)
    
    print("""
1. 🔧 Set up environment:
   source setup_env.sh

2. 🧪 Test the setup:
   python3 test_setup.py

3. 🚀 Run full automation:
   python3 run_automation.py

4. 📊 For better results, get API keys:
   - SerpAPI: https://serpapi.com/ (recommended)
   - Bing Search: https://azure.microsoft.com/en-us/services/cognitive-services/bing-web-search-api/

5. ⏰ Set up automation (optional):
   - Add to crontab: 0 9 * * * cd /path/to/script && source setup_env.sh && python3 email_automation.py
""")
    
    print("\n" + "=" * 50)
    print("IMPORTANT NOTES")
    print("=" * 50)
    
    print("""
⚠️  LEGAL & ETHICAL CONSIDERATIONS:
- Use only for legitimate job applications
- Respect website rate limits and robots.txt
- Follow email marketing best practices
- Ensure compliance with local laws

🔒 SECURITY:
- Keep your App Password secure
- Don't share your credentials
- Use environment variables, not hardcoded values

📈 OPTIMIZATION:
- Start with small batches (10-20 emails)
- Monitor email deliverability
- Adjust delays if needed
- Use API keys for better search results
""")
    
    print("\n🎉 Setup complete! You're ready to start job hunting!")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 