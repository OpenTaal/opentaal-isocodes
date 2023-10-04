![GitHub last commit](https://img.shields.io/github/last-commit/opentaal/opentaal-isocodes)
![GitHub commit activity](https://img.shields.io/github/commit-activity/y/opentaal/opentaal-isocodes)
![GitHub Repo stars](https://img.shields.io/github/stars/opentaal/opentaal-isocodes)
![GitHub watchers](https://img.shields.io/github/watchers/opentaal/opentaal-isocodes)
![GitHub Sponsors](https://img.shields.io/github/sponsors/opentaal)
![Liberapay patrons](https://img.shields.io/liberapay/patrons/opentaal)

# ISO-codes

_Nederlandse vertaling van ISO-codes voor verbetering schrijfhulpbestanden._

Dutch translation of ISO codes for improving writing aid files.

## Usage

The files offered below are intended for improving Dutch writing aid files such
as word list, spelling checker dictionary, hyphenations patterns, etc. However,
they can also be used in software applications.

The upstream package containing translations for Dutch and many other languages
is called isocodes, see:
- [releases](https://salsa.debian.org/iso-codes-team/iso-codes/-/releases)
- [Debian package](https://packages.debian.org/search?keywords=iso-codes)
- [Ubuntu package](https://packages.ubuntu.com/search?keywords=iso-codes)

It contains XML and JSON files with translations in MO files. For use in
Python, please see the package pycountry:
- [releases](https://salsa.debian.org/iso-codes-team/iso-codes/-/releases)
- [PyPI package](https://pypi.org/project/pycountry/)
- [Debian package](https://packages.debian.org/search?keywords=python3-pycountry)
- [Ubuntu package](https://packages.ubuntu.com/search?keywords=python3-pycountry)

Standard | Description | Dutch Translations
---|---|---
ISO 15924 | [Vierletterige codes schriftsystemen](https://nl.wikipedia.org/w/index.php?search=ISO_15924) | [MD](md/iso_15924.md) [HTML](html/iso_15924.html) [TSV](tsv/iso_15924.tsv)
ISO 3166-1 | [Drieletterige codes landnamen](https://nl.wikipedia.org/w/index.php?search=ISO_3166-1) | [MD](md/iso_3166-1.md) [HTML](html/iso_3166-1.html) [TSV](tsv/iso_3166-1.tsv)
ISO 3166-2 | [Codes onderverdelingen van landen](https://nl.wikipedia.org/w/index.php?search=ISO_3166-2) | [MD](md/iso_3166-2.md) [HTML](html/iso_3166-2.html) [TSV](tsv/iso_3166-2.tsv)
ISO 3166-3 | [Vierletterige codes voormalige landen](https://nl.wikipedia.org/w/index.php?search=ISO_3166-3) | [MD](md/iso_3166-3.md) [HTML](html/iso_3166-3.html) [TSV](tsv/iso_3166-3.tsv)
ISO 4217 | [Drieletterige codes valuta's](https://nl.wikipedia.org/w/index.php?search=ISO_4217) | [MD](md/iso_4217.md) [HTML](html/iso_4217.html) [TSV](tsv/iso_4217.tsv)
ISO 639-2 | [Drieletterige codes talen](https://nl.wikipedia.org/w/index.php?search=ISO_639#ISO_639-2) | [MD](md/iso_639-2.md) [HTML](html/iso_639-2.html) [TSV](tsv/iso_639-2.tsv)
ISO 639-3 | [Drieletterige codes alle talen](https://nl.wikipedia.org/w/index.php?search=ISO_639#ISO_639-3) | [MD](md/iso_639-3.md) [HTML](html/iso_639-3.html) [TSV](tsv/iso_639-3.tsv)
ISO 639-5 | [Drieletterige codes taalfamilies](https://nl.wikipedia.org/w/index.php?search=ISO_639-5) | [MD](md/iso_639-5.md) [HTML](html/iso_639-5.html) [TSV](tsv/iso_639-5.tsv)

See also the package isoquery:
- [releases](https://codeberg.org/toddy/isoquery/releases)
- [Debian package](https://packages.debian.org/search?keywords=isoquery)
- [Ubuntu package](https://packages.ubuntu.com/search?keywords=isoquery)


## Source

The upstream source is https://salsa.debian.org/iso-codes-team/iso-codes with
https://salsa.debian.org/iso-codes-team/iso-codes/-/blob/main/COPYING as
license.

## Updating

For generating updated versions of the MarkDown, HTML and TSV files, install the
required packages with:

    pip install -U polib

Then in the directory `scripts`, run:

    ./download.sh
    ./report.py

## Contribute

Translating the remaining language names is not trivial. Only when you are
very sure about your Dutch translation skills, please contribute via
https://hosted.weblate.org/languages/nl/iso-codes/ . When using sources for
translations, be absolutely sure they are of high quality. Some are simply put
through a translation service and keep incorrect translation in orbit.

For questions regarding existing translations, you can also open an issue
at https://github.com/OpenTaal/opentaal-isocodes/issues to discuss
improvements before adding them to Weblate.

Please, help us create free and open Dutch writing tools. Donate tax free to our
foundation at https://www.opentaal.org/vrienden-van-opentaal or contact us is
you have word lists to database skills to offer.

Donating is also possible with <noscript><a href="https://liberapay.com/opentaal/donate"><img alt="Donate using Liberapay" src="https://liberapay.com/assets/widgets/donate.svg"></a></noscript>
