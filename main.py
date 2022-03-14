import threading
import PySimpleGUI as sg
from pygame import mixer
import random
import sys, os


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


mixer.init()

window_closed = False
correct_sound = mixer.Sound(resource_path("audio\\correct.wav"))
cyrillic_sounds = [mixer.Sound(resource_path("audio\\"+str(i+1)+".wav")) for i in range(33)]
cyrillic_chars = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
MAX_ROWS = 3
MAX_COL = 11
score = 0
buttons_disabled = True
char_that_user_must_find = random.choice(cyrillic_chars)


character_buttons = [[sg.Button(cyrillic_chars[j+i*11], size=(4, 2), key=cyrillic_chars[j+i*11], pad=(0,0)) for j in range(MAX_COL)] for i in range(MAX_ROWS)]


window = sg.Window('Cyrillic Trainer', [[sg.Input(visible=False), sg.Text(f"Score: {score}", size=(11, 1), key="SCORE")], *character_buttons])
DEFAULT_BUTTON_COLOR = character_buttons[0][0].ButtonColor


def reset_button_color(key):
    window[key].update(button_color=DEFAULT_BUTTON_COLOR)


def enable_window():
    global buttons_disabled
    buttons_disabled = False


def play_sound(character):
    if not window_closed:
        cyrillic_sounds[cyrillic_chars.find(character)].play()

# don't play the sound as soon as the user starts the program, wait a tiny bit
threading.Timer(1, play_sound, char_that_user_must_find).start()
# only allow them to pick a choice once the talking stops
threading.Timer(2, enable_window).start()

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        window_closed = True
        break
    #print(event)
    if event == "REPEAT":
        play_sound(char_that_user_must_find)
    elif event in cyrillic_chars and not buttons_disabled:
        buttons_disabled = True

        window[event].update(button_color=(None, 'red'))
        window[char_that_user_must_find].update(button_color=(None, 'green'))
        if char_that_user_must_find == event:
            correct_sound.play()
            score += 1
            wait_time = 1
        else:
            score = 0
            play_sound(event)
            wait_time = 2.5
        window["SCORE"].update(f"Score: {score}")

        threading.Timer(wait_time, reset_button_color, char_that_user_must_find).start()
        threading.Timer(wait_time, reset_button_color, event).start()
        # only allow them to pick a choice once the talking stops
        threading.Timer(wait_time+1, enable_window).start()
        char_that_user_must_find = random.choice(cyrillic_chars)
        threading.Timer(wait_time, play_sound, char_that_user_must_find).start()

window.close()