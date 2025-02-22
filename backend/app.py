from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from modules.dns_scan import DNSScanner
from modules.domain_scan import DomainScanner
from modules.nmap_scan import NmapScanner
from modules.traffic_scan import TrafficScanner
from modules.vuln_scan import VulnerabilityScanner
from modules.owasp_zap_scan import OWASPZAPScanner
from modules.headers_scan import HeadersScanner
from modules.sitadel_scan import SitadelScanner  # Add this line
import concurrent.futures
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder="../frontend")  # Set static folder to frontend
CORS(app)

# Serve the frontend index.html file
@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

# API endpoint for scanning
@app.route('/api/scan', methods=['POST'])
def scan():
    data = request.json
    domain = data.get('domain')
    
    if not domain:
        return jsonify({'error': 'Domain is required'}), 400
    
    try:
        # Initialize scanners
        scanners = {
            'dns': DNSScanner(),
            'domain': DomainScanner(),
            'nmap': NmapScanner(),
            'traffic': TrafficScanner(),
            'vuln': VulnerabilityScanner(),
            'owasp_zap': OWASPZAPScanner(),
            'headers': HeadersScanner(),
            'sitadel': SitadelScanner()  # Add this line
        }
        
        # Use ThreadPoolExecutor to run scans concurrently
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(scanners['dns'].scan, domain): 'dns',
                executor.submit(scanners['domain'].scan, domain): 'domain',
                executor.submit(scanners['nmap'].scan, domain): 'nmap',
                executor.submit(scanners['traffic'].scan, domain): 'traffic',
                executor.submit(scanners['owasp_zap'].scan, f"http://{domain}"): 'owasp_zap',
                executor.submit(scanners['headers'].scan, domain): 'headers',
                executor.submit(scanners['sitadel'].scan, domain): 'sitadel'  # Add this line
            }
            
            results = {}
            for future in concurrent.futures.as_completed(futures):
                scan_type = futures[future]
                results[scan_type] = future.result()
            
            # Run vulnerability scan with port scan results
            results['vuln'] = scanners['vuln'].scan(domain, results['nmap'])
        
        return jsonify(results)
    
    except Exception as e:
        logger.error(f"Error during scan: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)