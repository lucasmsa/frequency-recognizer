import pyaudio
import wave
import aubio
import numpy as np
import parabolic
import struct
from scipy import signal
from scipy.fftpack import fft
import matplotlib.pyplot as plt
import time



class Decoder:

    def decodeSound(self):
        
        chunk = 1024  # Record in chunks of 1024 samples
        sample_format = pyaudio.paInt16  # 16 bits per sample
        channel = 1
        fs = 44100  # Record at 44100 samples per second
        seconds = 10
        swidth = 32
        filename = "output.wav"

        window = np.blackman(chunk)

        p = pyaudio.PyAudio()  # Create an interface to PortAudio

        plt.ion()
            
        fig, (ax, ax2) = plt.subplots(2, figsize=(15, 8))

        print('Recording')

        stream = p.open(format=sample_format,
                        channels=channel,
                        rate=fs,
                        input=True,
                        output=True,
                        frames_per_buffer=chunk,
                        )
        
        x = np.arange( 0, 2 * chunk, 2)
        x_fft = np.linspace(0, fs, chunk)

        line, = ax.plot(x, np.random.rand(chunk), '-', lw=2)
        line_fft, = ax2.semilogx(x_fft, np.random.rand(chunk), '-', lw=2) 

        
        ax.set_title('Audio received from microphone')
        ax.set_xlabel('samples')
        ax.set_ylabel('volume')
        ax.set_ylim(0, 256)
        ax.set_xlim(0, 2 * chunk)
        #plt.setp(ax, xticks=[0, chunk, 2*chunk], yticks=[0, 128, 256])

        ax2.set_xlim(20, fs / 2)

        while True:
            try:
                data = stream.read(chunk)
                
                dataToInt = struct.unpack(str(2 * chunk) + 'B', data)
                dataNP = np.array(dataToInt, dtype='b')[::2] + 128

                line.set_ydata(dataNP)
                
                y_fft = fft(dataToInt)
                line_fft.set_ydata(np.abs(y_fft[0:chunk]) * 2 / (256 * chunk))

                fig.canvas.draw()
                fig.canvas.flush_events()
                #time.sleep(0.05)

            except(Exception):

                print('End recording session')            

     

    def pitchDetection(self):
        # PyAudio object.
        p = pyaudio.PyAudio()
        bitsDecoded = []

        # Open stream.
        stream = p.open(format=pyaudio.paFloat32,
            channels=1, rate=44100, input=True,
            frames_per_buffer=1024)

        # Aubio's pitch detection.
        pDetection = aubio.pitch("default", 2048, 1024, 44100)
        # Set unit.
        pDetection.set_unit("Hz")
        pDetection.set_silence(-40)

        while True:

            data = stream.read(1024)
            samples = np.fromstring(data, dtype=aubio.float_type)
            pitch = pDetection(samples)[0]
            """ 
            # Compute Fourier transform of windowed signal
            # windowed = data * blackmanharris(len(data))
            windowed = np.array(len(data)) * blackmanharris(len(data))
            f = np.fft.rfft(windowed)
            print(f)

            # Find the peak and interpolate to get a more accurate peak
            i = np.argmax(abs(f))  # Just use this for less-accurate, naive version
            true_i = parabolic.Trapezoidal(np.log(abs(f)), i)[0]

            # Convert to equivalent frequency
            print(f'frequency: {44100 * true_i / len(windowed)}') """

            # Compute the energy (volume) of the
            # current frame.
            volume = np.sum(samples**2)/len(samples)
            # Format the volume output so that at most
            # it has six decimal numbers.
            volume = "{:.6f}".format(volume)

            if pitch >= 1550:
                bitsDecoded.append(0)
            elif pitch > 200:
                bitsDecoded.append(1)


            print(pitch)
            #print(volume)
            print(f'Message\'s bits: {bitsDecoded}')


decodeMessage = Decoder()
decodeMessage.decodeSound()
