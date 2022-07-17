#!/bin/bash
set -e

cd ..
wget -O iso-codes.zip https://hosted.weblate.org/download-language/nl/iso-codes/?format=zip
rm -rf iso-codes
unzip -o iso-codes.zip
rm -f iso-codes.zip
cd iso-codes
rm -rf glossary
mv iso-639-2 src
mv src/* .
rmdir src
rm -rf iso*/*.pot
