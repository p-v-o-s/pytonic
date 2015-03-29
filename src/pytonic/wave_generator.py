import wave
import random
import numpy
import struct
import datetime

DEFAULT_FILENAME    = 'out.wav'
DEFAULT_SAMPLE_RATE = 44100  #Hz
AMPLITUDE_MAX       = 2**15 - 1

def constrain(x, low, high):
    if x < low:
        return low
    elif x > high:
        return high
    else:
        return x


class WaveSoundGenerator(object):
    def __init__(self, 
                 filename = DEFAULT_FILENAME, 
                 volume = 50,
                 sample_rate = DEFAULT_SAMPLE_RATE
                ):
        self.volume      = volume
        self.sample_rate = sample_rate
        self.wave        = wave.open(filename, 'w')
        self.wave.setparams((2, 2, sample_rate, 0, 'NONE', 'not compressed'))

    def setVolume(self, volume):
        """set the volume of the sound system"""
        self.volume = constrain(volume,0,100)

    def play(self, freq, duration, shape='sine'):
        """play a note of freq (hertz) for duration (seconds)"""
        N = duration*self.sample_rate
        t = numpy.linspace(0,duration,N)
        R = None
        L = None
        if shape == 'sine':
            R = AMPLITUDE_MAX*(self.volume/100.0)*numpy.sin(2*numpy.pi*freq*t)
            L = R
        R = numpy.where(R < -AMPLITUDE_MAX, -AMPLITUDE_MAX, R)
        R = numpy.where(R >  AMPLITUDE_MAX,  AMPLITUDE_MAX, R)
        R = R.astype(numpy.int16)
        L = numpy.where(L < -AMPLITUDE_MAX, -AMPLITUDE_MAX, L)
        L = numpy.where(L >  AMPLITUDE_MAX,  AMPLITUDE_MAX, L)
        L = L.astype(numpy.int16)
        #interleave R & L channels then convert to string
        data = numpy.vstack((R,L)).reshape((-1,),order='F').tostring()
        #write out the data
        self.wave.writeframes(data)
        

    def soundStop(self):
        """stop the sound the hard way"""
        self.wave.close()

    def __del__(self):
        self.soundStop()

###############################################################################
# TEST CODE
###############################################################################
if __name__ == "__main__":
    SG = WaveSoundGenerator()
    # set the volume of the sound system (0 to 100%)
    SG.setVolume(50)
    # play a note of requency 440 hertz (A4) for a duration of 5 seconds
    SG.play(440, 5)
    # play a note of requency 261.6 hertz (C4) for a duration of 5 seconds
    SG.play(261.6, 5)
    # optional
    SG.soundStop()
    

