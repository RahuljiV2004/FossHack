import whois
import logging
from datetime import datetime
import subprocess

logger = logging.getLogger(__name__)

class DomainScanner:import whois
import logging
from datetime import datetime
import subprocess
import tempfile
import os

logger = logging.getLogger(__name__)

class DomainScanner:
    def scan(self, domain):
        results = {
            'registrar': None,
            'creation_date': None,
            'expiration_date': None,
            'registrant': None,
            'subdomains': [],
            'error': None
        }
        
        try:
            # Get WHOIS information with a timeout
            domain_info = whois.whois(domain, timeout=10)
            
            results['registrar'] = domain_info.registrar
            results['creation_date'] = str(domain_info.creation_date)
            results['expiration_date'] = str(domain_info.expiration_date)
            results['registrant'] = domain_info.registrant
            
            # Run Sublist3r for subdomain enumeration
            subdomains = self._run_sublister(domain)
            results['subdomains'] = subdomains
            
        except Exception as e:
            logger.error(f"Domain scan error for {domain}: {e}")
            results['error'] = str(e)
            
        return results
    
    def _run_sublister(self, domain):
        try:
            with tempfile.TemporaryDirectory() as tmp_dir:
                output_file = os.path.join(tmp_dir, 'subdomains.txt')
                cmd = f"sublist3r -d {domain} -o {output_file}"
                subprocess.run(cmd, shell=True, check=True)
                
                with open(output_file, 'r') as f:
                    subdomains = f.read().splitlines()
                
                return subdomains
        except Exception as e:
            logger.error(f"Sublist3r error for {domain}: {e}")
            return []
        
import whois
import logging
from datetime import datetime
import subprocess
import tempfile
import os

logger = logging.getLogger(__name__)

class DomainScanner:
    def scan(self, domain):
        results = {
            'registrar': None,
            'creation_date': None,
            'expiration_date': None,
            'registrant': None,
            'subdomains': [],
            'error': None
        }
        
        try:
            # Get WHOIS information with a timeout
            domain_info = whois.whois(domain, timeout=10)
            
            results['registrar'] = domain_info.registrar
            results['creation_date'] = str(domain_info.creation_date)
            results['expiration_date'] = str(domain_info.expiration_date)
            results['registrant'] = domain_info.registrant
            
            # Run Sublist3r for subdomain enumeration
            subdomains = self._run_sublister(domain)
            results['subdomains'] = subdomains
            
        except Exception as e:
            logger.error(f"Domain scan error for {domain}: {e}")
            results['error'] = str(e)
            
        return results
    
    def _run_sublister(self, domain):
        try:
            with tempfile.TemporaryDirectory() as tmp_dir:
                output_file = os.path.join(tmp_dir, 'subdomains.txt')
                cmd = f"sublist3r -d {domain} -o {output_file}"
                subprocess.run(cmd, shell=True, check=True)
                
                with open(output_file, 'r') as f:
                    subdomains = f.read().splitlines()
                
                return subdomains
        except Exception as e:
            logger.error(f"Sublist3r error for {domain}: {e}")
            return []
    def scan(self, domain):
        results = {
            'registrar': None,
            'creation_date': None,
            'expiration_date': None,
            'registrant': None,
            'subdomains': [],
            'error': None
        }
        
        try:
            # Get WHOIS information with a timeout
            domain_info = whois.whois(domain)
            
            results['registrar'] = domain_info.registrar
            results['creation_date'] = str(domain_info.creation_date)
            results['expiration_date'] = str(domain_info.expiration_date)
            results['registrant'] = domain_info.registrant
            
            # Run Sublist3r for subdomain enumeration
            subdomains = self._run_sublister(domain)
            results['subdomains'] = subdomains
            
        except Exception as e:
            logger.error(f"Domain scan error for {domain}: {e}")
            results['error'] = str(e)
            
        return results
    
    def _run_sublister(self, domain):
        try:
            cmd = f"sublist3r -d {domain} -o /tmp/subdomains.txt"
            subprocess.run(cmd, shell=True, check=True)
            
            with open('/tmp/subdomains.txt', 'r') as f:
                subdomains = f.read().splitlines()
            
            return subdomains
        except Exception as e:
            logger.error(f"Sublist3r error for {domain}: {e}")
            return []