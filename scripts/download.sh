#!/bin/bash
set -e

cd ..

if [ -e data ]; then
    rm -rf data
fi
mkdir data
cd data
for i in 639-2 639-3 639-5 4217 3166-1 3166-2 3166-3 15924; do
    wget -O iso_$i.json \
    https://salsa.debian.org/iso-codes-team/iso-codes/-/raw/main/data/iso_$i.json?inline=false
done
cd ..

if [ -e weblate ]; then
    rm rf weblate
fi
mkdir weblate
cd weblate
wget -O iso-codes.zip \
https://hosted.weblate.org/download-language/nl/iso-codes/?format=zip
unzip -o iso-codes.zip
rm -f iso-codes.zip
mv iso-codes/iso-639-2/* .
rm -rf ico-codes
rm -rf iso*/*.pot
cd ..
