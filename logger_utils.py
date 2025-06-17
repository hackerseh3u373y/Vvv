"""
Logging utilities for the simplex signal tool
"""

import logging
import os
from datetime import datetime

def setup_logging(level='INFO'):
    """Setup logging configuration"""
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Generate log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"logs/simplex_sniffer_{timestamp}.log"
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized. Log file: {log_filename}")

def log_capture_session(args):
    """Log capture session parameters"""
    logger = logging.getLogger(__name__)
    
    logger.info("CAPTURE SESSION STARTED")
    logger.info("-" * 30)
    logger.info(f"Frequency: {args.freq} MHz")
    logger.info(f"Gain: {args.gain} dB")
    logger.info(f"Sample Rate: {args.sample_rate} Hz")
    logger.info(f"Duration: {args.duration} seconds")
    logger.info(f"Output File: {args.output}")
    logger.info(f"Output Format: {args.format}")
    logger.info(f"Filter Range: {args.filter_range} kHz")
    logger.info(f"Analysis Enabled: {args.analyze}")
    logger.info(f"Plotting Enabled: {args.plot}")
    logger.info(f"Device Index: {args.device_index}")
    logger.info("-" * 30)
