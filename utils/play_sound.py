from simpleaudio import WaveObject
from .colour import Colour

#play notification sound
def play_sound(sound_file):
        try:
            audio_object = WaveObject.from_wave_file(f"../sounds/{sound_file}")
            play = audio_object.play()
            play.wait_done()
            play.stop()
        except FileNotFoundError:
            print(f"{Colour().error} {sound_file} file not found. {Colour().default}")
        except Exception:
            print (f"{Colour().error} Error with playing notification audio. {Colour().default}")
        finally:
            return