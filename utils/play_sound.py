import pygame
from colour import Colour
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

# takes sound file with extension as an argument then plays the corresponding sound
def play_sound(sound_file):
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
