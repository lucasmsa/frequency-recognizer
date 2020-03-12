import bitarray as ba
import pyaudio
import wave
import numpy as np
import simpleaudio as sa
import time
import binascii
import pyaudio

class Encoder():
    def __init__(self, file=None, message='', choice=0):
        self.message = message 
        with open(file, 'r') as f:
            self.file = f.read()   
        self.choice = choice

    def encodeString(self, toEnconde): 
        messageToBits = ba.bitarray()
        messageToBits.frombytes(toEnconde.encode("utf-8"))
        messageToBitsList = messageToBits.tolist()
        bitsMessage = ba.bitarray(messageToBitsList)
        
        listBits = [int(bit) for bit in bitsMessage]
        
        strBits = ''.join(map(str, listBits))
        
        originalMessage = bitsMessage.tostring()
        
        print( "\nmessage: " + str(toEnconde),
               "\nmessageToBits: " + str(messageToBits), 
               "\nbitsMessage: " + str(bitsMessage), 
               "\nstrBits: " + str(strBits),
               "\nstrBitsToString: " + str(bitsMessage.tostring()))

        return strBits


    def bitsToAudio(self):
        fs = 8000
        fs_2 = 11025

        if self.choice==0:
            note = np.array(list(self.encodeString(self.file)), dtype=int)
        else:
            note = np.array(list(self.encodeString(self.message)), dtype=int)

        for bit in note:

            audio = (2**31 - 1) / np.max(np.abs(bit + 1))
            audio = audio.astype(np.int32)

            if bit == 0:
                playObj = sa.play_buffer(audio, 1, 2, fs)

            elif bit == 1:
                playObj = sa.play_buffer(audio, 1, 2, fs_2)
                
            playObj.wait_done()
            time.sleep(0.5)
        
        return note

msgEncode = Encoder("commands.txt", 'po', 1)
print(msgEncode.bitsToAudio())
