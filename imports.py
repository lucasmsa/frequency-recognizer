import pyaudio
import wave
import aubio
import numpy as np
import argparse
import queue
import sys
import struct
from scipy import signal
from scipy.fftpack import fft
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sounddevice as sd
import time
from scipy.signal import lfilter, savgol_filter
import time
import multiprocessing
