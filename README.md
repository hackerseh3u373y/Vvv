# Simplex Signal Penetration Testing Tool

A Python-based application for detecting, monitoring, and analyzing simplex signals on Kali Linux. This tool is designed for legitimate security research, penetration testing, and forensic analysis of simplex communication systems.

## ⚠️ Legal Disclaimer

**This tool is intended for authorized security research, penetration testing, and forensic analysis purposes only.** Users must ensure they have proper authorization before monitoring any signals. Unauthorized interception of communications may be illegal in your jurisdiction.

## Features

- **Signal Detection**: Detect and monitor simplex signals (walkie-talkies, public radios, VHF/UHF)
- **RTL-SDR Support**: Full support for RTL-SDR hardware dongles
- **Recording Capabilities**: Record signals in WAV or RAW format
- **Signal Analysis**: Extract frequency, signal strength (RSSI), and spectrum analysis
- **Command-Line Interface**: Comprehensive CLI with configurable parameters
- **Data Logging**: Log captured data for offline analysis
- **Visualization**: Generate spectrum plots and waterfall displays

## Requirements

### Hardware
- RTL-SDR compatible USB dongle
- Appropriate antenna for target frequency range

### Software
- Kali Linux (or compatible Linux distribution)
- Python 3.7+
- RTL-SDR drivers and tools

## Installation

1. Clone or download the tool files
2. Run the setup script:
   \`\`\`bash
   chmod +x setup.sh
   ./setup.sh
   \`\`\`

3. Alternatively, install manually:
   \`\`\`bash
   sudo apt update
   sudo apt install rtl-sdr librtlsdr-dev python3-pip
   pip3 install -r requirements.txt
   \`\`\`

## Usage

### Basic Usage
\`\`\`bash
python3 simplex_sniffer.py --freq 446.056 --gain 40 --duration 30 --output signal.wav
\`\`\`

### Advanced Usage
\`\`\`bash
# Monitor emergency services frequency with analysis
python3 simplex_sniffer.py --freq 162.550 --gain 30 --duration 60 --analyze --plot

# Capture amateur radio with custom sample rate
python3 simplex_sniffer.py --freq 144.390 --sample-rate 2048000 --duration 120 --format raw

# Monitor with specific filter bandwidth
python3 simplex_sniffer.py --freq 446.056 --filter-range 25 --duration 45 --analyze
\`\`\`

### Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--freq` | Center frequency in MHz (required) | - |
| `--gain` | RF gain (0-49) | 40 |
| `--sample-rate` | Sample rate in Hz | 2048000 |
| `--duration` | Capture duration in seconds | 30 |
| `--output` | Output filename | Auto-generated |
| `--format` | Output format (wav/raw) | wav |
| `--filter-range` | Filter bandwidth in kHz | 50.0 |
| `--analyze` | Enable real-time analysis | False |
| `--plot` | Generate spectrum plots | False |
| `--device-index` | RTL-SDR device index | 0 |

## Output Files

- **Audio Files**: WAV or RAW format recordings
- **Log Files**: Detailed capture logs in `logs/` directory
- **Analysis Reports**: Text reports with signal analysis
- **Plots**: Spectrum and waterfall plots (PNG format)

## Common Frequency Ranges

| Service | Frequency Range | Example |
|---------|----------------|---------|
| Amateur Radio 2m | 144-148 MHz | 144.390 MHz |
| Amateur Radio 70cm | 420-450 MHz | 446.056 MHz |
| NOAA Weather | 162.400-162.550 MHz | 162.550 MHz |
| Marine VHF | 156-162 MHz | 156.800 MHz |
| Aviation | 118-137 MHz | 121.500 MHz |

## Troubleshooting

### RTL-SDR Not Detected
\`\`\`bash
# Check if device is recognized
lsusb | grep RTL
rtl_test -t
\`\`\`

### Permission Issues
\`\`\`bash
# Add user to plugdev group
sudo usermod -a -G plugdev $USER
# Logout and login again
\`\`\`

### Sample Rate Issues
- Try lower sample rates (1024000, 512000)
- Ensure your RTL-SDR supports the chosen sample rate

## Security Research Applications

This tool is designed for:
- **Penetration Testing**: Assess wireless communication security
- **Forensic Analysis**: Analyze captured communications
- **Security Research**: Study simplex communication protocols
- **Red Team Operations**: Authorized wireless reconnaissance
- **Educational Purposes**: Learn about RF signal analysis

## Contributing

This tool is designed for the security research community. Contributions should focus on:
- Enhanced signal analysis capabilities
- Additional modulation detection
- Improved visualization features
- Performance optimizations

## License

Educational/Research Use Only - Ensure compliance with local laws and regulations.

---

**Remember**: Always obtain proper authorization before monitoring any communications. This tool is for legitimate security research and forensic analysis only.
