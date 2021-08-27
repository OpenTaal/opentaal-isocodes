#!/usr/bin/env python3
'''Convert PO files to HTML.'''

from datetime import datetime
from os import getcwd, path
from pathlib import Path
from polib import pofile

__location__ = path.realpath(path.join(getcwd(), path.dirname(__file__)))


def description(iso):
    '''Describe an ISO standard.'''
    descriptions = {'iso_15924': ('Vierletterige codes schriftsystemen',
                                  'https://nl.wikipedia.org/wiki/ISO_15924'),
                    'iso_3166-1': ('Drieletterige codes landnamen',
                                   'https://nl.wikipedia.org/wiki/ISO_3166-1'),
                    'iso_3166-2': ('Codes onderverdelingen van landen',
                                   'https://nl.wikipedia.org/wiki/ISO_3166-2'),
                    'iso_3166-3': ('Vierletterige codes voormalige landen',
                                   'https://nl.wikipedia.org/wiki/ISO_3166-3'),
                    'iso_4217': ('Drieletterige codes valuta\'s',
                                 'https://nl.wikipedia.org/wiki/ISO_4217'),
                    'iso_639-2': ('Drieletterige codes talen',
                                  'https://nl.wikipedia.org/wiki/ISO_639#ISO_639-2'),
                    'iso_639-3': ('Drieletterige codes alle talen',
                                  'https://nl.wikipedia.org/wiki/ISO_639#ISO_639-3'),
                    'iso_639-5': ('Drieletterige codes taalfamilies',
                                  'https://en.wikipedia.org/wiki/ISO_639-5'),
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
    mado.write('')

def index(isos):
    '''Write index HTML.'''
    with open(path.join(path.join(__location__, '..'), 'index.html'), 'w') as html, \
    open(path.join(path.join(__location__, '..'), 'README.md'), 'w') as mado:
        header(html, mado, 'ISO-codes')

        mado.write('''_Nederlandse vertaling van ISO-codes voor verbetering schrijfhulpbestanden._

Dutch translation of ISO codes for improving writing aid files.

## Source

The upstream source is https://salsa.debian.org/iso-codes-team/iso-codes with
https://salsa.debian.org/iso-codes-team/iso-codes/-/blob/main/COPYING as
license.

## Usage

The files offered here are only for improving Dutch writing aid files such as
word list, spelling checker dictionary, hyphenations patterns, etc. The Dutch
translations are best used from upstream stable releases which are found at:
- [source files](https://salsa.debian.org/iso-codes-team/iso-codes/-/releases)
- [Debian package](https://packages.debian.org/search?keywords=iso-codes)
- [Ubuntu package](https://packages.ubuntu.com/search?keywords=iso-codes)

These contain XML files with translations in MO files. For use in Python,
please see [pycountry](https://pypi.org/project/pycountry/).

## Updating

For generating updated versions of the MarkDown, HTML and TSV files, install
[polib](https://pypi.org/project/polib/) with e.g.:

    sudo pip3 install -U polib

Then in the directory `scripts`, run:

    ./download.sh
    ./extracht.sh
    ./convert.py

## Contributing

Translating the remaining language names is not trivial. Only when you are
very sure about your Dutch translation skills, please contribute via
https://hosted.weblate.org/languages/nl/iso-codes/ . When using sources for
translations, be absolutely sure they are of high quality. Some are simply put
through a translation service and keep incorrect translation in orbit.

For questions regarding existing translations, you can also open an issue
at https://github.com/OpenTaal/opentaal-isocodes/issues to discuss
improvements before adding them to Weblate.

''')

        html.write('<p>Voor gebruik, lees de <a href="https://github.com/opentaal/opentaal-isocodes">documentatie</a> goed door. Deze bestanden zijn alleen voor reviewdoeleinden.</p>\n')
        html.write('<table>\n')
        html.write('<tr><th>Standaard</th><th>Beschrijving</th><th>Vertalingen</th></tr>\n')
        mado.write('Standaard | Beschrijving | Vertalingen\n')
        mado.write('---|---|---\n')
        for iso, name in sorted(isos.items()):
            desc = description(iso)
            html.write(f'<tr><td>{name}</td><td><a target="_blank" href="{desc[1]}">{desc[0]}</a></td><td><a href="html/{iso}.html">HTML</a> <a href="md/{iso}.md">MD</a> <a href="tsv/{iso}.tsv">TSV</a></td></tr>\n')
            mado.write(f'{name} | [{desc[0]}]({desc[1]}) | [MD](md/{iso}.md) [HTML](html/{iso}.html) [TSV](tsv/{iso}.tsv)\n')
        html.write('</table>\n')

        footer(html, mado)

def main():
    '''Run main functionality.'''
    utcnow = datetime.utcnow()
    dtstamp = utcnow.strftime('%Y-%m-%d %H:%M:%S UTC')
    directory = Path(path.join(path.join(__location__, '..'), 'iso-codes'))
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
            desc = description(iso)
            html.write('<p>Voor gebruik, lees de <a href="https://github.com/opentaal/opentaal-isocodes">documentatie</a> goed door. Deze bestanden zijn alleen voor reviewdoeleinden.</p>\n')
            html.write(f'<p><a target="_blank" href="{desc[1]}">{desc[0]}</a>. Totaal {len(sourcefile)} ISO-codes, {sourcefile.percent_translated()}% is vertaald op {dtstamp}.</p>\n')
            mado.write('Voor gebruik, lees de [documentatie](https://github.com/opentaal/opentaal-isocodes) goed door. Deze bestanden zijn alleen voor reviewdoeleinden.\n')
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
                    html.write(f'<tr><td style="font-family: monospace;">{entry.comment}</td><td style="font-family: monospace;">{entry.msgid}</td><td style="font-family: monospace;">{entry.msgstr}</td></tr>\n')
                    mado.write(f'`{entry.comment}` | `{entry.msgid}` | `{entry.msgstr}`\n')
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
                    html.write(f'<tr><td style="font-family: monospace;">{entry.comment}</td><td style="font-family: monospace;">{entry.msgid}</td></tr>\n')
                    mado.write(f'`{entry.comment}` | `{entry.msgid}`\n')
                    tsv.write(f'{entry.comment}\t{entry.msgid}\t\n')
                html.write('</table>\n')
            footer(html, mado)
    index(isos)

if __name__ == "__main__":
    main()
