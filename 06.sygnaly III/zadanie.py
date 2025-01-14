import numpy as np
import wave
import scipy.signal as signalSC
import scipy.io.wavfile
import sys
import warnings

warnings.filterwarnings("ignore")

def read_file(filename):
    sampleRate, signal = scipy.io.wavfile.read(filename)
    sampleCount = len(signal)
    duration = float(sampleCount) / sampleRate

    return signal, sampleCount, duration

def getFrequency(signal, sampleCount, duration, mono):
    if mono == 0:
        signal = [s[0] for s in signal]

    signal = signal * np.kaiser(sampleCount, 100)

    fftSpectrum = np.log(abs(np.fft.rfft(signal)))
    spectrum = np.copy(fftSpectrum)

    for k in range(2, 6):
        decimetedSpectrum = signalSC.decimate(fftSpectrum, k)
        spectrum[:len(decimetedSpectrum)] += decimetedSpectrum

    start = int(50 * duration)
    position = np.argmax(spectrum[start:])
    mainFrequency = (start + position) / duration

    return mainFrequency

if __name__ == "__main__":
    try:
        signal, sampleCount, duration = read_file(sys.argv[1])

        mono = 1
        if signal.ndim > 1:
            mono = 0

        mainFrequency = getFrequency(signal, sampleCount, duration, mono)

        if mainFrequency < 165:
            print("M")
        else:
            print("K")
    except Exception:
        print("K")
