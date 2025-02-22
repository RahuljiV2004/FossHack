import os
import requests
import logging
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class SubdomainScanner:
    def __init__(self, wordlist_path="wordlist.txt"):
        self.wordlist_path = wordlist_path

    def scan(self, domain):
        results = {
            'subdomains': [],
            'error': None
        }

        try:
            # Step 1: Generate a wordlist (common subdomains + parsed from HTML)
            wordlist = self._generate_wordlist(domain)

            # Step 2: Use ThreadPoolExecutor for concurrent subdomain checking
            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = {
                    executor.submit(self._check_subdomain, f"{subdomain}.{domain}"): subdomain
                    for subdomain in wordlist
                }

                for future in as_completed(futures):
                    subdomain = futures[future]
                    try:
                        if future.result():
                            results['subdomains'].append(f"{subdomain}.{domain}")
                    except Exception as e:
                        logger.error(f"Error checking subdomain {subdomain}: {e}")

        except Exception as e:
            logger.error(f"Subdomain scan error: {e}")
            results['error'] = str(e)

        return results

    def _generate_wordlist(self, domain):
        """
        Generate a wordlist by combining common subdomains and words parsed from the target site.
        """
        wordlist = set()

        # Step 1: Add common subdomains
        common_subdomains = [
            "www", "mail", "ftp", "admin", "test", "dev", "api", "blog", "webmail", "support",
            "shop", "portal", "cdn", "static", "app", "beta", "staging", "m", "mobile", "secure"
        ]
        wordlist.update(common_subdomains)

        # Step 2: Extract subdomains from the HTML content of the target website
        try:
            # Fetch the HTML content of the target website
            response = requests.get(f"http://{domain}", timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all links in the HTML
            for link in soup.find_all('a', href=True):
                href = link['href']
                # Extract subdomains from URLs
                if domain in href:
                    subdomain = re.match(rf"(https?:\/\/)?([a-zA-Z0-9\-]+\.)?{domain}", href)
                    if subdomain and subdomain.group(2):
                        wordlist.add(subdomain.group(2).rstrip('.'))

            # Find subdomains in script tags
            for script in soup.find_all('script', src=True):
                src = script['src']
                if domain in src:
                    subdomain = re.match(rf"(https?:\/\/)?([a-zA-Z0-9\-]+\.)?{domain}", src)
                    if subdomain and subdomain.group(2):
                        wordlist.add(subdomain.group(2).rstrip('.'))

        except Exception as e:
            logger.error(f"Failed to extract subdomains from HTML: {e}")

        return list(wordlist)

    def _check_subdomain(self, subdomain):
        """
        Check if a subdomain exists by making an HTTP request.
        """
        try:
            response = requests.get(f"http://{subdomain}", timeout=5)
            if response.status_code == 200:
                return True
        except requests.RequestException:
            pass
        return False