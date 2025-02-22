import requests
import logging

logger = logging.getLogger(__name__)

class HeadersScanner:
    def scan(self, domain):
        results = {
            'headers': {},
            'error': None
        }

        try:
            # Send a GET request to the domain
            response = requests.get(f"http://{domain}")
            results['headers'] = dict(response.headers)
        except Exception as e:
            logger.error(f"Headers scan error for {domain}: {e}")
            results['error'] = str(e)
        
        return results