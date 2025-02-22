import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)

class BrokenLinkChecker:
    def __init__(self):
        self.visited_urls = set()
        self.broken_links = []

    def check_links(self, base_url):
        """
        Check for broken links on the given base URL.
        """
        try:
            # Start with the base URL
            self._crawl_and_check(base_url, base_url)
            return self.broken_links
        except Exception as e:
            logger.error(f"Error during broken link check: {e}")
            return [{'url': base_url, 'error': str(e)}]

    def _crawl_and_check(self, base_url, current_url):
        """
        Recursively crawl and check links on the website.
        """
        if current_url in self.visited_urls:
            return
        self.visited_urls.add(current_url)

        try:
            response = requests.get(current_url, timeout=10)
            if response.status_code != 200:
                self.broken_links.append({
                    'url': current_url,
                    'status_code': response.status_code,
                    'error': f"Broken link with status code {response.status_code}"
                })
                return

            # Parse the page for links
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', href=True)

            # Check all links on the page
            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = []
                for link in links:
                    full_url = urljoin(base_url, link['href'])
                    if full_url not in self.visited_urls:
                        futures.append(executor.submit(self._check_link, base_url, full_url))

                for future in as_completed(futures):
                    future.result()  # Wait for all checks to complete

        except requests.RequestException as e:
            self.broken_links.append({
                'url': current_url,
                'error': str(e)
            })

    def _check_link(self, base_url, url):
        """
        Check if a link is broken.
        """
        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                self.broken_links.append({
                    'url': url,
                    'status_code': response.status_code,
                    'error': f"Broken link with status code {response.status_code}"
                })
        except requests.RequestException as e:
            self.broken_links.append({
                'url': url,
                'error': str(e)
            })