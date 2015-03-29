import time

def scale_equal_tempered(octave=4):
    a = 2.0**(1.0/12.0)
    return lambda n, octave=octave: 440.0*(a)**(n + 12*(octave-4))

PITCH_MAP = {}
PITCH_MAP['A']  = 0
PITCH_MAP['#A'] = 1
PITCH_MAP['bB'] = 1
PITCH_MAP['B']  = 2
PITCH_MAP['C']  = 3
PITCH_MAP['#C'] = 4
PITCH_MAP['bD'] = 4
PITCH_MAP['D']  = 5
PITCH_MAP['#D'] = 6
PITCH_MAP['bE'] = 6
PITCH_MAP['E']  = 7
PITCH_MAP['F']  = 8
PITCH_MAP['#F'] = 9
PITCH_MAP['bG'] = 9
PITCH_MAP['G']  = 10
PITCH_MAP['#G'] = 11
PITCH_MAP['bA'] = 11

class MusicPlayer(object):
    def __init__(self, sound_generator, scale = None, pitch_map = None, octave = 4, ts_top = 4.0, ts_bottom = 4.0, tempo_qpm = 120):
        self.sound_generator = sound_generator
        if scale is None:
            scale = scale_equal_tempered(octave=octave)
        self.scale = scale
        if pitch_map is None:
            pitch_map = PITCH_MAP
        self.pitch_map = pitch_map
        self.octave = octave
        self.current_dur    = 4.0 #quarter note
        self.set_time_signature(ts_top,ts_bottom)
        self.set_tempo(tempo_qpm)

    def set_time_signature(self, ts_top, ts_bottom):
        self.ts_top    = ts_top
        self.ts_bottom = ts_bottom

    def set_tempo(self, qpm): #qpm = quaternotes per minute
        self.measure_length = 60.0 * (self.ts_top / self.ts_bottom) / (qpm/4.0)     

    def set_scale(self, scale):
        self.scale = scale

    def set_octave(self, octave):
        self.octave = octave

    def set_dur(self, dur):
        self.current_dur = dur

    def play_note(self, pitch, dur = None, octave = None):
        num  = self.pitch_map.get(pitch)
        if octave is None:
            octave = self.octave
        elif octave == '-':
            octave = self.octave - 1
        elif octave == '+':
            octave = self.octave + 1
        freq = self.scale(num, octave = octave)
        if dur is None:
            dur = self.current_dur
        length  = self.measure_length/dur
        self.sound_generator.play(freq, length)

    def rest(self, dur = None):
        if dur is None:
            dur = self.current_dur
        length  = self.measure_length/dur
        time.sleep(length) 


###############################################################################
# TEST CODE
###############################################################################
if __name__ == "__main__":
    import os, glob
    from tksound import SoundGenerator
    SG = SoundGenerator()
    # set the volume of the sound system (0 to 100%)
    SG.setVolume(60)
    MP = MusicPlayer(SG)
