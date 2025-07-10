#!/usr/bin/env python3
"""
Search API Implementation for Company Discovery
Uses SerpAPI to find software development companies in Middle Eastern countries.
"""

import os
import time
import logging
from typing import List, Dict
import requests
from visited_links_manager import visited_links_manager

logger = logging.getLogger(__name__)

class SerpAPISearcher:
    """Handles company search using SerpAPI."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('SERPAPI_KEY')
        self.base_url = "https://serpapi.com/search"
        
        # Use the global visited links manager
        self.visited_manager = visited_links_manager
        logger.info("SerpAPISearcher initialized with visited links tracking")
        
    def search_companies(self, country: str, max_results: int = 20) -> List[str]:
        """Search for software development companies using SerpAPI."""
        if not self.api_key:
            logger.warning("SerpAPI key not provided, using fallback method")
            return self._fallback_search(country, max_results)
        
        search_queries = [
            f"software development company {country}",
            f"web development company {country}",
            f"mobile app development {country}",
            f"IT services {country}",
            f"software house {country}"
        ]
        
        all_urls = []
        
        for query in search_queries:
            try:
                # Check if this search has been performed before
                if self.visited_manager.is_search_visited(query, search_type="serpapi_search"):
                    logger.info(f"Skipping already performed search: {query}")
                    continue
                
                # Mark search as visited
                self.visited_manager.mark_search_visited(
                    query, 
                    search_type="serpapi_search",
                    scraper_name="SerpAPISearcher",
                    metadata={'country': country}
                )
                
                params = {
                    'q': query,
                    'api_key': self.api_key,
                    'engine': 'google',
                    'num': max_results // len(search_queries),
                    'gl': self._get_country_code(country),
                    'hl': 'en'
                }
                
                response = requests.get(self.base_url, params=params)
                response.raise_for_status()
                
                data = response.json()
                
                if 'organic_results' in data:
                    for result in data['organic_results']:
                        if 'link' in result:
                            url = result['link']
                            # Filter out already visited URLs
                            if not self.visited_manager.is_link_visited(url):
                                all_urls.append(url)
                            else:
                                logger.info(f"Skipping already visited URL: {url}")
                
                # Rate limiting
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Error searching with SerpAPI for '{query}': {str(e)}")
                continue
        
        # Save visited data after searches
        self.visited_manager.save_all_data()
        
        return list(set(all_urls))[:max_results]
    
    def _get_country_code(self, country: str) -> str:
        """Get country code for search localization."""
        country_codes = {
            'Saudi Arabia': 'sa',
            'United Arab Emirates': 'ae',
            'Kuwait': 'kw',
            'Jordan': 'jo',
            'Oman': 'om'
        }
        return country_codes.get(country, 'us')
    
    def _fallback_search(self, country: str, max_results: int) -> List[str]:
        """Fallback search method when API is not available."""
        logger.info(f"Using fallback search for {country}")
        
        # Sample companies for demonstration
        fallback_companies = {
            'Saudi Arabia': [
                'https://www.stc.com.sa',
                'https://www.elm.sa',
                'https://www.ncb.com.sa',
                'https://www.sauditech.com.sa',
                'https://www.itida.gov.sa'
            ],
            'United Arab Emirates': [
                'https://www.etisalat.ae',
                'https://www.du.ae',
                'https://www.adnoc.ae',
                'https://www.emirates.com',
                'https://www.dubaitech.ae'
            ],
            'Kuwait': [
                'https://www.zain.com',
                'https://www.ooredoo.com.kw',
                'https://www.viva.com.kw'
            ],
            'Jordan': [
                'https://www.orange.jo',
                'https://www.zain.jo',
                'https://www.umniah.com'
            ],
            'Oman': [
                'https://www.omantel.om',
                'https://www.ooredoo.om'
            ]
        }
        
        return fallback_companies.get(country, [])[:max_results]

class BingSearcher:
    """Alternative searcher using Bing Search API."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('BING_SEARCH_KEY')
        self.base_url = "https://api.bing.microsoft.com/v7.0/search"
        
        # Use the global visited links manager
        self.visited_manager = visited_links_manager
        logger.info("BingSearcher initialized with visited links tracking")
        
    def search_companies(self, country: str, max_results: int = 20) -> List[str]:
        """Search for companies using Bing Search API."""
        if not self.api_key:
            logger.warning("Bing API key not provided")
            return []
        
        search_queries = [
            f"software development company {country}",
            f"web development {country}",
            f"mobile app development {country}"
        ]
        
        all_urls = []
        
        for query in search_queries:
            try:
                # Check if this search has been performed before
                if self.visited_manager.is_search_visited(query, search_type="bing_search"):
                    logger.info(f"Skipping already performed search: {query}")
                    continue
                
                # Mark search as visited
                self.visited_manager.mark_search_visited(
                    query, 
                    search_type="bing_search",
                    scraper_name="BingSearcher",
                    metadata={'country': country}
                )
                
                headers = {
                    'Ocp-Apim-Subscription-Key': self.api_key
                }
                
                params = {
                    'q': query,
                    'count': max_results // len(search_queries),
                    'mkt': 'en-US'
                }
                
                response = requests.get(self.base_url, headers=headers, params=params)
                response.raise_for_status()
                
                data = response.json()
                
                if 'webPages' in data and 'value' in data['webPages']:
                    for result in data['webPages']['value']:
                        if 'url' in result:
                            url = result['url']
                            # Filter out already visited URLs
                            if not self.visited_manager.is_link_visited(url):
                                all_urls.append(url)
                            else:
                                logger.info(f"Skipping already visited URL: {url}")
                
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Error searching with Bing API for '{query}': {str(e)}")
                continue
        
        # Save visited data after searches
        self.visited_manager.save_all_data()
        
        return list(set(all_urls))[:max_results]

def get_searcher(api_preference: str = 'serpapi') -> object:
    """Get appropriate searcher based on available API keys."""
    if api_preference == 'serpapi' and os.getenv('SERPAPI_KEY'):
        return SerpAPISearcher()
    elif api_preference == 'bing' and os.getenv('BING_SEARCH_KEY'):
        return BingSearcher()
    else:
        logger.info("No API keys found, using fallback searcher")
        return SerpAPISearcher()  # Uses fallback method 