#!/usr/bin/env python3
'''Report Dutch translation in iso-codes for review and word list inclusion.'''

from datetime import datetime
from glob import glob
from os import getcwd, path
from pathlib import Path
import sys

from polib import pofile

#from nltk import edit_distance

__location__ = path.realpath(path.join(getcwd(), path.dirname(__file__)))


def description(iso, base):
    '''Describe an ISO standard.'''
    descriptions = {'iso_15924': ('Vierletterige codes schriftsystemen',
                                  f'{base}ISO_15924'),
                    'iso_3166-1': ('Drieletterige codes landnamen',
                                   f'{base}ISO_3166-1'),
                    'iso_3166-2': ('Codes onderverdelingen van landen',
                                   f'{base}ISO_3166-2'),
                    'iso_3166-3': ('Vierletterige codes voormalige landen',
                                   f'{base}ISO_3166-3'),
                    'iso_4217': ('Drieletterige codes valuta\'s',
                                 f'{base}ISO_4217'),
                    'iso_639-2': ('Drieletterige codes talen',
                                  f'{base}ISO_639#ISO_639-2'),
                    'iso_639-3': ('Drieletterige codes alle talen',
                                  f'{base}ISO_639#ISO_639-3'),
                    'iso_639-5': ('Drieletterige codes taalfamilies',
                                  f'{base}ISO_639-5'),
                    }
    return descriptions[iso]

def header(html, mado, title):
    '''Write HTML and mado header.'''
    html.write(f'''<html>
<head>
<title>{title}</title>
</head>
<body>
<h1>{title}</h1>
''')
    mado.write(f'''# {title}

''')

def footer(html, mado):
    '''Write HTML footer.'''
    html.write('''</body>
</html''')
    mado.write('\n')

def htmlcomment(comment, base):
    if ', ' in comment:
        results = []
        for part in comment.split(', '):
            pos = part.rfind(' ')
            results.append(f'<a target="_blank" href="{base}{part[pos+1:]}">{part}</a>')
        return ', '.join(results)
    else:
        pos = comment.rfind(' ')
        return f'<a target="_blank" href="{base}{comment[pos+1:]}">{comment}</a>'

def madocomment(comment, base):
    if ', ' in comment:
        results = []
        for part in comment.split(', '):
            pos = part.rfind(' ')
            results.append(f'[`{part}`]({base}{part[pos+1:]})')
        return '`, `'.join(results)
    else:
        pos = comment.rfind(' ')
        return f'[`{comment}`]({base}{comment[pos+1:]})'

def htmlpart(parts, base):
    if '; ' in parts:
        if ' / ' in parts:
            print(f'ERROR: Too complex {parts}')
            sys.exit(1)
        else:
            parts = parts.split('; ')
            ndx = 0
            while ndx < len(parts):
                parts[ndx] = f'<a target="_blank" href="{base}{parts[ndx]}">{parts[ndx]}</a>'
                ndx += 1
            return '; '.join(parts)
    else:
        if ' / ' in parts:
            parts = parts.split(' / ')
            ndx = 0
            while ndx < len(parts):
                parts[ndx] = f'<a target="_blank" href="{base}{parts[ndx]}">{parts[ndx]}</a>'
                ndx += 1
            return ' / '.join(parts)
        else:
            return f'<a target="_blank" href="{base}{parts}">{parts}</a>'

def madopart(parts, base):
    if '; ' in parts:
        if ' / ' in parts:
            print(f'ERROR: Too complex {parts}')
            sys.exit(1)
        else:
            parts = parts.split('; ')
            ndx = 0
            while ndx < len(parts):
                parts[ndx] = f'[`{parts[ndx]}`]({base}{parts[ndx].replace(" ", "_")})'
                ndx += 1
            return '`; `'.join(parts)
    else:
        if ' / ' in parts:
            parts = parts.split(' / ')
            ndx = 0
            while ndx < len(parts):
                parts[ndx] = f'[`{parts[ndx]}`]({base}{parts[ndx].replace(" ", "_")})'
                ndx += 1
            return '` / `'.join(parts)
        else:
            return f'[`{parts}`]({base}{parts.replace(" ", "_")})'

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
    strings = ('',
               'Gereserveerd voor privégebruik (begin)',
               'Gereserveerd voor privégebruik (einde)',
               'Geen linguïstische inhoud; niet van toepassing',
               '	Aandelenmarkteenheid Europese ',
               '	Aandelenmarkteenheid Europese ',
               '	Aandelenmarkteenheid Europese ',

               '	Zichtbare spraak',               
               '	Code voor overgeërfd schrift',
               'Wiskundige notatie',
               '	Symbolen (emojivariant)',
               'Symbolen	',
               '	Code voor ongeschreven documenten',
               '	Code voor onbepaald schrift',
               '	Code voor niet-gecodeerd schrift',
               
               'De codes toegekend voor transacties waar')
    for string in strings:
        if string == msgstr:
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


def main():
    '''Run main functionality.'''
    utcnow = datetime.utcnow()
    dtstamp = utcnow.strftime('%Y-%m-%d %H:%M:%S UTC')
    directory = Path(path.join(path.join(__location__, '..'), 'iso-codes'))
    base_en = 'https://en.wikipedia.org/w/index.php?search='
    base_nl = 'https://nl.wikipedia.org/w/index.php?search='
    isos = {}
    for sourcepath in Path(directory.resolve()).glob('*/nl.po'):
        iso = sourcepath.parts[-2]
        name = iso.replace('iso_', 'ISO ')
        isos[iso] = name
        with open(path.join(path.join(__location__, '..'), f'html/{iso}.html'), 'w') as html, \
        open(path.join(path.join(__location__, '..'), f'md/{iso}.md'), 'w')as mado, \
        open(path.join(path.join(__location__, '..'), f'tsv/{iso}.tsv'), 'w')as tsv:
            sourcefile = pofile(sourcepath)
            header(html, mado, name)
            desc = description(iso, base_nl)
            html.write('<p>Voor gebruik, lees de <a href="https://github.com/opentaal/opentaal-isocodes">documentatie</a> goed door. Deze bestanden zijn alleen voor reviewdoeleinden!</p>\n')
            html.write(f'<p><a target="_blank" href="{desc[1]}">{desc[0]}</a>. Totaal {len(sourcefile)} ISO-codes, {sourcefile.percent_translated()}% is vertaald op {dtstamp}.</p>\n')
            mado.write('Voor gebruik, lees de [documentatie](https://github.com/opentaal/opentaal-isocodes) goed door. Deze bestanden zijn alleen voor reviewdoeleinden!\n')
            mado.write('\n')
            mado.write(f'[{desc[0]}]({desc[1]}). Totaal {len(sourcefile)} ISO-codes, {sourcefile.percent_translated()}% is vertaald op {dtstamp}.\n')
            tsv.write('Codebeschijving\tEngels\tNederlands\n')
            if len(sourcefile.translated_entries()):
                html.write(f'<h2>Vertaald ({len(sourcefile.translated_entries())})</h2>')
                html.write('<table>\n')
                html.write('<tr><th>Codebeschijving</th><th>Engels</th><th>Nederlands</th></tr>\n')
                mado.write('\n')
                mado.write('Codebeschrijving | Engels | Nederlands\n')
                mado.write('---|---|---\n')
                for entry in sourcefile.translated_entries():
                    partsid = htmlpart(entry.msgid, base_en)
                    partsstr = htmlpart(entry.msgstr, base_nl)
                    html.write(f'<tr><td style="font-family: monospace;">{htmlcomment(entry.comment, base_en)}</td><td style="font-family: monospace;">{partsid}</td><td style="font-family: monospace;">{partsstr}</td></tr>\n')
                    partsid = madopart(entry.msgid, base_en)
                    partsstr = madopart(entry.msgstr, base_nl)
                    mado.write(f'{madocomment(entry.comment, base_en)} | {partsid} | {partsstr}\n')
                    tsv.write(f'{entry.comment}\t{entry.msgid}\t{entry.msgstr}\n')
                html.write('</table>\n')
            if len(sourcefile.untranslated_entries()):
                html.write(f'<h2>Onvertaald ({len(sourcefile.untranslated_entries())})</h2>\n')
                html.write('<table>\n')
                html.write('<tr><th>Codebeschijving</th><th>Engels</th></tr>\n')
                mado.write('\n')
                mado.write('Codebeschrijving | Engels\n')
                mado.write('---|---\n')
                for entry in sourcefile.untranslated_entries():
                    partsid = htmlpart(entry.msgid, base_en)
                    html.write(f'<tr><td style="font-family: monospace;">{htmlcomment(entry.comment, base_en)}</td><td style="font-family: monospace;">{partsid}</td></tr>\n')
                    partsid = madopart(entry.msgid, base_en)
                    mado.write(f'{madocomment(entry.comment, base_en)} | {partsid}\n')
                    tsv.write(f'{entry.comment}\t{entry.msgid}\t\n')
                html.write('</table>\n')
            footer(html, mado)

    # words = {}
    # for filepath in glob('../iso-codes/*/nl.po'):
    #     iso_code = filepath[13:-6]
    #     category = get_category(iso_code)
    #     print(f'{filepath} {category}')
    #     with open(filepath) as file:
    #         msgstrs = {}
    #         msgid = None
    #         msgstr = None
    #         for line in file:
    #             line = line[:-1]
    #             if line.startswith('msgid "'):
    #                 msgid = line[7:-1]
    #             elif line.startswith('msgstr "'):
    #                 msgstr = line[8:-1]
    #                 if is_useless(msgstr):
    #                     continue
    #                 msgstr = fix(msgstr) #TODO split semicolon
    #                 if msgstr in msgstrs:
    #                     msgstrs[msgstr] += 1
    #                 else:
    #                     msgstrs[msgstr] = 1
    #                 print(f'  {msgstr}')
    #                 if iso_code != 'iso_4217':
    #                     if msgstr != 'gebarentalen' and msgstr[0] not in (
    #                             'A', 'Å', 'Á', 'Ā', 'B',
    #                             'C', 'Č', 'Ç', 'D',
    #                             'E', 'É', 'Ē', 'F', 'G',
    #                             'H', 'Ħ',
    #                             'I', 'Î', 'J',
    #                             'K', 'Ķ',
    #                             'L', 'Ł', 'M',
    #                             'N', 'Ñ',
    #                             'O', 'Ö', 'P', 'Q', 'R',
    #                             'S', 'Ş', 'Š', 'Ș', 'Ś', 'T',
    #                             'U', 'Ú', 'V', 'W', 'X', 'Y',
    #                             'Z', 'Ž', 'Ż'):
    #                         print('WARNING: First character should be upper case.')
    #                 if msgstr not in words:
    #                     words[msgstr] = []
    #                 if category not in words[msgstr]:
    #                     words[msgstr].append(category)
    #         for l, count in sorted(msgstrs.items()):
    #             if count > 1:
    #                 print(f'{count} {l}')

if __name__ == "__main__":
    main()
