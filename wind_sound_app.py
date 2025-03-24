import sys
import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QHBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class WindSoundApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.stream = None
        self.file_path = None

    def init_ui(self):
        self.setWindowTitle("Wind Sound and Analysis")
        self.setGeometry(100, 100, 800, 400)
        
        self.select_button = QPushButton("Select WAV File", self)
        self.select_button.clicked.connect(self.select_file)
        
        self.start_button = QPushButton("Start Wind", self)
        self.start_button.clicked.connect(self.start_wind)
        
        self.stop_button = QPushButton("Stop Wind", self)
        self.stop_button.clicked.connect(self.stop_wind)
        
        self.analyze_button = QPushButton("Analyze Sound", self)
        self.analyze_button.clicked.connect(self.analyze_sound)
        
        self.layout = QHBoxLayout()
        self.left_layout = QVBoxLayout()
        
        self.left_layout.addWidget(self.select_button)
        self.left_layout.addWidget(self.start_button)
        self.left_layout.addWidget(self.stop_button)
        self.left_layout.addWidget(self.analyze_button)
        
        self.layout.addLayout(self.left_layout)
        
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)
        
        self.setLayout(self.layout)

    def select_file(self):
        file_dialog = QFileDialog()
        self.file_path, _ = file_dialog.getOpenFileName(self, "Select WAV File", "", "Audio Files (*.wav)")
    
    def generate_wind_sound(self, outdata, frames, time, status):
        if status:
            print(status)
        noise = np.random.normal(0, 0.1, frames)
        filtered_noise = np.convolve(noise, np.ones(100)/100, mode='same')
        outdata[:, 0] = filtered_noise
    
    def start_wind(self):
        if self.stream is None:
            self.stream = sd.OutputStream(channels=1, callback=self.generate_wind_sound, samplerate=44100)
            self.stream.start()
    
    def stop_wind(self):
        if self.stream is not None:
            self.stream.stop()
            self.stream.close()
            self.stream = None
    
    def analyze_sound(self):
        if self.file_path:
            sample_rate, data = wav.read(self.file_path)
            if len(data.shape) > 1:
                data = data[:, 0]  # Convert stereo to mono
            n = len(data)
            freq_spectrum = np.fft.fft(data)
            freq_magnitude = np.abs(freq_spectrum[:n // 2])
            freqs = np.fft.fftfreq(n, d=1/sample_rate)[:n // 2]
            
            self.ax.clear()
            self.ax.plot(freqs, freq_magnitude, color='blue')
            self.ax.set_xlabel('Frequency (Hz)')
            self.ax.set_ylabel('Magnitude')
            self.ax.set_title('Frequency Spectrum')
            self.ax.grid()
            self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WindSoundApp()
    window.show()
    sys.exit(app.exec())
