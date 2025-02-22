import whois
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class DomainScanner:
    def scan(self, domain):
        results = {
            'registrar': None,
            'creation_date': None,
            'expiration_date': None,
            'registrant': None,
            'subdomains': [],  # Sublist3r is commented out, so this will always be empty
            'error': None
        }

        try:
            # Get WHOIS information
            domain_info = whois.whois(domain)
            
            results['registrar'] = domain_info.registrar
            results['creation_date'] = str(domain_info.creation_date)
            results['expiration_date'] = str(domain_info.expiration_date)
            results['registrant'] = domain_info.registrant
            
            # Sublist3r is commented out, so no subdomains will be fetched
            # subdomains = self._run_sublister(domain)
            # results['subdomains'] = subdomains
            
        except Exception as e:
            logger.error(f"Domain scan error for {domain}: {e}")
            results['error'] = str(e)
            
        return results
    
    # Comment out the Sublist3r function
    # def _run_sublister(self, domain):
    #     try:
    #         cmd = f"sublist3r -d {domain} -o /tmp/subdomains.txt"
    #         subprocess.run(cmd, shell=True, check=True)
            
    #         with open('/tmp/subdomains.txt', 'r') as f:
    #             subdomains = f.read().splitlines()
            
    #         return subdomains
    #     except Exception as e:
    #         logger.error(f"Sublist3r error for {domain}: {e}")
    #         return []