import pyaudio
import wave
import aubio
import numpy as np
import parabolic
import struct
from scipy import signal
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

        print('Recording')

        stream = p.open(format=sample_format,
                        channels=channel,
                        rate=fs,
                        input=True,
                        output=True,
                        frames_per_buffer=chunk,
                        )
        
        figure, axis = plt.subplots()
        
        x = np.arrange( 0, 2 * chunk, 2)
        line, = axis.plot(x, np.random.rand(chunk))
        
        while True:
            data = stream.read(chunk)

            dataToInt = np.array(struct.unpack(str(2 * chunk) + 'B', data), dtype='b')[::2] + 127
            line.set_ydata(dataToInt)
            figure.canvas.draw()
            figure.canvas.flush_events()

        """ frames = []  # Initialize array to store frames
        data = stream.read(chunk)
        # Store data in chunks for 10 seconds
        for i in range(0, int(fs / chunk * seconds)):
            print(len(data))


            #stream.write(data)

            indata = np.array(len(data)/swidth)*window

            # Take the fft and square each value
            fftData=abs(np.fft.rfft(indata))**2
            # find the maximum
            which = fftData[1:].argmax() + 1
            # use quadratic interpolation around the max
            if which != len(fftData)-1:
                y0,y1,y2 = np.log(fftData[which-1:which+2:])
                x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
                # find the frequency and output it
                thefreq = (which+x1)*fs/chunk
                print(f"The freq is {thefreq} Hz.")
            else:
                thefreq = which*fs/chunk
                print(f"The freq is {thefreq} Hz.")
            # read some more data
            data = stream.read(chunk)
            frames.append(data)
            

        # Stop and close the stream 
        stream.write(data)
        stream.stop_stream()
        stream.close()
        # Terminate the PortAudio interface
        p.terminate()

        print('Finished recording')

        # Save the recorded data as a WAV file
        wf = wave.open('audio/audio-decoded.wav', 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close() """

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
