import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from modules.dns_scan import DNSScanner
from modules.domain_scan import DomainScanner
from modules.nmap_scan import NmapScanner
from modules.traffic_scan import TrafficScanner
from modules.vuln_scan import VulnerabilityScanner
from modules.owasp_zap_scan import OWASPZAPScanner
from modules.headers_scan import HeadersScanner
from modules.broken_link_checker import BrokenLinkChecker
from modules.html_vulnerability_scanner import HTMLVulnerabilityScanner
from modules.builtwith_scanner import BuiltWithScanner
from modules.sensitive_file_checker import SensitiveFileChecker
from modules.subdomain_scanner import SubdomainScanner
import concurrent.futures
import logging
import shutil

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder="../frontend")
CORS(app)

def check_tool_installed(tool_name):
    """
    Check if a tool is installed and accessible in the system's PATH.
    """
    return shutil.which(tool_name) is not None

@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/scan', methods=['POST'])
def scan():
    data = request.json
    domain = data.get('domain')
    
    if not domain:
        return jsonify({'error': 'Domain is required'}), 400
    
    try:
        # Check if required tools are installed
        required_tools = {
            'ruby': 'Ruby (required for WhatWeb)',
            'wafw00f': 'WafW00F',
            'zap.sh': 'OWASP ZAP'
        }

        missing_tools = []
        for tool, name in required_tools.items():
            if not check_tool_installed(tool):
                missing_tools.append(name)

        if missing_tools:
            return jsonify({
                'error': f"The following tools are missing: {', '.join(missing_tools)}. Please install them and ensure they are in your PATH."
            }), 400

        # Initialize scanners
        scanners = {
            'dns': DNSScanner(),
            'domain': DomainScanner(),
            'nmap': NmapScanner(),
            'traffic': TrafficScanner(),
            'vuln': VulnerabilityScanner(),
            'owasp_zap': OWASPZAPScanner(zap_path="/Applications/ZAP.app/Contents/MacOS/ZAP.sh"),  # Update with the correct path
            'headers': HeadersScanner(),
            'broken_links': BrokenLinkChecker(),
            'html_vuln': HTMLVulnerabilityScanner(),
            'builtwith': BuiltWithScanner(whatweb_path="/path/to/whatweb"),  # Update with the correct path
            'sensitive_files': SensitiveFileChecker(),
            'subdomains': SubdomainScanner()
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
                executor.submit(scanners['broken_links'].check_links, f"http://{domain}"): 'broken_links',
                executor.submit(scanners['html_vuln'].scan, f"http://{domain}"): 'html_vuln',
                executor.submit(scanners['builtwith'].scan, domain): 'builtwith',
                executor.submit(scanners['sensitive_files'].search_sensitive_files, domain): 'sensitive_files',
                executor.submit(scanners['subdomains'].scan, domain): 'subdomains'
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