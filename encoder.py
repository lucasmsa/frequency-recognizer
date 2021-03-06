import bitarray as ba
import pyaudio
import wave
import numpy as np
from pysine import sine
import itertools
import sys
import simpleaudio as sa
import time
import binascii
import pyaudio

class Encoder():
    def __init__(self, file=None, message='', choice=0):
        self.message = message 
        with open(file, 'rb') as f:
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
        fs = 7000
        fs_2 = 12000

        if self.choice == 0:
            note = np.array(list(self.encodeString(self.file)), dtype=int)
        else:
            note = np.array(list(self.encodeString(self.message)), dtype=int)

        for bit in note:

            if bit == 0:
                sine(frequency=fs, duration=0.285)

            elif bit == 1:
                sine(frequency=fs_2, duration=0.285)

            #time.sleep(0.5)

        return note

msgEncode = Encoder("commands.txt", 'po', 1)
print(msgEncode.bitsToAudio())
