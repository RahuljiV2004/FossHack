import subprocess
import json
import logging
import time
import os

logger = logging.getLogger(__name__)

class OWASPZAPScanner:
    def __init__(self):
        self.zap_path = "/Applications/ZAP.app/Contents/Java/zap.sh"  # Path to zap.sh
        self.report_dir = "/tmp/zap_reports"
        self.api_key = "your_api_key"  # Replace with your ZAP API key
        self.zap_home = "/tmp/zap_home"  # Custom home directory for ZAP

    def scan(self, target_url):
        results = {
            'alerts': [],
            'error': None
        }

        try:
            # Create report and home directories
            os.makedirs(self.report_dir, exist_ok=True)
            os.makedirs(self.zap_home, exist_ok=True)

            # Start ZAP in daemon mode with a custom home directory
            zap_process = subprocess.Popen(
                [self.zap_path, "-daemon", "-config", f"api.key={self.api_key}", "-dir", self.zap_home],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )

            # Wait for ZAP to start
            time.sleep(10)

            # Run an active scan
            scan_command = [
                self.zap_path, "-cmd",
                "-quickurl", target_url,
                "-quickprogress",
                "-quickout", f"{self.report_dir}/zap_report.json",
                "-config", f"api.key={self.api_key}",
                "-dir", self.zap_home
            ]
            subprocess.run(scan_command, check=True)

            # Stop ZAP
            zap_process.terminate()

            # Parse the report
            with open(f"{self.report_dir}/zap_report.json", "r") as f:
                report_data = json.load(f)
                results['alerts'] = report_data.get('alerts', [])

        except subprocess.CalledProcessError as e:
            logger.error(f"OWASP ZAP scan error: {e}")
            results['error'] = str(e)
        except Exception as e:
            logger.error(f"Unexpected error during OWASP ZAP scan: {e}")
            results['error'] = str(e)

        return results