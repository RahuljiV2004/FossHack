import os
import time
import logging
import subprocess
from zapv2 import ZAPv2

logger = logging.getLogger(__name__)

class OWASPZAPScanner:
    def __init__(self, zap_path="/Applications/ZAP.app/Contents/MacOS/ZAP.sh", zap_proxy="http://127.0.0.1:8080"):
        self.zap_path = zap_path
        self.zap_proxy = zap_proxy
        self.zap = ZAPv2(proxies={'http': zap_proxy, 'https': zap_proxy})

    def scan(self, target_url):
        results = {
            'alerts': [],
            'spider': {},
            'active_scan': {},
            'error': None
        }

        try:
            # Start ZAP in daemon mode (if not already running)
            self._start_zap_daemon()

            # Run a quick scan using ZAP API
            logger.info(f"Starting ZAP scan on {target_url}")
            self.zap.urlopen(target_url)  # Open the target URL in ZAP
            scan_id = self.zap.spider.scan(target_url)  # Start the spider
            while int(self.zap.spider.status(scan_id)) < 100:
                logger.info(f"Spider progress: {self.zap.spider.status(scan_id)}%")
                time.sleep(5)

            results['spider'] = {
                'status': 'completed',
                'urls': self.zap.spider.results(scan_id)
            }

            # Start the active scan
            scan_id = self.zap.ascan.scan(target_url)
            while int(self.zap.ascan.status(scan_id)) < 100:
                logger.info(f"Active scan progress: {self.zap.ascan.status(scan_id)}%")
                time.sleep(5)

            results['active_scan'] = {
                'status': 'completed',
                'alerts': self.zap.ascan.alerts(scan_id)
            }

            # Retrieve the alerts
            results['alerts'] = self.zap.core.alerts()

        except Exception as e:
            logger.error(f"OWASP ZAP scan error: {e}")
            results['error'] = str(e)

        return results

    def _start_zap_daemon(self):
        """
        Start ZAP in daemon mode if it's not already running.
        """
        try:
            # Check if ZAP is already running
            check_zap = subprocess.run(["pgrep", "-f", "ZAP.sh"], stdout=subprocess.PIPE)
            if check_zap.returncode != 0:
                # Start ZAP in daemon mode
                zap_daemon_command = [
                    self.zap_path,
                    "-daemon",
                    "-host", "127.0.0.1",
                    "-port", "8080",
                    "-config", "api.disablekey=true"  # Disable API key requirement
                ]
                subprocess.Popen(zap_daemon_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                logger.info("Started ZAP in daemon mode.")
                time.sleep(10)  # Wait for ZAP to initialize
        except Exception as e:
            logger.error(f"Failed to start ZAP daemon: {e}")
            raise