import requests
import logging

logger = logging.getLogger(__name__)

class VulnerabilityScanner:
    def scan(self, domain, port_scan_results):
        vulnerabilities = []
        
        try:
            # Check for common vulnerabilities based on open ports
            for port in port_scan_results['open_ports']:
                service = port_scan_results['services'].get(port, {})
                
                # Check for known vulnerabilities in the service
                vuln_info = self._check_service_vulnerabilities(
                    domain, port, service.get('name'), 
                    service.get('product'), service.get('version')
                )
                
                if vuln_info:
                    vulnerabilities.extend(vuln_info)
            
            # Run a basic HTTP header check for vulnerabilities
            http_vulns = self._check_http_headers(domain)
            if http_vulns:
                vulnerabilities.extend(http_vulns)
                
        except Exception as e:
            logger.error(f"Vulnerability scan error for {domain}: {e}")
            vulnerabilities.append({
                'title': 'Scan Error',
                'risk_level': 'Unknown',
                'description': str(e),
                'exploitation': 'N/A',
                'mitigation': 'N/A'
            })
            
        return vulnerabilities
    
    def _check_service_vulnerabilities(self, domain, port, service_name, product, version):
        vulns = []
        
        # Check for vulnerable versions of software
        if product and version:
            if self._is_vulnerable_version(product, version):
                vulns.append({
                    'title': f'Vulnerable {product} version',
                    'risk_level': 'High',
                    'description': f'Running vulnerable version {version} of {product}.',
                    'exploitation': 'Multiple known exploits available for this version.',
                    'mitigation': 'Upgrade to the latest version of the software.'
                })
                
        return vulns
    
    def _check_http_headers(self, domain):
        vulns = []
        
        try:
            # Example: Check for missing security headers
            headers = self._get_http_headers(domain)
            
            if 'X-Frame-Options' not in headers:
                vulns.append({
                    'title': 'Missing X-Frame-Options Header',
                    'risk_level': 'Medium',
                    'description': 'The X-Frame-Options header is missing, making the site vulnerable to clickjacking attacks.',
                    'exploitation': 'Clickjacking',
                    'mitigation': 'Add X-Frame-Options header with DENY or SAMEORIGIN'
                })
            
            if 'Content-Security-Policy' not in headers:
                vulns.append({
                    'title': 'Missing Content-Security-Policy Header',
                    'risk_level': 'High',
                    'description': 'The Content-Security-Policy header is missing, making the site vulnerable to XSS attacks.',
                    'exploitation': 'Cross-Site Scripting (XSS)',
                    'mitigation': 'Add Content-Security-Policy header'
                })
                
        except Exception as e:
            logger.error(f"HTTP header check error for {domain}: {e}")
        
        return vulns
    
    def _get_http_headers(self, domain):
        response = requests.get(f"http://{domain}")
        return response.headers
    
    def _is_vulnerable_version(self, product, version):
        # Placeholder for version vulnerability check
        # You can integrate with a vulnerability database like CVE or NVD
        return False