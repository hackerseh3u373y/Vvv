"""
Signal Analysis Module
Provides signal analysis, peak detection, and visualization capabilities
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy import signal as scipy_signal
from scipy.fft import fft, fftfreq
import logging
from datetime import datetime

class SignalAnalyzer:
    def __init__(self, sample_rate, filter_bandwidth=50000):
        self.logger = logging.getLogger(__name__)
        self.sample_rate = sample_rate
        self.filter_bandwidth = filter_bandwidth
        self.analysis_results = []
        
    def calculate_rssi(self, samples):
        """Calculate Received Signal Strength Indicator (RSSI)"""
        # Calculate power in dBm
        power_linear = np.mean(np.abs(samples)**2)
        power_dbm = 10 * np.log10(power_linear) - 30  # Approximate conversion
        return power_dbm
    
    def detect_signal_peaks(self, samples, threshold_db=-60, min_distance=1000):
        """Detect signal peaks in frequency domain"""
        # Compute FFT
        fft_data = fft(samples)
        freqs = fftfreq(len(samples), 1/self.sample_rate)
        
        # Convert to power spectrum in dB
        power_spectrum = 20 * np.log10(np.abs(fft_data) + 1e-12)
        
        # Find peaks
        peaks, properties = scipy_signal.find_peaks(
            power_spectrum[:len(power_spectrum)//2],  # Only positive frequencies
            height=threshold_db,
            distance=min_distance
        )
        
        # Extract peak information
        peak_info = []
        for peak in peaks:
            freq = freqs[peak]
            power = power_spectrum[peak]
            peak_info.append((freq, power))
        
        # Sort by power (strongest first)
        peak_info.sort(key=lambda x: x[1], reverse=True)
        
        return peak_info
    
    def apply_bandpass_filter(self, samples, low_freq, high_freq):
        """Apply bandpass filter to samples"""
        nyquist = self.sample_rate / 2
        low = low_freq / nyquist
        high = high_freq / nyquist
        
        b, a = scipy_signal.butter(4, [low, high], btype='band')
        filtered_samples = scipy_signal.filtfilt(b, a, samples)
        
        return filtered_samples
    
    def plot_spectrum(self, samples, center_freq, sample_rate, save_plot=True):
        """Plot frequency spectrum"""
        # Compute FFT
        fft_data = fft(samples)
        freqs = fftfreq(len(samples), 1/sample_rate)
        
        # Shift to center frequency
        freqs_shifted = freqs + center_freq
        
        # Convert to power spectrum in dB
        power_spectrum = 20 * np.log10(np.abs(fft_data) + 1e-12)
        
        # Plot
        plt.figure(figsize=(12, 6))
        plt.plot(freqs_shifted[:len(freqs_shifted)//2] / 1e6, 
                power_spectrum[:len(power_spectrum)//2])
        plt.xlabel('Frequency (MHz)')
        plt.ylabel('Power (dB)')
        plt.title(f'Signal Spectrum - Center: {center_freq/1e6:.3f} MHz')
        plt.grid(True, alpha=0.3)
        
        if save_plot:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"spectrum_{timestamp}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            self.logger.info(f"Spectrum plot saved: {filename}")
        
        plt.show()
    
    def plot_waterfall(self, samples, sample_rate, save_plot=True):
        """Generate waterfall plot for time-frequency analysis"""
        # Parameters for STFT
        nperseg = 1024
        noverlap = nperseg // 2
        
        # Compute spectrogram
        f, t, Sxx = scipy_signal.spectrogram(
            samples, 
            fs=sample_rate,
            nperseg=nperseg,
            noverlap=noverlap
        )
        
        # Convert to dB
        Sxx_db = 10 * np.log10(Sxx + 1e-12)
        
        # Plot waterfall
        plt.figure(figsize=(12, 8))
        plt.pcolormesh(t, f / 1e6, Sxx_db, shading='gouraud', cmap='viridis')
        plt.colorbar(label='Power (dB)')
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (MHz)')
        plt.title('Waterfall Plot - Time vs Frequency')
        
        if save_plot:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"waterfall_{timestamp}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            self.logger.info(f"Waterfall plot saved: {filename}")
        
        plt.show()
    
    def analyze_modulation(self, samples):
        """Basic modulation analysis"""
        # Calculate instantaneous amplitude and phase
        analytic_signal = scipy_signal.hilbert(samples)
        amplitude = np.abs(analytic_signal)
        phase = np.unwrap(np.angle(analytic_signal))
        
        # Calculate instantaneous frequency
        inst_freq = np.diff(phase) / (2.0 * np.pi) * self.sample_rate
        
        # Basic statistics
        amp_std = np.std(amplitude)
        freq_std = np.std(inst_freq)
        
        # Simple modulation detection heuristics
        if amp_std > 0.1:
            modulation_type = "Likely AM"
        elif freq_std > 1000:
            modulation_type = "Likely FM"
        else:
            modulation_type = "Unknown/CW"
        
        return {
            'modulation_type': modulation_type,
            'amplitude_std': amp_std,
            'frequency_std': freq_std,
            'mean_amplitude': np.mean(amplitude)
        }
    
    def generate_report(self, filename):
        """Generate analysis report"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(filename, 'w') as f:
            f.write("SIMPLEX SIGNAL ANALYSIS REPORT\n")
            f.write("=" * 50 + "\n")
            f.write(f"Generated: {timestamp}\n")
            f.write(f"Sample Rate: {self.sample_rate} Hz\n")
            f.write(f"Filter Bandwidth: {self.filter_bandwidth} Hz\n\n")
            
            if self.analysis_results:
                f.write("ANALYSIS RESULTS:\n")
                f.write("-" * 20 + "\n")
                for result in self.analysis_results:
                    f.write(f"{result}\n")
            else:
                f.write("No analysis results available.\n")
        
        self.logger.info(f"Analysis report saved: {filename}")
