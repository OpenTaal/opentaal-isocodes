#!/usr/bin/env python3
'''Extract Dutch toponymes from iso-codes.'''

from glob import glob
import sys

#from nltk import edit_distance

def get_category(directory):
    '''Get category.'''
    if directory in ('iso_3166-1', 'iso_3166-2', 'iso_3166-3'):
        return 'land'
    if 'iso_4217' == directory:
        return 'valuta'
    if 'iso_15924' == directory:
        return 'schrift'
    if 'iso_639-5' == directory:
        return 'taalfamilie'
    if directory in ('iso_639-2', 'iso_639-3'):
        return 'taal'
    print(f'ERROR: Unknown ISO code {directory}')
    sys.exit(1)
    return ''

def is_useless(msgstr):
    '''Test if msgstr is useful.'''
    if msgstr == '':
        return True
    strings = ('Gereserveerd voor privégebruik',
               'Geen linguïstische inhoud; niet van toepassing',
               '	Aandelenmarkteenheid Europese ',
               'De codes toegekend voor transacties waar')
    for string in strings:
        if string in msgstr:
            return True
    # chars = ('²',
    #          'ə')
    # for char in chars:
    #     if char in msgstr:
    #         return True
    return False

def fix(line):
    '''Fix line.'''
    for match in (' (na', ' (tot', ' (ca. ', ' (1', ' (2', ' (3', ' (4', ' (5', ' (6', ' (7', ' (8', ' (9'):
        pos = line.find(match)
        if pos != -1:
            line = line[:pos]
    for match in (' (familie)', ' (district)', ' (stad)', ' (volgende dag)', ' (overige)', ' (trustgebied)', ', op het Engels gebaseerd', ', op het Frans gebaseerd', ', op het Portugees gebaseerd'):
         if line.endswith(match):
            line = line[:-len(match)]
    #Zuid, etc
    # if line.endswith(', Oud'):
    #     line = f'Oud {line[:-5]}'
    # if line.endswith(', Middel'):
    #     line = f'Middle {line[:-8]}'
    #TODO make a for loop
    if line.endswith(', Republiek'):
        line = f'Republiek {line[:-11]}'
    if line.endswith(', Socialistische Republiek van de Unie van'):
        line = f'Socialistische Republiek van de Unie van {line[:-42]}'
    if line.endswith(', Democratische Volksrepubliek'):
        line = f'Democratische Volksrepubliek {line[:-30]}'
    if line.endswith(', Democratische Republiek'):
        line = f'Democratische Republiek {line[:-25]}'
    if line.endswith(', Socialistische Federale Republiek'):
        line = f'Socialistische Federale Republiek {line[:-35]}'
    if line.endswith(', Provincie'):
        line = f'Provincie {line[:-11]}'
    if line.endswith(', Oblast'):
        line = f'Oblast {line[:-8]}'
    if line[0] == ' ' or line[-1] == ' ':
        print(f'ERROR: Space at begin or end {line}')
        sys.exit(1)
    if line[-1] == ',':
        print(f'ERROR: Comma at end {line}')
        sys.exit(1)
    return line

words = {}
for filepath in glob('../iso-codes/*/nl.po'):
    iso_code = filepath[13:-6]
    category = get_category(iso_code)
    print(f'{filepath} {category}')
    with open(filepath) as file:
        msgstrs = {}
        msgid = None
        msgstr = None
        for line in file:
            line = line[:-1]
            # print(line)
            if line.startswith('msgid "'):
                msgid = line[7:-1]
            elif line.startswith('msgstr "'):
                msgstr = line[8:-1]
                if is_useless(msgstr):
                    continue
                #TODO split on semicolon
                msgstr = fix(msgstr)
                if msgstr in msgstrs:
                    msgstrs[msgstr] += 1
                else:
                    msgstrs[msgstr] = 1
                print(f'  {msgstr}')
                if iso_code != 'iso_4217':
                    if msgstr != 'gebarentalen' and msgstr[0] not in (
                            'A', 'Å', 'Á', 'Ā', 'B',
                            'C', 'Č', 'Ç', 'D',
                            'E', 'É', 'Ē', 'F', 'G',
                            'H', 'Ħ',
                            'I', 'Î', 'J',
                            'K', 'Ķ',
                            'L', 'Ł', 'M',
                            'N', 'Ñ',
                            'O', 'Ö', 'P', 'Q', 'R',
                            'S', 'Ş', 'Š', 'Ș', 'Ś', 'T',
                            'U', 'Ú', 'V', 'W', 'X', 'Y',
                            'Z', 'Ž', 'Ż'):
                        print('WARNING: First character should be upper case.')
                if msgstr not in words:
                    words[msgstr] = []
                if category not in words[msgstr]:
                    words[msgstr].append(category)

        for l, count in sorted(msgstrs.items()):
            if count > 1:
                print(f'{count} {l}')
# print(words)
