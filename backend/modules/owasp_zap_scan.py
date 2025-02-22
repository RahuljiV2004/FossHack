import subprocess
import json
import logging
import time
import os
from pathlib import Path

logger = logging.getLogger(__name__)

class OWASPZAPScanner:
    def __init__(self):
        # Use a dynamic path for ZAP
        self.zap_path = str(Path(__file__).resolve().parent.parent / "ZAP" / "zap.sh")
        self.report_dir = str(Path(__file__).resolve().parent.parent / "tmp" / "zap_reports")
        self.api_key = "your_api_key"  # Replace with your ZAP API key

    def scan(self, target_url):
        results = {
            'alerts': [],
            'error': None
        }

        try:
            # Create report directory
            os.makedirs(self.report_dir, exist_ok=True)

            # Start ZAP in daemon mode
            zap_process = subprocess.Popen(
                [self.zap_path, "-daemon", "-config", f"api.key={self.api_key}"],
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
                "-config", f"api.key={self.api_key}"
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