import visa, time

class PPMSSoundGenerator(object):
    def __init__(self, addr):
        self.ppms = visa.instrument(addr, term_chars = "")
    def play(self, freq, duration):
        """play a note of freq (hertz) for duration (seconds)"""
        cmd = "BEEP %f, %f" % (duration, freq)
        ppms.write(cmd)
        time.sleep(duration)
        

###############################################################################
# TEST CODE
###############################################################################
if __name__ == "__main__":
    from pymusic import MusicPlayer, MusicReader
    SG = PPMSSoundGenerator("GPIB::15")
    MP = MusicPlayer(SG)
    MR = MusicReader(MP)
    
    pattern = os.sep.join(("songs","*.sng"))
    for fn in glob.glob(pattern):
        print "playing song file:", fn
        song = open(fn).read()
        MR.play_song(song)
   

    
