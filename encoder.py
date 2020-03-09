import bitarray as ba
import pyaudio
import wave
import numpy as np
import simpleaudio as sa
import time
import binascii
import pyaudio

class Encoder():

    def __init__(self, message):
        self.message = message    

    def encodeString(self): 
        messageToBits = ba.bitarray()
        messageToBits.frombytes(self.message.encode("utf-8"))
        messageToBitsList = messageToBits.tolist()
        bitsMessage = ba.bitarray(messageToBitsList)
        
        listBits = [int(bit) for bit in bitsMessage]
        
        strBits = ''.join(map(str, listBits))
        
        originalMessage = bitsMessage.tostring()
        
        print( "\nmessage: " + str(self.message),
               "\nmessageToBits: " + str(messageToBits), 
               "\nbitsMessage: " + str(bitsMessage), 
               "\nstrBits: " + str(strBits),
               "\nstrBitsToSting: " + str(bitsMessage.tostring()))

        return strBits


    def bitsToAudio(self):
        frequency = 440
        fs = 8000
        fs_2 = 48000
        seconds = 7

        t = np.linspace(0, seconds, seconds * fs, False)

        note = np.array(list(self.encodeString()), dtype=int)

        for bit in note:

            audio = (2**15 - 1) / np.max(np.abs(bit + 1))
            audio = audio.astype(np.int16)

            if bit == 0:
                playObj = sa.play_buffer(audio, 1, 2, fs)

            elif bit == 1:
                playObj = sa.play_buffer(audio, 1, 2, fs_2)
                
            playObj.wait_done()
            time.sleep(1)


        return note
        

msgEncode = Encoder("tomar no cu")
print(msgEncode.bitsToAudio())