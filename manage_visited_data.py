#!/usr/bin/env python3
"""
Manage Visited Data - Tool to manage visited links and companies tracking
"""

import json
import os
import argparse
from datetime import datetime
from dynamic_company_finder import DynamicCompanyFinder

def show_stats():
    """Show statistics about visited data."""
    finder = DynamicCompanyFinder()
    stats = finder.get_visited_stats()
    
    print("=== VISITED DATA STATISTICS ===")
    print(f"Visited links: {stats['visited_links_count']}")
    print(f"Visited companies: {stats['visited_companies_count']}")
    print(f"Links file exists: {stats['visited_links_file_exists']}")
    print(f"Companies file exists: {stats['visited_companies_file_exists']}")
    
    # Show file modification times if they exist
    if stats['visited_links_file_exists']:
        try:
            with open('visited_links.json', 'r') as f:
                data = json.load(f)
                last_updated = data.get('last_updated', 'Unknown')
                print(f"Links file last updated: {last_updated}")
        except Exception as e:
            print(f"Could not read links file: {e}")
    
    if stats['visited_companies_file_exists']:
        try:
            with open('visited_companies.json', 'r') as f:
                data = json.load(f)
                last_updated = data.get('last_updated', 'Unknown')
                print(f"Companies file last updated: {last_updated}")
        except Exception as e:
            print(f"Could not read companies file: {e}")

def clear_all_data():
    """Clear all visited data."""
    finder = DynamicCompanyFinder()
    
    confirmation = input("Are you sure you want to clear ALL visited data? This cannot be undone. (yes/no): ")
    if confirmation.lower() == 'yes':
        finder.clear_visited_data()
        print("✅ All visited data has been cleared.")
    else:
        print("❌ Operation cancelled.")

def export_data():
    """Export visited data to a backup file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"visited_data_backup_{timestamp}.json"
    
    try:
        visited_links = set()
        visited_companies = set()
        
        # Load visited links
        if os.path.exists('visited_links.json'):
            with open('visited_links.json', 'r') as f:
                data = json.load(f)
                visited_links = set(data.get('visited_links', []))
        
        # Load visited companies
        if os.path.exists('visited_companies.json'):
            with open('visited_companies.json', 'r') as f:
                data = json.load(f)
                visited_companies = set(data.get('visited_companies', []))
        
        # Create backup
        backup_data = {
            'export_date': datetime.now().isoformat(),
            'visited_links': list(visited_links),
            'visited_companies': list(visited_companies),
            'total_links': len(visited_links),
            'total_companies': len(visited_companies)
        }
        
        with open(backup_file, 'w') as f:
            json.dump(backup_data, f, indent=2)
        
        print(f"✅ Visited data exported to: {backup_file}")
        print(f"   - {len(visited_links)} visited links")
        print(f"   - {len(visited_companies)} visited companies")
        
    except Exception as e:
        print(f"❌ Error exporting data: {e}")

def import_data(backup_file):
    """Import visited data from a backup file."""
    if not os.path.exists(backup_file):
        print(f"❌ Backup file not found: {backup_file}")
        return
    
    try:
        with open(backup_file, 'r') as f:
            backup_data = json.load(f)
        
        visited_links = backup_data.get('visited_links', [])
        visited_companies = backup_data.get('visited_companies', [])
        
        print(f"Backup contains:")
        print(f"  - {len(visited_links)} visited links")
        print(f"  - {len(visited_companies)} visited companies")
        print(f"  - Created: {backup_data.get('export_date', 'Unknown')}")
        
        confirmation = input("Import this data? This will merge with existing data. (yes/no): ")
        if confirmation.lower() != 'yes':
            print("❌ Import cancelled.")
            return
        
        # Load existing data
        finder = DynamicCompanyFinder()
        
        # Merge data
        finder.visited_links.update(visited_links)
        finder.visited_companies.update(visited_companies)
        
        # Save merged data
        finder._save_visited_links()
        finder._save_visited_companies()
        
        print("✅ Data imported successfully!")
        
        # Show final stats
        stats = finder.get_visited_stats()
        print(f"Total visited links: {stats['visited_links_count']}")
        print(f"Total visited companies: {stats['visited_companies_count']}")
        
    except Exception as e:
        print(f"❌ Error importing data: {e}")

def list_recent_links(limit=20):
    """List recent visited links."""
    if not os.path.exists('visited_links.json'):
        print("No visited links file found.")
        return
    
    try:
        with open('visited_links.json', 'r') as f:
            data = json.load(f)
            links = data.get('visited_links', [])
        
        print(f"=== RECENT VISITED LINKS (Last {min(limit, len(links))}) ===")
        for i, link in enumerate(links[-limit:], 1):
            print(f"{i:2d}. {link}")
        
        if len(links) > limit:
            print(f"\n... and {len(links) - limit} more links")
        
    except Exception as e:
        print(f"Error reading links: {e}")

def list_recent_companies(limit=20):
    """List recent visited companies."""
    if not os.path.exists('visited_companies.json'):
        print("No visited companies file found.")
        return
    
    try:
        with open('visited_companies.json', 'r') as f:
            data = json.load(f)
            companies = data.get('visited_companies', [])
        
        print(f"=== RECENT VISITED COMPANIES (Last {min(limit, len(companies))}) ===")
        for i, company in enumerate(companies[-limit:], 1):
            # Parse company key to show name and website
            parts = company.split('_', 1)
            if len(parts) == 2:
                name, website = parts
                website = website if website != 'no_website' else 'No website'
                print(f"{i:2d}. {name.title()} - {website}")
            else:
                print(f"{i:2d}. {company}")
        
        if len(companies) > limit:
            print(f"\n... and {len(companies) - limit} more companies")
        
    except Exception as e:
        print(f"Error reading companies: {e}")

def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(description="Manage visited links and companies data")
    
    parser.add_argument('action', choices=['stats', 'clear', 'export', 'import', 'links', 'companies'],
                       help='Action to perform')
    parser.add_argument('--file', help='Backup file for import operation')
    parser.add_argument('--limit', type=int, default=20, help='Number of items to show (default: 20)')
    
    args = parser.parse_args()
    
    if args.action == 'stats':
        show_stats()
    elif args.action == 'clear':
        clear_all_data()
    elif args.action == 'export':
        export_data()
    elif args.action == 'import':
        if not args.file:
            print("❌ Please specify a backup file with --file")
        else:
            import_data(args.file)
    elif args.action == 'links':
        list_recent_links(args.limit)
    elif args.action == 'companies':
        list_recent_companies(args.limit)

if __name__ == "__main__":
    main() 