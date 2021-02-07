Random utilities for signal-sticker-tool
========================================


This directory has a few ad-hoc scripts intended to be used together with `signal-sticker-tool`. Feel free to add your own.




## `convert-getstickerpack.sh` and `make-getstickerpack-index.py`

There is an app called "Sticker maker for WhatsApp" which seems to be a bit popular among Brazilian WhatsApp users. I never used neither of them, but once a recently-"converted" contact asked me how to add these stickers to Signal. So I launched a MitM-proxied WLAN, asked him to connect through it, and noticed that all this app did was download .zip packs from "getstickerpack.com". Quick conversion task...

To use it, just note the name of the sticker pack and run `./convert-getstickerpack.sh THAT-PACK-NAME`. The first script will download and unpack the stickers in a directory with the same name and launch the second one to generate a YAML definition file that `signal-sticker-tool` can use.

There will be no automatic emoji/sticker associations, just placeholders. Add some if you want then upload the stickers to Signal.
