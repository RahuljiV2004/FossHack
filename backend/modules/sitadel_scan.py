import os
import subprocess
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class SitadelScanner:
    def __init__(self):
        # Dynamically locate Sitadel
        self.sitadel_path = self._find_sitadel()
        self.report_dir = str(Path(__file__).resolve().parent.parent / "tmp" / "sitadel_reports")
        os.makedirs(self.report_dir, exist_ok=True)  # Ensure the directory exists
        self.scan_cache = {}  # Cache to store scan results

    def _find_sitadel(self):
        """
        Dynamically locate the Sitadel script.
        """
        # Check if the user has specified the Sitadel path via an environment variable
        sitadel_path_env = os.getenv("SITADEL_PATH")
        if sitadel_path_env and os.path.exists(sitadel_path_env):
            return sitadel_path_env

        # Check common installation paths
        common_paths = [
            "/usr/bin/sitadel.py",  # Linux
            "/usr/local/bin/sitadel.py",  # Linux
            str(Path.home() / "Sitadel" / "sitadel.py"),  # User directory
            "/Users/rejenthompson/Desktop/projects_cyber/Sitadel/sitadel.py",  # Your machine
            str(Path(__file__).resolve().parent.parent / "Sitadel" / "sitadel.py"),  # Project directory
        ]

        for path in common_paths:
            if os.path.exists(path):
                return path

        # If not found, prompt the user to install Sitadel
        raise FileNotFoundError(
            "Sitadel not found. Please install Sitadel and ensure it is in your PATH or set the SITADEL_PATH environment variable."
        )

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

            # Run Sitadel with default scan configuration
            scan_command = [
                "python3", self.sitadel_path, target_url,
                "-f", "server,cms,waf,framework,frontend,header,lang,system",
                "-a", "injection,bruteforce,vulns,other",
                "-r", "1",  # Default risk level (LOW)
                "--no-redirect",
                "-v"
            ]

            process = subprocess.Popen(
                scan_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
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