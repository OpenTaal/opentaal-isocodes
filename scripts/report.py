#!/usr/bin/env python3
'''Report Dutch translation in iso-codes for review and word list inclusion.'''

from datetime import datetime
# from glob import glob
from operator import itemgetter
from json import load
from os import getcwd, path
from pathlib import Path
import sys

from hunspell import HunSpell
from polib import pofile
from termcolor import cprint

#from nltk import edit_distance

__location__ = path.realpath(path.join(getcwd(), path.dirname(__file__)))
hun_obj = HunSpell('/usr/share/hunspell/nl.dic', '/usr/share/hunspell/nl.aff')


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

def header(html, mado, spel, title):
    '''Write HTML and mado header.'''
    html.write(f'''<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
* {{font-family: monospace, monospace;}}
textarea {{line-height: 150%;}}
</style>
</head>
<body>
<h1>{title}</h1>
''')
    mado.write(f'''# {title}

''')
    spel.write(f'''# {title}

''')

def footer(html, mado):
    '''Write HTML and Markdown footer.'''
    html.write('''<br>
<small>Voor het onderhouden van deze vertalingen en de ondersteuning hiervan in de Nederlandse spellingcontrole, doneer via <a target="_blank" href="https://liberapay.com/opentaal">Liberapay</a> aan Stichting OpenTaal.</small>
</body>
</html''')
    mado.write('''
<small>Voor het onderhouden van deze vertalingen en de ondersteuning hiervan in de Nederlandse spellingcontrole, doneer via <a target="_blank" href="https://liberapay.com/opentaal">Liberapay</a> aan Stichting OpenTaal.</small>
''')

def htmlcomment(comment, base):
    '''Write HTML comment, i.e. code with description.'''
    comment = comment.replace('Inverted name', 'Inv.')
    comment = comment.replace('Official name', 'Off.')
    comment = comment.replace('Common name', 'Com.')
    pos = comment.find(', ')
    return f'<a target="_blank" href="{base}{comment[:pos]}">{comment[:pos]}</a>&nbsp;{comment[pos+2:-4]}'

def madocomment(comment, base):
    '''Write Markdown comment, i.e. code with description.'''
    pos = comment.find(', ')
    return f'[`{comment[:pos]}`]({base}{comment[:pos]})`{comment[pos+1:-4]}`'

def htmlpart(parts, base):
    '''Note that monospace is added outside of this method.'''
    if parts == 'NOG NIET VERTAALD':
        return parts
    if '; ' in parts:
        if ' / ' in parts:
            print(f'ERROR: Too complex {parts}')
            sys.exit(1)
        else:
            parts = parts.split('; ')
            ndx = 0
            prev = ''
            while ndx < len(parts):
                if prev == parts[ndx]: # not really needed up to now
                    cprint(f'WARNING: Identical parts {prev}', 'yellow')
                parts[ndx] = f'<a target="_blank" href="{base}{parts[ndx].replace(",", "")}">{parts[ndx]}</a>'
                prev = parts[ndx]
                ndx += 1
            return '; '.join(parts)
    if ' / ' in parts:
        parts = parts.split(' / ')
        ndx = 0
        while ndx < len(parts):
            parts[ndx] = f'<a target="_blank" href="{base}{parts[ndx].replace(",", "")}">{parts[ndx]}</a>'
            ndx += 1
        return ' / '.join(parts)
    return f'<a target="_blank" href="{base}{parts.replace(",", "")}">{parts}</a>'

def madopart(parts, base):
    '''Note that monospace via ` is added inside this method as it needs to be
    inside of the link.'''
    if parts == 'NOG NIET VERTAALD':
        return f'`{parts}`'
    if '; ' in parts:
        if ' / ' in parts:
            print(f'ERROR: Too complex {parts}')
            sys.exit(1)
        else:
            parts = parts.split('; ')
            ndx = 0
            while ndx < len(parts):
                parts[ndx] = f'[`{parts[ndx]}`]({base}{parts[ndx].replace(",", "").replace(" ", "%20")})'
                ndx += 1
            return '`; `'.join(parts)
    if ' / ' in parts:
        parts = parts.split(' / ')
        ndx = 0
        while ndx < len(parts):
            parts[ndx] = f'[`{parts[ndx]}`]({base}{parts[ndx].replace(",", "").replace(" ", "%20")})'
            ndx += 1
        return '` / `'.join(parts)
    return f'[`{parts}`]({base}{parts.replace(",", "").replace(" ", "%20")})'

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
    for match in (' (na', ' (tot', ' (ca. ', ' (1', ' (2', ' (3', ' (4', ' (5',
                  ' (6', ' (7', ' (8', ' (9'):
        pos = line.find(match)
        if pos != -1:
            line = line[:pos]
    for match in (' (familie)', ' (district)', ' (stad)', ' (volgende dag)',
                  ' (overige)', ' (trustgebied)', ', op het Engels gebaseerd',
                  ', op het Frans gebaseerd', ', op het Portugees gebaseerd'):
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


def write_spelling(spel, code, en, nl):
    '''Write spelling checker information.'''
    spell = hun_obj.spell(nl)
    count = 0
    if not spell:
        if ' ' in nl:
            for subterm in nl.split(' '):
                #TODO also in opentaal-woordinfo
                if subterm[0] == '(':
                    subterm = subterm[1:]
                for end in (';', ',', ')'):
                    if subterm[-1] == end:
                        subterm = subterm[:-1]
                if subterm != '' and not hun_obj.spell(subterm):
                    spel.write(f'`{code}` | `{en}` | `{nl}` | `{subterm}`\n')
                    count += 1
        else:
            spel.write(f'`{code}` | `{en}` | `{nl}` | `{nl}`\n')
            count += 1
    return count


def main():
    '''Run main functionality.'''
    utcnow = datetime.utcnow()
    dtstamp = utcnow.strftime('%Y-%m-%d %H:%M:%S UTC')
    directory = Path(path.join(path.join(__location__, '..'), 'weblate'))
    base_en = 'https://en.wikipedia.org/w/index.php?search='
    base_nl = 'https://nl.wikipedia.org/w/index.php?search='
    isos = {}

    #TODO move to inside weblate loop
    # data_639_2_alpha_2 = {}
    data_639_2_alpha_3 = {}
    data_639_3_alpha_3 = {}
    data_639_5_alpha_3 = {}
    data_3166_1_alpha_2 = {}
    data_3166_1_alpha_3 = {}
    data_3166_2_code = {}
    data_3166_3_alpha_2 = {}
    data_3166_3_alpha_3 = {}
    data_3166_3_alpha_4 = {}
    for dataname in sorted(('639-2', '639-3', '639-5', '3166-1', '3166-2', '3166-3', '4217', '15924')):
        with open(path.join(__location__, f'../data/iso_{dataname}.json')) as filepath:  # pylint:disable=unspecified-encoding
            keys = {}
            data = load(filepath)
            for entry in data[dataname]:
                if dataname == '3166-1':
                    data_3166_1_alpha_2[entry['alpha_2']] = {'alpha_3': entry['alpha_3'],
                                                             'flag': entry['flag'],
                                                             'name': entry['name']}
                    data_3166_1_alpha_3[entry['alpha_3']] = {'alpha_2': entry['alpha_2'],
                                                             'flag': entry['flag'],
                                                             'name': entry['name']}
                    if 'official_name' in entry.keys():
                        data_3166_1_alpha_2[entry['alpha_2']]['official_name'] = entry['official_name']
                        data_3166_1_alpha_3[entry['alpha_3']]['official_name'] = entry['official_name']
                    if 'common_name' in entry.keys():
                        data_3166_1_alpha_2[entry['alpha_2']]['common_name'] = entry['common_name']
                        data_3166_1_alpha_3[entry['alpha_3']]['common_name'] = entry['common_name']
                elif dataname == '3166-2':
                    data_3166_2_code[entry['code']] = {'name': entry['name'],
                                                       'type': entry['type']}
                    if 'parent' in entry.keys():
                        data_3166_2_code[entry['code']]['parent'] = entry['parent']
                elif dataname == '3166-3':
                    data_3166_3_alpha_2[entry['alpha_2']] = {'alpha_3': entry['alpha_3'],
                                                             'alpha_4': entry['alpha_4'],
                                                             'withdrawal_date': entry['withdrawal_date'],
                                                             'name': entry['name']}
                    data_3166_3_alpha_3[entry['alpha_3']] = {'alpha_2': entry['alpha_2'],
                                                             'alpha_4': entry['alpha_4'],
                                                             'withdrawal_date': entry['withdrawal_date'],
                                                             'name': entry['name']}
                    data_3166_3_alpha_4[entry['alpha_4']] = {'alpha_2': entry['alpha_2'],
                                                             'alpha_3': entry['alpha_3'],
                                                             'withdrawal_date': entry['withdrawal_date'],
                                                             'name': entry['name']}
                    if 'common_name' in entry.keys():
                        data_3166_3_alpha_2[entry['alpha_2']]['numeric'] = entry['numeric']
                        data_3166_3_alpha_3[entry['alpha_3']]['numeric'] = entry['numeric']
                        data_3166_3_alpha_4[entry['alpha_4']]['numeric'] = entry['numeric']
                elif dataname == '639-2':
                    data_639_2_alpha_3[entry['alpha_3']] = {'name': entry['name']}
                    if 'alpha_2' in entry.keys():
                        data_639_2_alpha_3[entry['alpha_3']]['alpha_2'] = entry['alpha_2']
                    if 'bibliographic' in entry.keys():
                        data_639_2_alpha_3[entry['alpha_3']]['bibliographic'] = entry['bibliographic']
                    if 'common_name' in entry.keys():
                        data_639_2_alpha_3[entry['alpha_3']]['common_name'] = entry['common_name']
                elif dataname == '639-3':
                    data_639_3_alpha_3[entry['alpha_3']] = {'name': entry['name'], 'scope': entry['scope'], 'type': entry['type']}
                    if 'inverted_name' in entry.keys():
                        data_639_3_alpha_3[entry['alpha_3']]['inverted_name'] = entry['inverted_name']
                    if 'alpha_2' in entry.keys():
                        data_639_3_alpha_3[entry['alpha_3']]['alpha_2'] = entry['alpha_2']
                    if 'bibliographic' in entry.keys():
                        data_639_3_alpha_3[entry['alpha_3']]['bibliographic'] = entry['bibliographic']
                    if 'common_name' in entry.keys():
                        data_639_3_alpha_3[entry['alpha_3']]['common_name'] = entry['common_name']
                elif dataname == '639-5':
                    data_639_5_alpha_3[entry['alpha_3']] = {'name': entry['name']}
                for key in entry.keys():
                    if key in keys:
                        keys[key] += 1
                    else:
                        keys[key] = 1
            print(f'Keys in datafile iso_{dataname}.json')
            for key, count in sorted(keys.items(), key=itemgetter(1), reverse=True):
                print(f'\t{count}\t{key}')

    countries_en = {}
    countries_nl = {}
    regions_en = {}
    regions_nl = {}
    languages_en = {}
    languages_nl = {}
    print('\nName\t\tMax. length EN~NL\tTrans.\tTotal = Trans. + Fuzzy + Untrans.\tSpelling')
    for sourcepath in sorted(Path(directory.resolve()).glob('*/nl.po')):
        iso = sourcepath.parts[-2]
        name = iso.replace('iso_', 'ISO ')
        isos[iso] = name
        with open(path.join(path.join(__location__, '..'), f'html/{iso}.html'), 'w') as html, \
        open(path.join(path.join(__location__, '..'), f'md/{iso}.md'), 'w') as mado, \
        open(path.join(path.join(__location__, '..'), f'spelling/{iso}.md'), 'w') as spel, \
        open(path.join(path.join(__location__, '..'), f'tsv/{iso}.tsv'), 'w') as tsv:  # pylint:disable=unspecified-encoding
            sourcefile = pofile(sourcepath)
            header(html, mado, spel, name)
            desc = description(iso, base_nl)
            html.write('<p>Voor gebruik, lees de <a href="https://github.com/opentaal/opentaal-isocodes">documentatie</a> goed door. Deze bestanden zijn alleen voor reviewdoeleinden! Maak een <a target="_blank" href="https://github.com/OpenTaal/opentaal-isocodes/issues">issue</a> aan voor het geven van feedback.</p>\n')
            html.write(f'<p><a target="_blank" href="{desc[1]}">{desc[0]}</a>. Totaal {len(sourcefile)} ISO-codes, {sourcefile.percent_translated()}% is vertaald op {dtstamp}.</p>\n')
            mado.write('Voor gebruik, lees de [documentatie](https://github.com/opentaal/opentaal-isocodes) goed door. Deze bestanden zijn alleen voor reviewdoeleinden! Maak een [issue](https://github.com/OpenTaal/opentaal-isocodes/issues) aan voor het geven van feedback.\n')
            mado.write('\n')
            mado.write(f'[{desc[0]}]({desc[1]}). Totaal {len(sourcefile)} ISO-codes, {sourcefile.percent_translated()}% is vertaald op {dtstamp}.\n')
            spel.write('Voor gebruik, lees de [documentatie](https://github.com/opentaal/opentaal-isocodes) goed door. Deze bestanden zijn alleen voor reviewdoeleinden! Maak een [issue](https://github.com/OpenTaal/opentaal-isocodes/issues) aan voor het geven van feedback.\n')
            spel.write('\n')
            spel.write('Onderstaande tabel geeft een code, Engelse naam, Nederlandse naam en welk deel van de Nederlandse naam niet door de spellingcontrole wordt ondersteund. M.a.w. als spelfout wordt aangeduid.\n')
            spel.write('\n')

            codes = {}
            max_len_msgid = 0
            max_len_msgstr = 0
            spell_count = 0
            for entry in sourcefile.translated_entries() + sourcefile.fuzzy_entries(): #TODO report fuzzy seperately
                for comment in entry.comment.split(', '):
                    pos = comment.rfind(' ')
                    comment = f'{comment[pos+1:]}, {comment[:pos]}'
                    if comment in codes:
                        print(f'ERROR: Duplicate code {comment}')
                    else:
                        if len(entry.msgid) > max_len_msgid:
                            max_len_msgid = len(entry.msgid)
                        if len(entry.msgstr) > max_len_msgstr:
                            max_len_msgstr = len(entry.msgstr)
                        codes[comment] = (entry.msgid, entry.msgstr)
            for entry in sourcefile.untranslated_entries():
                for comment in entry.comment.split(', '):
                    pos = comment.rfind(' ')
                    comment = f'{comment[pos+1:]}, {comment[:pos]}'
                    if comment in codes:
                        print(f'ERROR: Duplicate code {comment}')
                    else:
                        if len(entry.msgid) > max_len_msgid:
                            max_len_msgid = len(entry.msgid)
                        codes[comment] = (entry.msgid, 'NOG NIET VERTAALD')

            # html.write(f'<h2>Vertaald ({len(sourcefile.translated_entries())}), onvertaald </h2>')
            html.write('<table>\n')
            mado.write('\n')
            spel.write('\n')
            if iso == 'iso_3166-1':
                html.write('<tr><th>Code</th>'
                           '<th>Kort</th>'
                           '<th>Vlag</th>'
                           '<th>Engels</th>'
                           '<th>Nederlands</th></tr>\n') #TODO refactor voor achtergrondkleur, niet via browser
                mado.write('Code | Kort | Vlag | Engels | Nederlands\n')
                mado.write('---|---|---|---|---\n')
                spel.write('Code | Engels | Nederlands | Spelling niet ondersteund\n')
                spel.write('---|---|---|---\n')
                tsv.write('Code\tKort\tVlag\tEngels\tNederlands\n')
                for code, value in sorted(codes.items()):
                    pos = code.find(', ')
                    data_code = code[:pos]
                    data_name = data_3166_1_alpha_3[data_code]['name']
                    data_short = data_3166_1_alpha_3[data_code]['alpha_2']
                    data_flag = data_3166_1_alpha_3[data_code]['flag']
                    # if data_name != '' and data_name != value[0]:
                        # print(f'WARNING: Mismatch data name "{data_name}" with msgid "{value[0]}" for code "{data_code}"')
                    html.write(f'<tr><td>{htmlcomment(code, base_en)}</td>'
                               f'<td>{data_short}</td>'
                               f'<td>{data_flag}</td>'
                               f'<td>{htmlpart(value[0], base_en)}</td></tr>\n')
                    mado.write(f'{madocomment(code, base_en)} | '
                               f'`{data_short}` |'
                               f'{data_flag} |'
                               f'{madopart(value[0], base_en)} | '
                               f'{madopart(value[1], base_nl)}\n')
                    tsv.write(f'{code}\t{data_short}\t{data_flag}\t{value[0]}\t{value[1]}\n')
                    spell_count += write_spelling(spel, code, value[0], value[1])
                    if code[pos:] == ', Name for':
                        countries_en[data_short] = value[0]
                        countries_nl[data_short] = value[1]
            elif iso == 'iso_3166-2':
                html.write('<tr><th>Code</th>'
                           '<th>Type</th>'
                           '<th>Engels</th>'
                           '<th>Nederlands</th></tr>\n')
                mado.write('Code | Type | Engels | Nederlands\n')
                mado.write('---|---|---|---\n')
                spel.write('Code | Engels | Nederlands | Spelling niet ondersteund\n')
                spel.write('---|---|---|---\n')
                tsv.write('Code\tType\tEngels\tNederlands\n')
                for code, value in sorted(codes.items()):
                    pos = code.find(', ')
                    data_code = code[:pos]
                    data_name = data_3166_2_code[data_code]['name']
                    data_type = data_3166_2_code[data_code]['type']
                    if data_name not in ('', value[0]):
                        cprint(f'WARNING: Mismatch data name "{data_name}" with msgid "{value[0]}" for code "{data_code}"', 'yellow')
                    html.write(f'<tr><td>{htmlcomment(code, base_en)}</td>'
                               f'<td>{data_type}</td>'
                               f'<td>{htmlpart(value[0], base_en)}</td>'
                               f'<td>{htmlpart(value[1], base_nl)}</td></tr>\n')
                    mado.write(f'{madocomment(code, base_en)} | '
                               f'`{data_type}` | '
                               f'{madopart(value[0], base_en)} | '
                               f'{madopart(value[1], base_nl)}\n')
                    tsv.write(f'{code}\t{data_type}\t{value[0]}\t{value[1]}\n')
                    spell_count += write_spelling(spel, code, value[0], value[1])
                    #TODO value[] for index for better sort
                    regions_en[countries_en[data_code[:2]] + data_code] = (data_code, f'{countries_en[data_code[:2]]}: {value[0]}')
                    regions_nl[countries_nl[data_code[:2]] + data_code] = (data_code, f'{countries_nl[data_code[:2]]}: {value[1]}')
            else:
                html.write('<tr><th>Code</th>'
                           '<th>Engels</th>'
                           '<th>Nederlands</th></tr>\n')
                mado.write('Code | Engels | Nederlands\n')
                mado.write('---|---|---\n')
                spel.write('Code | Engels | Nederlands | Spelling niet ondersteund\n')
                spel.write('---|---|---|---\n')
                tsv.write('Code\tEngels\tNederlands\n')
                for code, value in sorted(codes.items()):
                    pos = code.find(', ')
                    data_code = code[:pos]
                    if iso == 'iso_639-5':
                        data_name = data_639_5_alpha_3[data_code]['name']
                        if data_name not in ('', value[0]):
                            print(f'WARNING: Mismatch data name "{data_name}" '
                                  'with msgid "{value[0]}" for code "{data_code}"')
                    html.write(f'<tr><td>{htmlcomment(code, base_en)}</td>'
                               f'<td>{htmlpart(value[0], base_en)}</td>'
                               f'<td>{htmlpart(value[1], base_nl)}</td></tr>\n')
                    mado.write(f'{madocomment(code, base_en)} | '
                               f'{madopart(value[0], base_en)} | '
                               f'{madopart(value[1], base_nl)}\n')
                    tsv.write(f'{code}\t{value[0]}\t{value[1]}\n')
                    spell_count += write_spelling(spel, code, value[0], value[1])
                    if iso == 'iso_639-2':
                        if code[pos:] == ', Name for' and data_code != 'zxx':
                            if data_code in languages_en or data_code in languages_nl:
                                print('ERROR')
                                sys.exit(1)
                            languages_en[value[0].replace('; German, Low; Saxon, Low', '')] = data_code
                            languages_nl[value[1].replace('; Duits, Neder en Saksisch, Neder', '')] = data_code
            html.write('</table>\n')
            footer(html, mado)

            print(f'{name}\t'
                  f'{max_len_msgid:04d}~{max_len_msgstr:04d}\t\t'
                  f'{sourcefile.percent_translated():03d}%\t'
                  f'{len(sourcefile):04d} = '
                  f'{len(sourcefile.translated_entries()):04d} + '
                  f'{len(sourcefile.fuzzy_entries()):04d} + '
                  f'{len(sourcefile.untranslated_entries()):04d}\t\t'
                  f'{spell_count:04d}')

    # Write JSON files for HTML select field.

    countries_sort = ('NL', 'BE', 'SR', 'DE', 'AT', 'CH', 'FR', 'ES', 'IT')
    # max_len = 0
    with open(path.join(__location__, '../json/regions.json'), 'w') as jsonfile:  # pylint:disable=unspecified-encoding
        jsonfile.write('{\n')
        jsonfile.write('    "en": [')
        jsonfile.write('\n        ["", "- choose a region -"]')
        for country in countries_sort:
            for key, values in sorted(regions_en.items()):
                code, name = values
                if code[:2] == country:
                    jsonfile.write(f',\n        ["{code}", "{name}"]')
        for key, values in sorted(regions_en.items()):
            code, name = values
            # if len(code) > max_len:
                # max_len = len(code)
            if code[:2] not in countries_sort:
                jsonfile.write(f',\n        ["{code}", "{name}"]')
        jsonfile.write('\n    ],\n')
        jsonfile.write('    "nl": [')
        jsonfile.write('\n        ["", "- kies een regio -"]')
        for country in countries_sort:
            for key, values in sorted(regions_nl.items()):
                code, name = values
                if code[:2] == country:
                    jsonfile.write(f',\n        ["{code}", "{name}"]')
        for key, values in sorted(regions_nl.items()):
            code, name = values
            # if len(code) > max_len:
                # max_len = len(code)
            if code[:2] not in countries_sort:
                jsonfile.write(f',\n        ["{code}", "{name}"]')
        jsonfile.write('\n    ]\n')
        jsonfile.write('}\n')
    # print('XXXX', max_len)

    languages_sort = ('nld', 'eng', 'deu', 'fra', 'spa', 'ita', 'gsw', 'nds', 'fry')
    # max_len = 0
    with open(path.join(__location__, '../json/languages.json'), 'w') as jsonfile:  # pylint:disable=unspecified-encoding
        jsonfile.write('{\n')
        jsonfile.write('    "en": [')
        jsonfile.write('\n        ["", "- choose a language -"]')
        for language in languages_sort:
            for name, code in sorted(languages_en.items()):
                if code == language:
                    jsonfile.write(f',\n        ["{code}", "{name}"]')
        for name, code in sorted(languages_en.items()):
            # if len(code) > max_len:
                # max_len = len(code)
            if code not in languages_sort:
                jsonfile.write(f',\n        ["{code}", "{name}"]')
        jsonfile.write('\n    ],\n')
        jsonfile.write('    "nl": [')
        jsonfile.write('\n        ["", "- kies een taal -"]')
        for language in languages_sort:
            for name, code in sorted(languages_nl.items()):
                if code == language:
                    jsonfile.write(f',\n        ["{code}", "{name}"]')
        for name, code in sorted(languages_nl.items()):
            # if len(code) > max_len:
                # max_len = len(code)
            if code not in languages_sort:
                jsonfile.write(f',\n        ["{code}", "{name}"]')
        jsonfile.write('\n    ]\n')
        jsonfile.write('}\n')
    # print('XXXX', max_len)

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
