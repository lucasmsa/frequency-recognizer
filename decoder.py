from imports import *

class Decoder:
    
    
    def decodeSound(self):
        
        chunk = 12000 # Record in chunks of 1024 samples
        sample_format = pyaudio.paInt16  # 16 bits per sample
        channel = 1
        fs = 44100  # Record at 44100 samples per second 
        seconds = 10
        swidth = 32
        filename = "output.wav"

        

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

        ax2.set_xlim(20, fs / 2)
        
        bitsDecoder = []

        while True:
            try:
                start = time.time()
                data = stream.read(chunk)
                dataToInt = struct.unpack(str(2 * chunk) + 'B', data)
                dataNP = np.array(dataToInt, dtype='b')[::2] + 128
        
                dataNP = savgol_filter(dataNP, 103, 2)
            
                line.set_ydata(dataNP)

                y_fft = fft(dataToInt)
                treatedSignalCalculus = np.abs(y_fft[0:chunk]) * 2 / (256 * chunk)
                line_fft.set_ydata(treatedSignalCalculus)

                    
                fig.canvas.draw()
                fig.canvas.flush_events()

                peaks, _ = signal.find_peaks(treatedSignalCalculus)
                prominences = signal.peak_prominences(treatedSignalCalculus, peaks)[0]
                frequencies = signal.peak_prominences(treatedSignalCalculus, peaks)[1]
                print(len(prominences), len(frequencies))

                end = time.time()
                print(f'Time: {end - start}')

                try:
                    
                    print(f'max index -> {list(prominences).index(max(prominences))}')

                    max_index = list(prominences).index(max(prominences[580:1000]))

                    print(f'Frequencies: {max_index}')
                    print(f'Max_prominences: {prominences[max_index]}')

                    if max_index >= 600 and max_index <= 670 and prominences[max_index] > 0.1:

                        frequency_range = frequencies[max_index]

                        print(f'BIT: 0 -> {frequency_range}')
                        bitsDecoder.append(0)

                    elif max_index >= 700 and max_index <= 770 and prominences[max_index] > 0.05:
                        
                        frequency_range = frequencies[max_index]

                        print(f'BIT: 1 -> {frequency_range}')
                        bitsDecoder.append(1)  
                                     

                    print(f'Bits Decoded : {bitsDecoder}')

                except ValueError:
                    print(f'Problema, provavelmente o chunk ¯\_(ツ)_/¯')
                

            except KeyboardInterrupt:
                fig.End()
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

            if pitch >= 1550:
                bitsDecoded.append(0)
            elif pitch > 200:
                bitsDecoded.append(1)

            print(pitch)
            print(f'Message\'s bits: {bitsDecoded}')


decodeMessage = Decoder()
decodeMessage.decodeSound()
