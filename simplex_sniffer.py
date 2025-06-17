#!/usr/bin/env python3
"""
Simplex Signal Penetration Testing Tool
For legitimate security research and forensic analysis only.

Author: Security Research Team
License: Educational/Research Use Only
"""

import argparse
import sys
import os
import logging
import signal
from datetime import datetime
from signal_processor import SimplexSignalProcessor
from analyzer import SignalAnalyzer
from logger_utils import setup_logging, log_capture_session

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\n[INFO] Stopping signal capture...")
    sys.exit(0)

def validate_frequency(freq):
    """Validate frequency is within reasonable VHF/UHF range"""
    if not (30 <= freq <= 3000):  # 30MHz to 3GHz
        raise argparse.ArgumentTypeError(f"Frequency {freq} MHz is outside valid range (30-3000 MHz)")
    return freq

def main():
    parser = argparse.ArgumentParser(
        description="Simplex Signal Penetration Testing Tool - For authorized security research only",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python simplex_sniffer.py --freq 446.056 --gain 40 --duration 30 --output signal.wav
  python simplex_sniffer.py --freq 162.550 --sample-rate 2048000 --duration 60 --format raw
  python simplex_sniffer.py --freq 144.390 --gain 30 --filter-range 10 --analyze
        """
    )
    
    # Required arguments
    parser.add_argument('--freq', type=validate_frequency, required=True,
                       help='Center frequency in MHz (30-3000)')
    
    # Optional arguments
    parser.add_argument('--gain', type=int, default=40,
                       help='RF gain (0-49, default: 40)')
    parser.add_argument('--sample-rate', type=int, default=2048000,
                       help='Sample rate in Hz (default: 2048000)')
    parser.add_argument('--duration', type=int, default=30,
                       help='Capture duration in seconds (default: 30)')
    parser.add_argument('--output', type=str, default=None,
                       help='Output filename (auto-generated if not specified)')
    parser.add_argument('--format', choices=['wav', 'raw'], default='wav',
                       help='Output format (default: wav)')
    parser.add_argument('--filter-range', type=float, default=50.0,
                       help='Filter bandwidth in kHz (default: 50.0)')
    parser.add_argument('--analyze', action='store_true',
                       help='Perform real-time signal analysis')
    parser.add_argument('--plot', action='store_true',
                       help='Generate spectrum plots')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       default='INFO', help='Logging level (default: INFO)')
    parser.add_argument('--device-index', type=int, default=0,
                       help='RTL-SDR device index (default: 0)')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)
    
    # Legal disclaimer
    print("=" * 70)
    print("SIMPLEX SIGNAL PENETRATION TESTING TOOL")
    print("FOR AUTHORIZED SECURITY RESEARCH AND FORENSIC ANALYSIS ONLY")
    print("=" * 70)
    print("WARNING: This tool is intended for legitimate security research,")
    print("penetration testing, and forensic analysis purposes only.")
    print("Ensure you have proper authorization before monitoring any signals.")
    print("=" * 70)
    
    # Generate output filename if not provided
    if not args.output:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        freq_str = str(args.freq).replace('.', '_')
        args.output = f"simplex_capture_{freq_str}MHz_{timestamp}.{args.format}"
    
    # Setup signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        # Initialize signal processor
        logger.info(f"Initializing RTL-SDR device {args.device_index}")
        processor = SimplexSignalProcessor(
            device_index=args.device_index,
            sample_rate=args.sample_rate,
            center_freq=args.freq * 1e6,  # Convert MHz to Hz
            gain=args.gain
        )
        
        # Initialize analyzer if requested
        analyzer = None
        if args.analyze or args.plot:
            analyzer = SignalAnalyzer(args.sample_rate, args.filter_range * 1000)
        
        # Log capture session details
        log_capture_session(args)
        
        # Start capture
        logger.info(f"Starting signal capture on {args.freq} MHz for {args.duration} seconds")
        logger.info(f"Output: {args.output} ({args.format} format)")
        
        samples = processor.capture_signal(
            duration=args.duration,
            output_file=args.output,
            output_format=args.format,
            analyzer=analyzer,
            enable_analysis=args.analyze,
            enable_plotting=args.plot
        )
        
        logger.info(f"Capture completed. {len(samples)} samples recorded.")
        logger.info(f"Output saved to: {args.output}")
        
        # Generate final analysis report
        if analyzer:
            analyzer.generate_report(args.output.replace(f'.{args.format}', '_report.txt'))
        
    except KeyboardInterrupt:
        logger.info("Capture interrupted by user")
    except Exception as e:
        logger.error(f"Error during capture: {e}")
        sys.exit(1)
    finally:
        if 'processor' in locals():
            processor.cleanup()

if __name__ == "__main__":
    main()
