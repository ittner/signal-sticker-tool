#!/bin/sh

#
# Utility script to download sticker packs from getstickerpack.com.
#
# To use it, just run "./convert-getstickerpack.sh SOME-PACK-NAME"
# where SOME-PACK-NAME is the name of the sticker pack. It will create
# a directory with the same name, unpack the stickers there, and build
# an index that signal-sticker-tool can use -- however, you will need
# to add the emoji associations manually.
#

set -e

PACKNAME="$1"
if [ "x$PACKNAME" = "x" ]; then
    echo "Usage: $0 <packname>"
    exit 1
fi

mkdir $PACKNAME
cd $PACKNAME
wget https://getstickerpack.com/stickers/$PACKNAME/download -O $PACKNAME.zip
unzip $PACKNAME.zip
cd ..
./make-getstickerpack-index.py $PACKNAME


echo
echo "Sticker index generated in file $PACKNAME/stickers.yaml"
echo
echo "The script can't generate good emoji associations automatically, so"
echo "edit this file to ensure they make some sense."
echo 
echo "Then upload the pack to Signal and publish it somewhere other people"
echo "can find it."
echo
