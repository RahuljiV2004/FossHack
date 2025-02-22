import subprocess
import json
import logging
import os

logger = logging.getLogger(__name__)

class WhatWebScanner:
    def __init__(self, whatweb_path="whatweb"):
        self.whatweb_path = whatweb_path

    def scan(self, domain):
        results = {
            'technologies': [],
            'error': None
        }

        try:
            # Run WhatWeb using ruby
            whatweb_command = ["ruby", self.whatweb_path, domain]
            process = subprocess.Popen(whatweb_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            if process.returncode != 0:
                raise Exception(stderr.decode())

            # Parse WhatWeb output
            output = stdout.decode()
            results['technologies'] = self._parse_whatweb_output(output)

        except Exception as e:
            logger.error(f"WhatWeb scan error: {e}")
            results['error'] = str(e)

        return results

    def _parse_whatweb_output(self, output):
        technologies = []
        for line in output.splitlines():
            if "[" in line and "]" in line:
                tech = line.split("[")[1].split("]")[0]
                technologies.append(tech)
        return technologies


class WafWoofScanner:
    def __init__(self, wafwoof_path="wafw00f"):
        self.wafwoof_path = wafwoof_path

    def scan(self, domain):
        results = {
            'waf': None,
            'error': None
        }

        try:
            # Run WafW00F directly
            wafwoof_command = [self.wafwoof_path, domain]
            process = subprocess.Popen(wafwoof_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            if process.returncode != 0:
                raise Exception(stderr.decode())

            # Parse WafW00F output
            output = stdout.decode()
            results['waf'] = self._parse_wafwoof_output(output)

        except Exception as e:
            logger.error(f"WafW00F scan error: {e}")
            results['error'] = str(e)

        return results

    def _parse_wafwoof_output(self, output):
        if "No WAF detected" in output:
            return "No WAF detected"
        else:
            return output.split("WAF:")[1].strip()


class BuiltWithScanner:
    def __init__(self, whatweb_path="whatweb", wafwoof_path="wafw00f"):
        self.whatweb_scanner = WhatWebScanner(whatweb_path)
        self.wafwoof_scanner = WafWoofScanner(wafwoof_path)

    def scan(self, domain):
        results = {
            'technologies': [],
            'waf': None,
            'error': None
        }

        try:
            # Run WhatWeb to detect technologies
            whatweb_results = self.whatweb_scanner.scan(domain)
            if whatweb_results['error']:
                raise Exception(whatweb_results['error'])
            results['technologies'] = whatweb_results['technologies']

            # Run WafW00F to detect WAF
            wafwoof_results = self.wafwoof_scanner.scan(domain)
            if wafwoof_results['error']:
                raise Exception(wafwoof_results['error'])
            results['waf'] = wafwoof_results['waf']

        except Exception as e:
            logger.error(f"BuiltWith scan error: {e}")
            results['error'] = str(e)

        return results