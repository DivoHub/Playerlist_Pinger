import pygame
from colour import Colour
import os
import wave
import threading
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

# takes sound file with extension as an argument then plays the corresponding sound
def old_play_sound(sound_file):
    try:
        pygame.mixer.init()
        sound = pygame.mixer.Sound(f"../sounds/{sound_file}")
        sound.play()
        pygame.time.wait(int(sound.get_length() * 1000))  # Wait for the sound to finish playing
    except FileNotFoundError:
        print(f"{Colour().error}{sound_file} file not found.{Colour().default}")
    except Exception:
        print(f"{Colour().error}Error with playing notification audio.{Colour().default}")
    finally:
        pygame.mixer.quit()

def play_sound(sound_file):
    try:
        sound_path = os.path.join("..", "sounds", sound_file)
        with wave.open(sound_path, 'rb') as wave_file:
            audio_data = wave_file.readframes(wave_file.getnframes())
            wave_params = wave_file.getparams()

        def play_audio():
            import pyaudio  # Using pyaudio from the standard library
            audio = pyaudio.PyAudio()
            stream = audio.open(
                format=audio.get_format_from_width(wave_params.sampwidth),
                channels=wave_params.nchannels,
                rate=wave_params.framerate,
                output=True
            )
            stream.write(audio_data)
            stream.stop_stream()
            stream.close()
            audio.terminate()

        thread = threading.Thread(target=play_audio)
        thread.start()

    except FileNotFoundError:
        print(f"{Colour().error}{sound_file} file not found.{Colour().default}")
    except Exception:
        print(f"{Colour().error}Error with playing notification audio.{Colour().default}")

