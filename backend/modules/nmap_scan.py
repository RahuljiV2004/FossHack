import nmap
import logging

logger = logging.getLogger(__name__)

class NmapScanner:
    def scan(self, domain):
        nm = nmap.PortScanner()
        results = {
            'open_ports': [],
            'services': {},
            'os_detection': None,
            'error': None
        }
        
        try:
            # Basic port scan (no root privileges required)
            nm.scan(domain, arguments='-sT --top-ports 1000')
            
            for host in nm.all_hosts():
                for proto in nm[host].all_protocols():
                    ports = nm[host][proto].keys()
                    for port in ports:
                        port_info = nm[host][proto][port]
                        if port_info['state'] == 'open':
                            results['open_ports'].append(port)
                            results['services'][port] = {
                                'name': port_info['name'],
                                'product': port_info['product'],
                                'version': port_info['version']
                            }
                
                if 'osmatch' in nm[host]:
                    results['os_detection'] = nm[host]['osmatch']
                    
        except Exception as e:
            logger.error(f"Nmap scan error for {domain}: {e}")
            results['error'] = str(e)
            
        return results