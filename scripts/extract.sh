#!/bin/bash
set -e

cd ..
if [ -d iso-codes ]; then
    rm -rf iso-codes
fi
unzip iso-codes.zip
cd iso-codes
rm -rf glossary
mv iso-639-2/* .
rmdir iso-639-2
for i in *; do
    cd $i
    rm -f $(ls *.po|grep -v nl.po) *.pot
    cd ..
done
