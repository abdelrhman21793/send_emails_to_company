#!/usr/bin/env python3
"""
Visited Links Manager - Shared utility for managing visited links across all scrapers
This implementation provides a centralized way to track visited URLs and companies
to improve performance and avoid scraping blocks.
"""

import json
import os
import logging
from typing import Set, Optional, Dict, Any
from datetime import datetime, timedelta
from urllib.parse import urlparse, urljoin
import hashlib

logger = logging.getLogger(__name__)

class VisitedLinksManager:
    """Centralized manager for tracking visited links and companies across all scrapers."""
    
    def __init__(self, base_filename: str = "visited_links", expire_days: int = 30):
        """
        Initialize the visited links manager.
        
        Args:
            base_filename: Base filename for storing visited data
            expire_days: Number of days after which visited links expire (0 = never expire)
        """
        self.base_filename = base_filename
        self.expire_days = expire_days
        
        # File paths for different types of visited data
        self.visited_links_file = f"{base_filename}_urls.json"
        self.visited_companies_file = f"{base_filename}_companies.json"
        self.visited_searches_file = f"{base_filename}_searches.json"
        
        # In-memory storage for fast lookups
        self.visited_links = self._load_visited_links()
        self.visited_companies = self._load_visited_companies()
        self.visited_searches = self._load_visited_searches()
        
        # Clean up expired entries on initialization
        self._cleanup_expired_entries()
        
        logger.info(f"VisitedLinksManager initialized:")
        logger.info(f"  - {len(self.visited_links)} visited links loaded")
        logger.info(f"  - {len(self.visited_companies)} visited companies loaded")
        logger.info(f"  - {len(self.visited_searches)} visited searches loaded")
    
    def _load_visited_links(self) -> Dict[str, Dict]:
        """Load previously visited links from file."""
        if os.path.exists(self.visited_links_file):
            try:
                with open(self.visited_links_file, 'r') as f:
                    data = json.load(f)
                    return data.get('visited_links', {})
            except Exception as e:
                logger.warning(f"Could not load visited links: {e}")
        return {}
    
    def _load_visited_companies(self) -> Dict[str, Dict]:
        """Load previously visited companies from file."""
        if os.path.exists(self.visited_companies_file):
            try:
                with open(self.visited_companies_file, 'r') as f:
                    data = json.load(f)
                    return data.get('visited_companies', {})
            except Exception as e:
                logger.warning(f"Could not load visited companies: {e}")
        return {}
    
    def _load_visited_searches(self) -> Dict[str, Dict]:
        """Load previously visited search queries from file."""
        if os.path.exists(self.visited_searches_file):
            try:
                with open(self.visited_searches_file, 'r') as f:
                    data = json.load(f)
                    return data.get('visited_searches', {})
            except Exception as e:
                logger.warning(f"Could not load visited searches: {e}")
        return {}
    
    def _normalize_url(self, url: str) -> str:
        """Normalize URL for consistent comparison."""
        if not url:
            return ""
        
        # Remove trailing slashes, convert to lowercase, strip whitespace
        normalized = url.lower().strip().rstrip('/')
        
        # Remove common URL parameters that don't affect content
        if '?' in normalized:
            base_url = normalized.split('?')[0]
            # Only keep essential parameters
            return base_url
        
        return normalized
    
    def _create_company_key(self, company_name: str, website: Optional[str] = None) -> str:
        """Create a unique key for a company."""
        name_clean = company_name.lower().strip() if company_name else ""
        website_clean = self._normalize_url(website) if website else "no_website"
        
        # Create a hash to handle very long names/urls
        key_string = f"{name_clean}_{website_clean}"
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def _create_search_key(self, search_query: str, search_type: str = "general") -> str:
        """Create a unique key for a search query."""
        query_clean = search_query.lower().strip()
        key_string = f"{search_type}_{query_clean}"
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def _is_expired(self, timestamp: str) -> bool:
        """Check if a timestamp is expired based on expire_days setting."""
        if self.expire_days <= 0:
            return False  # Never expire
        
        try:
            visit_time = datetime.fromisoformat(timestamp)
            expiry_time = datetime.now() - timedelta(days=self.expire_days)
            return visit_time < expiry_time
        except Exception:
            return True  # If we can't parse the timestamp, consider it expired
    
    def _cleanup_expired_entries(self):
        """Remove expired entries from all collections."""
        if self.expire_days <= 0:
            return  # No expiration
        
        # Clean up visited links
        expired_links = []
        for url, data in self.visited_links.items():
            if self._is_expired(data.get('timestamp', '')):
                expired_links.append(url)
        
        for url in expired_links:
            del self.visited_links[url]
        
        # Clean up visited companies
        expired_companies = []
        for key, data in self.visited_companies.items():
            if self._is_expired(data.get('timestamp', '')):
                expired_companies.append(key)
        
        for key in expired_companies:
            del self.visited_companies[key]
        
        # Clean up visited searches
        expired_searches = []
        for key, data in self.visited_searches.items():
            if self._is_expired(data.get('timestamp', '')):
                expired_searches.append(key)
        
        for key in expired_searches:
            del self.visited_searches[key]
        
        if expired_links or expired_companies or expired_searches:
            logger.info(f"Cleaned up {len(expired_links)} expired links, "
                       f"{len(expired_companies)} expired companies, "
                       f"{len(expired_searches)} expired searches")
    
    def is_link_visited(self, url: str) -> bool:
        """Check if a link has been visited before."""
        normalized_url = self._normalize_url(url)
        if not normalized_url:
            return False
        
        data = self.visited_links.get(normalized_url)
        if not data:
            return False
        
        # Check if expired
        if self._is_expired(data.get('timestamp', '')):
            # Remove expired entry
            del self.visited_links[normalized_url]
            return False
        
        return True
    
    def mark_link_visited(self, url: str, scraper_name: str = "unknown", metadata: Optional[Dict] = None):
        """Mark a link as visited."""
        normalized_url = self._normalize_url(url)
        if not normalized_url:
            return
        
        visit_data = {
            'timestamp': datetime.now().isoformat(),
            'scraper': scraper_name,
            'visit_count': self.visited_links.get(normalized_url, {}).get('visit_count', 0) + 1
        }
        
        if metadata:
            visit_data.update(metadata)
        
        self.visited_links[normalized_url] = visit_data
    
    def is_company_visited(self, company_name: str, website: Optional[str] = None) -> bool:
        """Check if a company has been visited before."""
        company_key = self._create_company_key(company_name, website)
        
        data = self.visited_companies.get(company_key)
        if not data:
            return False
        
        # Check if expired
        if self._is_expired(data.get('timestamp', '')):
            # Remove expired entry
            del self.visited_companies[company_key]
            return False
        
        return True
    
    def mark_company_visited(self, company_name: str, website: Optional[str] = None, 
                           scraper_name: str = "unknown", metadata: Optional[Dict] = None):
        """Mark a company as visited."""
        company_key = self._create_company_key(company_name, website)
        
        visit_data = {
            'timestamp': datetime.now().isoformat(),
            'scraper': scraper_name,
            'company_name': company_name,
            'website': website,
            'visit_count': self.visited_companies.get(company_key, {}).get('visit_count', 0) + 1
        }
        
        if metadata:
            visit_data.update(metadata)
        
        self.visited_companies[company_key] = visit_data
    
    def is_search_visited(self, search_query: str, search_type: str = "general") -> bool:
        """Check if a search query has been performed before."""
        search_key = self._create_search_key(search_query, search_type)
        
        data = self.visited_searches.get(search_key)
        if not data:
            return False
        
        # Check if expired
        if self._is_expired(data.get('timestamp', '')):
            # Remove expired entry
            del self.visited_searches[search_key]
            return False
        
        return True
    
    def mark_search_visited(self, search_query: str, search_type: str = "general", 
                          scraper_name: str = "unknown", metadata: Optional[Dict] = None):
        """Mark a search query as performed."""
        search_key = self._create_search_key(search_query, search_type)
        
        visit_data = {
            'timestamp': datetime.now().isoformat(),
            'scraper': scraper_name,
            'search_query': search_query,
            'search_type': search_type,
            'visit_count': self.visited_searches.get(search_key, {}).get('visit_count', 0) + 1
        }
        
        if metadata:
            visit_data.update(metadata)
        
        self.visited_searches[search_key] = visit_data
    
    def save_all_data(self):
        """Save all visited data to files."""
        try:
            # Save visited links
            links_data = {
                'visited_links': self.visited_links,
                'last_updated': datetime.now().isoformat(),
                'total_links': len(self.visited_links)
            }
            with open(self.visited_links_file, 'w') as f:
                json.dump(links_data, f, indent=2)
            
            # Save visited companies
            companies_data = {
                'visited_companies': self.visited_companies,
                'last_updated': datetime.now().isoformat(),
                'total_companies': len(self.visited_companies)
            }
            with open(self.visited_companies_file, 'w') as f:
                json.dump(companies_data, f, indent=2)
            
            # Save visited searches
            searches_data = {
                'visited_searches': self.visited_searches,
                'last_updated': datetime.now().isoformat(),
                'total_searches': len(self.visited_searches)
            }
            with open(self.visited_searches_file, 'w') as f:
                json.dump(searches_data, f, indent=2)
            
            logger.info(f"Saved visited data: {len(self.visited_links)} links, "
                       f"{len(self.visited_companies)} companies, "
                       f"{len(self.visited_searches)} searches")
        except Exception as e:
            logger.error(f"Could not save visited data: {e}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about visited data."""
        return {
            'total_links': len(self.visited_links),
            'total_companies': len(self.visited_companies),
            'total_searches': len(self.visited_searches),
            'expire_days': self.expire_days,
            'files': {
                'links_file': self.visited_links_file,
                'companies_file': self.visited_companies_file,
                'searches_file': self.visited_searches_file
            }
        }
    
    def clear_all_data(self):
        """Clear all visited data (use with caution)."""
        self.visited_links.clear()
        self.visited_companies.clear()
        self.visited_searches.clear()
        
        # Remove files
        for file_path in [self.visited_links_file, self.visited_companies_file, self.visited_searches_file]:
            if os.path.exists(file_path):
                os.remove(file_path)
        
        logger.info("All visited data cleared")
    
    def export_data(self, filename: Optional[str] = None) -> str:
        """Export all visited data to a backup file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"visited_data_backup_{timestamp}.json"
        
        try:
            backup_data = {
                'export_date': datetime.now().isoformat(),
                'visited_links': self.visited_links,
                'visited_companies': self.visited_companies,
                'visited_searches': self.visited_searches,
                'statistics': self.get_statistics()
            }
            
            with open(filename, 'w') as f:
                json.dump(backup_data, f, indent=2)
            
            logger.info(f"Visited data exported to: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Error exporting data: {e}")
            return ""


# Global instance for easy access
visited_links_manager = VisitedLinksManager() 