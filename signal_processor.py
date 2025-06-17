"""
Signal Processing Module for Simplex Signal Detection
Handles RTL-SDR interface and signal capture
"""

import numpy as np
import logging
from rtlsdr import RtlSdr
import wave
import struct
import time
from scipy import signal as scipy_signal

class SimplexSignalProcessor:
    def __init__(self, device_index=0, sample_rate=2048000, center_freq=446.056e6, gain=40):
        self.logger = logging.getLogger(__name__)
        self.device_index = device_index
        self.sample_rate = sample_rate
        self.center_freq = center_freq
        self.gain = gain
        self.sdr = None
        self.is_capturing = False
        
        self._initialize_sdr()
    
    def _initialize_sdr(self):
        """Initialize RTL-SDR device"""
        try:
            self.sdr = RtlSdr(device_index=self.device_index)
            self.sdr.sample_rate = self.sample_rate
            self.sdr.center_freq = self.center_freq
            self.sdr.gain = self.gain
            
            self.logger.info(f"RTL-SDR initialized:")
            self.logger.info(f"  Sample Rate: {self.sample_rate} Hz")
            self.logger.info(f"  Center Frequency: {self.center_freq/1e6:.3f} MHz")
            self.logger.info(f"  Gain: {self.gain} dB")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize RTL-SDR: {e}")
            raise
    
    def capture_signal(self, duration, output_file, output_format='wav', 
                      analyzer=None, enable_analysis=False, enable_plotting=False):
        """Capture signal for specified duration"""
        self.is_capturing = True
        num_samples = int(duration * self.sample_rate)
        
        self.logger.info(f"Capturing {num_samples} samples...")
        
        try:
            # Capture samples
            samples = self.sdr.read_samples(num_samples)
            
            # Perform real-time analysis if requested
            if enable_analysis and analyzer:
                self._perform_realtime_analysis(samples, analyzer, enable_plotting)
            
            # Save to file
            self._save_samples(samples, output_file, output_format)
            
            return samples
            
        except Exception as e:
            self.logger.error(f"Error during capture: {e}")
            raise
        finally:
            self.is_capturing = False
    
    def _perform_realtime_analysis(self, samples, analyzer, enable_plotting):
        """Perform real-time signal analysis"""
        self.logger.info("Performing signal analysis...")
        
        # Calculate signal strength (RSSI)
        rssi = analyzer.calculate_rssi(samples)
        self.logger.info(f"Signal Strength (RSSI): {rssi:.2f} dBm")
        
        # Detect peaks in frequency domain
        peaks = analyzer.detect_signal_peaks(samples)
        if peaks:
            self.logger.info(f"Detected {len(peaks)} signal peaks")
            for i, (freq, power) in enumerate(peaks[:5]):  # Show top 5
                freq_mhz = (self.center_freq + freq) / 1e6
                self.logger.info(f"  Peak {i+1}: {freq_mhz:.3f} MHz, {power:.2f} dB")
        
        # Generate plots if requested
        if enable_plotting:
            analyzer.plot_spectrum(samples, self.center_freq, self.sample_rate)
            analyzer.plot_waterfall(samples, self.sample_rate)
    
    def _save_samples(self, samples, output_file, output_format):
        """Save samples to file in specified format"""
        if output_format == 'wav':
            self._save_as_wav(samples, output_file)
        elif output_format == 'raw':
            self._save_as_raw(samples, output_file)
        else:
            raise ValueError(f"Unsupported output format: {output_format}")
    
    def _save_as_wav(self, samples, filename):
        """Save complex samples as WAV file (I/Q interleaved)"""
        # Convert complex samples to interleaved I/Q
        interleaved = np.empty(len(samples) * 2, dtype=np.float32)
        interleaved[0::2] = samples.real
        interleaved[1::2] = samples.imag
        
        # Normalize to 16-bit range
        normalized = np.int16(interleaved * 32767)
        
        with wave.open(filename, 'wb') as wav_file:
            wav_file.setnchannels(2)  # I and Q channels
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(self.sample_rate)
            wav_file.writeframes(normalized.tobytes())
        
        self.logger.info(f"Saved {len(samples)} samples as WAV: {filename}")
    
    def _save_as_raw(self, samples, filename):
        """Save complex samples as raw binary file"""
        # Convert to complex64 format
        samples_complex64 = samples.astype(np.complex64)
        
        with open(filename, 'wb') as f:
            f.write(samples_complex64.tobytes())
        
        self.logger.info(f"Saved {len(samples)} samples as RAW: {filename}")
    
    def set_frequency(self, freq_hz):
        """Change center frequency"""
        if self.sdr:
            self.sdr.center_freq = freq_hz
            self.center_freq = freq_hz
            self.logger.info(f"Frequency changed to {freq_hz/1e6:.3f} MHz")
    
    def set_gain(self, gain_db):
        """Change RF gain"""
        if self.sdr:
            self.sdr.gain = gain_db
            self.gain = gain_db
            self.logger.info(f"Gain changed to {gain_db} dB")
    
    def cleanup(self):
        """Clean up RTL-SDR resources"""
        if self.sdr:
            self.sdr.close()
            self.logger.info("RTL-SDR device closed")
