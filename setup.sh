#!/bin/bash

# Setup script for Simplex Signal Penetration Testing Tool
# For Kali Linux

echo "Setting up Simplex Signal Penetration Testing Tool..."
echo "=================================================="

# Update package list
echo "Updating package list..."
sudo apt update

# Install RTL-SDR drivers and tools
echo "Installing RTL-SDR drivers and tools..."
sudo apt install -y rtl-sdr librtlsdr-dev librtlsdr0

# Install Python dependencies
echo "Installing Python dependencies..."
sudo apt install -y python3-pip python3-dev

# Install required Python packages
echo "Installing Python packages..."
pip3 install -r requirements.txt

# Create necessary directories
echo "Creating directories..."
mkdir -p logs
mkdir -p captures
mkdir -p plots

# Set permissions
chmod +x simplex_sniffer.py

# Test RTL-SDR installation
echo "Testing RTL-SDR installation..."
rtl_test -t

echo "Setup complete!"
echo ""
echo "Usage examples:"
echo "  python3 simplex_sniffer.py --freq 446.056 --gain 40 --duration 30 --output signal.wav"
echo "  python3 simplex_sniffer.py --freq 162.550 --sample-rate 2048000 --duration 60 --format raw"
echo "  python3 simplex_sniffer.py --freq 144.390 --gain 30 --filter-range 10 --analyze --plot"
echo ""
echo "IMPORTANT: This tool is for authorized security research and forensic analysis only."
echo "Ensure you have proper authorization before monitoring any signals."
