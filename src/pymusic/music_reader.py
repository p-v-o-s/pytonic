import re
Note_token_regex  = re.compile("([+-]?[#b]?[ABCDEFG])(\d+[.]?)?") 
Instr_token_regex = re.compile("([dorst])(.*)")       

class MusicReader(object):
    def __init__(self, music_player):
        self.music_player = music_player
        self.note_tokens  = music_player.pitch_map.keys()
    def play_song(self, song):
        for token in song.split():
            #try parsing as a note token
            m = Note_token_regex.match(token)
            if m:
                pitch, dur = m.groups()
                octave = None
                if pitch.startswith('-'):   #play down a octave
                    octave = '-'
                    pitch = pitch[1:]
                elif pitch.startswith('+'): #play up an octave
                    octave = '+'
                    pitch = pitch[1:]
                if dur is None:
                    pass
                elif dur.endswith('.'):
                    dur = 2.0/3.0 * float(dur[:-1])
                else:
                    dur = float(dur)
                self.music_player.play_note(pitch, dur, octave = octave)       
            else:
                m = Instr_token_regex.match(token)
                if m:
                    instr = m.group(1)
                    if instr == 'd':
                        dur = m.group(2)
                        if dur.endswith('.'):
                            dur = 2.0/3.0 * int(dur[:-1])
                        else:
                            dur = float(dur)
                        #print "set duration:", dur
                        self.music_player.set_dur(dur) 
                    elif instr == 'o':  #octave switch
                        octave = m.group(2)
                        if octave == '+':
                            octave = self.music_player.octave + 1
                        elif octave == '-':
                            octave = self.music_player.octave - 1
                        octave = int(octave)
                        #print "set octave:", octave
                        self.music_player.set_octave(octave)
                    elif instr == 'r':   #rest
                        dur = m.group(2)
                        if dur is None:
                            pass
                        elif dur.endswith('.'):
                            dur = 2.0/3.0 * float(dur[:-1])
                        else:
                            dur = float(dur)
                        #print "rest"
                        self.music_player.rest(dur)
                    elif instr == 's':   #time signature
                        sig = m.group(2)
                        sig = sig.split(",")
                        #print "rest"
                        self.music_player.set_time_signature(ts_top    = float(sig[0]),
                                                             ts_bottom = float(sig[1]),
                                                            )
                    elif instr == 't':
                        qpm = float(m.group(2))
                        self.music_player.set_tempo(qpm)
                      

###############################################################################
# TEST CODE
###############################################################################
if __name__ == "__main__":
    import os, glob
    from music_player import MusicPlayer
    from tksound import SoundGenerator
    SG = SoundGenerator()
    # set the volume of the sound system (0 to 100%)
    SG.setVolume(60)
    MP = MusicPlayer(SG)
    MR = MusicReader(MP)
    
    pattern = os.sep.join(("songs","*.sng"))
    for fn in glob.glob(pattern):
        print "playing song file:", fn
        song = open(fn).read()
        MR.play_song(song)
   
