#!/usr/bin/env bash

# Use this tool if you need to re-create
# Diffuse.app/Contents/Resources/diffuse.icns
# in case the icon changes (unlikely).

sizes=(16 32 64 128 256 512)
for s in "${sizes[@]}"; do
  echo $s
  rsvg-convert -h $s "$1" > "icon_${s}x$s.png"
done

cp 'icon_32x32.png'     'icon_16x16@2x.png'
cp 'icon_64x64.png'     'icon_32x32@2x.png'
cp 'icon_256x256.png'   'icon_128x128@2x.png'
cp 'icon_512x512.png'   'icon_256x256@2x.png'

mkdir icon.iconset
mv icon_*x*.png icon.iconset
iconutil -c icns icon.iconset
