import dns.resolver
import logging

logger = logging.getLogger(__name__)

class DNSScanner:
    def scan(self, domain):
        results = {
            'a_records': [],
            'mx_records': [],
            'ns_records': [],
            'txt_records': [],
            'cname_records': [],
            'soa_records': [],
            'error': None
        }
        
        try:
            # A records
            a_records = dns.resolver.resolve(domain, 'A')
            results['a_records'] = [str(record) for record in a_records]
            
            # MX records
            mx_records = dns.resolver.resolve(domain, 'MX')
            results['mx_records'] = [str(record.exchange) for record in mx_records]
            
            # NS records
            ns_records = dns.resolver.resolve(domain, 'NS')
            results['ns_records'] = [str(record) for record in ns_records]
            
            # TXT records
            txt_records = dns.resolver.resolve(domain, 'TXT')
            results['txt_records'] = [str(record) for record in txt_records]
            
            # CNAME records
            try:
                cname_records = dns.resolver.resolve(domain, 'CNAME')
                results['cname_records'] = [str(record) for record in cname_records]
            except dns.resolver.NoAnswer:
                results['cname_records'] = []
            
            # SOA records
            try:
                soa_records = dns.resolver.resolve(domain, 'SOA')
                results['soa_records'] = [str(record) for record in soa_records]
            except dns.resolver.NoAnswer:
                results['soa_records'] = []
            
        except dns.resolver.NXDOMAIN:
            results['error'] = 'Domain does not exist'
        except dns.resolver.NoAnswer:
            results['error'] = 'No DNS records found for the domain'
        except dns.resolver.Timeout:
            results['error'] = 'DNS query timed out'
        except Exception as e:
            logger.error(f"DNS scan error for {domain}: {e}")
            results['error'] = str(e)
            
        return results