#play notification sound
def play_sound(sound_file):
        try:
            audio_object = WaveObject.from_wave_file(f"./sounds/{sound_file}")
            play = audio_object.play()
            play.wait_done()
            play.stop()
        except FileNotFoundError:
            print(f"{colour.error} {sound_file} file not found. {colour.default}")
        except Exception:
            print (f"{colour.error} Error with playing notification audio. {colour.default}")
        finally:
            return