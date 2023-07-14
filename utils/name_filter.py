from threading import Thread
from .colour import Colour

def name_filter(playerlist):
    words_file = open('../banned_words.txt', 'r')
    banned_words = words_file.read().split()
    player_strings = " ".join(playerlist)
    for each_word in banned_words:
        if (each_word in player_strings):
            print (f"{Colour().error}Banned word: [{each_word}]  found in online player list.{Colour().default}")

def add_banned_words():
    words_file = open('../banned_words.txt', 'w+')
    banned_words = words_file.read().split()
    while True:
        new_word = input(f"{Colour().default} Enter word to add to banned list (enter 'x' when finished):    ")
        if (new_word == "x"):
            break
        elif (new_word in banned_words):
            print(f"{Colour().warning} word is already on list. {Colour().default}")
        else:
            banned_words.append(new_word)
            words_file.write(banned_words)
            words_file.close()
