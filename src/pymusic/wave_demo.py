import os, glob
###############################################################################
# TEST CODE
###############################################################################
if __name__ == "__main__":
    from pymusic import MusicPlayer, MusicReader
    from wave_generator import WaveSoundGenerator
    pattern = os.sep.join(("songs","*.sng"))
    for fn in glob.glob(pattern):
        name, ext = os.path.splitext(fn)
        wave_filename = "%s.wav" % name
        SG = WaveSoundGenerator(wave_filename)
        MP = MusicPlayer(SG)
        MR = MusicReader(MP)
        print "playing song file:", fn
        song = open(fn).read()
        MR.play_song(song)
        SG.soundStop()
   
