# ISO-codes

_Nederlandse vertaling van ISO-codes._

Dutch translation of ISO codes.

## Source

The upstream source is https://salsa.debian.org/iso-codes-team/iso-codes

## Prerequisits

For generating the HTML, MarkDown and TSV files in this repository, install
[polib](https://pypi.org/project/polib/) with e.g.:

    sudo pip3 install -U polib

Then in the directory `scripts`, run:

    ./download.sh
    ./extracht.sh
    ./convert.py

## Usage

The files offered here are only for improving Dutch word list, spelling
checking, hyphenations patterns, etc. For using the upstream translations, see
for example:
- TODO Debian package
- TODO pycountry package

## Contributing

Translating the remaining language names is not trivial. Only when you are
very sure about your Dutch translation skills, please contribute via
https://hosted.weblate.org/languages/nl/iso-codes/

For questions regarding existing translations, you can also open an issue
at https://github.com/OpenTaal/opentaal-isocodes/issues
Standaard | Beschrijving | Vertalingen
---|---|---
ISO 15924 | [Vierletterige codes schriftsystemen](https://nl.wikipedia.org/wiki/ISO_15924) | [HTML](iso_15924.html) [MD](iso_15924.md) [TSV](iso_15924.tsv)
ISO 3166-1 | [Drieletterige codes landnamen](https://nl.wikipedia.org/wiki/ISO_3166-1) | [HTML](iso_3166-1.html) [MD](iso_3166-1.md) [TSV](iso_3166-1.tsv)
ISO 3166-2 | [Codes onderverdelingen van landen](https://nl.wikipedia.org/wiki/ISO_3166-2) | [HTML](iso_3166-2.html) [MD](iso_3166-2.md) [TSV](iso_3166-2.tsv)
ISO 3166-3 | [Vierletterige codes voormalige landen](https://nl.wikipedia.org/wiki/ISO_3166-3) | [HTML](iso_3166-3.html) [MD](iso_3166-3.md) [TSV](iso_3166-3.tsv)
ISO 4217 | [Drieletteringe codes valuta's](https://nl.wikipedia.org/wiki/ISO_4217) | [HTML](iso_4217.html) [MD](iso_4217.md) [TSV](iso_4217.tsv)
ISO 639-2 | [Drieletteringe codes talen](https://nl.wikipedia.org/wiki/ISO_639#ISO_639-2) | [HTML](iso_639-2.html) [MD](iso_639-2.md) [TSV](iso_639-2.tsv)
ISO 639-3 | [Drieletteringe codes alle talen](https://nl.wikipedia.org/wiki/ISO_639#ISO_639-3) | [HTML](iso_639-3.html) [MD](iso_639-3.md) [TSV](iso_639-3.tsv)
ISO 639-5 | [Drieletterige codes taalfamilies](https://en.wikipedia.org/wiki/ISO_639-5) | [HTML](iso_639-5.html) [MD](iso_639-5.md) [TSV](iso_639-5.tsv)
