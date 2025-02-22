from scapy.all import *
import time
import logging

logger = logging.getLogger(__name__)

class TrafficScanner:
    def scan(self, domain):
        results = []
        try:
            # Capture packets for 30 seconds
            start_time = time.time()
            packets = sniff(filter=f"host {domain}", timeout=30)
            
            # Analyze traffic in 5-second intervals
            interval = 5
            current_time = start_time
            
            while current_time < start_time + 30:
                packet_count = len([p for p in packets if p.time >= current_time and 
                                  p.time < current_time + interval])
                
                results.append({
                    'timestamp': time.strftime('%H:%M:%S', time.localtime(current_time)),
                    'packets': packet_count
                })
                
                current_time += interval
                
        except Exception as e:
            logger.error(f"Traffic scan error for {domain}: {e}")
            results.append({'error': str(e)})
            
        return results