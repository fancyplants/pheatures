import sys
import json
import curses
import os

import tty, termios
def _unix_getch():
    """Get a single character from stdin, Unix version"""

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())          # Raw read
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

getch = _unix_getch

with open('text.json') as f:
    dataset = json.load(f)

# get any consonants that aren't already done/in the dataset
def get_consonants():
    with open('consonants.txt', 'r') as f:
        all_letters = f.read().split()

    done = dataset.keys()

    # filter only letters not in our current dataset
    letters = [l for l in all_letters if l not in done]
    
    return letters

def get_vowels():
    with open('vowels.txt') as f:
        all_vowels = f.read().split()

    done = dataset.keys()

    vowels = [v for v in all_vowels if v not in done]

    return vowels

def get_features():
    with open('features.txt') as f:
        features = f.read().split('\n')
    
    return features

features = get_features()

vowel_presets = {
    'syllabic': '+',
    'stress': '-',
    'long': '-',
    'consonantal': '-',
    'sonorant': '+',
    'continuant': '+',
    'delayed release': '0',
    'approximant': '+',
    'tap': '-',
    'trill': '-',
    'lateral': '-',
    'nasal': '-',
    'voice': '+',
    'spread glottis': '-',
    'constricted glottis': '-',
    'labiodental': '-',
    'CORONAL': '-',
    'anterior': '0',
    'distributed': '0',
    'strident': '0',
    'DORSAL': '+'
}

def get_preset(feature):
    return vowel_presets.get(feature, None)

def fill_features(phone):
    print()
    dataset[phone] = {}
    # for filling in "null" data
    skip = 0
    for feature in features:
        if skip > 0:
            skip -= 1
            dataset[phone][feature] = '0'
            continue

        while True:
            print(f'{feature} value for {phone}: ', end='')
            value = getch()
            if value == '\u0003':
                sys.exit(1)
            # value = input(f'{feature} value for {l}: ')

            # equal sign means plus, it's just so I don't have to hit shift
            if value == '=' or value == '-' or value == '0':
                if feature == 'CORONAL' and value == '-':
                    skip = 3
                if feature == 'DORSAL' and value == '-':
                    skip = 5

                # set to actual
                if value == '=':
                    value = '+'

                # another line break
                print(value)
                break
            print('Nope, not valid.')

        dataset[phone][feature] = value

    # save progress at every step
    with open('text.json', 'w+') as f:
        json.dump(dataset, f, indent=4, ensure_ascii=False)

for phone in get_consonants():
    fill_features(phone)
