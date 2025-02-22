import subprocess
import json
import logging
import os
import threading
from pathlib import Path

logger = logging.getLogger(__name__)

class SitadelScanner:
    def __init__(self):
        # Use a dynamic path for Sitadel
        self.sitadel_path = str(Path(__file__).resolve().parent.parent / "Sitadel" / "sitadel.py")
        self.report_dir = str(Path(__file__).resolve().parent.parent / "tmp" / "sitadel_reports")
        self.scan_cache = {}  # Cache to store scan results

    def scan(self, target_url):
        if target_url in self.scan_cache:
            return self.scan_cache[target_url]

        results = {
            'fingerprints': {},
            'attacks': {},
            'error': None
        }

        try:
            # Create report directory
            os.makedirs(self.report_dir, exist_ok=True)

            # Run Sitadel with a deep scan configuration
            scan_command = (
                f"python3 {self.sitadel_path} {target_url} "
                "-f server,cms,waf,framework,frontend,header,lang,system "  # All fingerprint modules
                "-a injection,bruteforce,vulns,other "  # All attack modules
                "-r 2 "  # Risk level: DANGEROUS (deep scan)
                "--no-redirect "  # Do not follow redirects
                "-v"  # Verbose output
            )

            # Run the scan in a separate thread
            def run_scan():
                try:
                    process = subprocess.Popen(
                        scan_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
                    )
                    stdout, stderr = process.communicate()

                    if process.returncode != 0:
                        raise Exception(stderr.decode())

                    # Parse the output
                    output = stdout.decode()
                    results['fingerprints'], results['attacks'] = self._parse_output(output)

                    # Cache the results
                    self.scan_cache[target_url] = results
                except Exception as e:
                    logger.error(f"Sitadel scan error: {e}")
                    results['error'] = str(e)

            # Start the scan in a new thread
            scan_thread = threading.Thread(target=run_scan)
            scan_thread.start()
            scan_thread.join(timeout=300)  # Wait for 300 seconds (5 minutes) max

            if scan_thread.is_alive():
                # If the scan is still running after 5 minutes, terminate it
                logger.warning("Sitadel scan timed out")
                results['error'] = "Scan timed out"

        except Exception as e:
            logger.error(f"Unexpected error during Sitadel scan: {e}")
            results['error'] = str(e)

        return results

    def _parse_output(self, output):
        fingerprints = {}
        attacks = {}

        # Example parsing logic (customize based on Sitadel's output format)
        for line in output.splitlines():
            if "Fingerprint:" in line:
                key, value = line.split(":", 1)
                fingerprints[key.strip()] = value.strip()
            elif "Attack:" in line:
                key, value = line.split(":", 1)
                attacks[key.strip()] = value.strip()

        return fingerprints, attacks