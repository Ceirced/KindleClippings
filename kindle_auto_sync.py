#!/usr/bin/env python3

import os
import sys
import time
import subprocess
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(Path(__file__).parent / 'kindle_auto_sync.log')
    ]
)

KINDLE_VOLUME = "/Volumes/Kindle"
CHECK_INTERVAL = 5
SYNC_SCRIPT = Path(__file__).parent / "sync_kindle_clippings.sh"

def is_kindle_connected():
    return os.path.exists(KINDLE_VOLUME) and os.path.isdir(KINDLE_VOLUME)

def run_sync_script():
    try:
        logging.info("Running sync script...")
        result = subprocess.run(
            [str(SYNC_SCRIPT)],
            capture_output=True,
            text=True,
            check=True
        )
        logging.info("Sync and parsing output:")
        for line in result.stdout.splitlines():
            logging.info(f"  {line}")
        
        if "Successfully parsed clippings" in result.stdout:
            logging.info("Clippings parsed into individual book files successfully")
        elif "Warning: Failed to parse clippings" in result.stdout:
            logging.warning("Sync succeeded but parsing failed - check KindleClippings.py")
        
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Sync failed: {e}")
        if e.stderr:
            logging.error(f"Error output: {e.stderr}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error running sync: {e}")
        return False

def main():
    logging.info("Starting Kindle auto-sync monitor...")
    logging.info(f"Monitoring for Kindle at: {KINDLE_VOLUME}")
    logging.info(f"Check interval: {CHECK_INTERVAL} seconds")
    
    kindle_was_connected = False
    last_sync_time = None
    
    try:
        while True:
            kindle_connected = is_kindle_connected()
            
            if kindle_connected and not kindle_was_connected:
                logging.info("Kindle connected! Waiting 2 seconds for mount to stabilize...")
                time.sleep(2)
                
                if is_kindle_connected():
                    current_time = datetime.now()
                    if last_sync_time is None or (current_time - last_sync_time).seconds > 60:
                        if run_sync_script():
                            last_sync_time = current_time
                            logging.info("Sync completed successfully")
                        else:
                            logging.warning("Sync failed - will retry on next connection")
                    else:
                        logging.info("Skipping sync - last sync was less than 60 seconds ago")
                else:
                    logging.warning("Kindle disconnected during stabilization period")
            
            elif not kindle_connected and kindle_was_connected:
                logging.info("Kindle disconnected")
            
            kindle_was_connected = kindle_connected
            time.sleep(CHECK_INTERVAL)
            
    except KeyboardInterrupt:
        logging.info("\nStopping Kindle auto-sync monitor...")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()