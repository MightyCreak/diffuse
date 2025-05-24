#!/bin/bash
## Prepare files for a new release.

## This script automate this process:
## 1. Update these files with new version and new date:
##    - meson.build
##    - data/usr/share/gnome/help/diffuse/*/diffuse.xml
##    - data/usr/share/omf/diffuse/diffuse-*.omf
##    - utils/book2manual.xsl
##    - windows-installer/build.py
##    - windows-installer/diffuse.iss
##    - windows-installer/diffuse.new.iss
## 2. Update CHANGELOG.md
##    - Add new line under `## Unreleased` following this syntax: `## x.y.z - YYYY-MM-DD`
## 3. Update AppData release notes in data/io.github.mightycreak.Diffuse.appdata.xml.in:
##    - Create a new `<release>` tag under `<releases>`, fill the `version` and `date` attributes
##    - Create a new `<description>` tag under the new `<release>` tag
##    - Create a new `<p>` tag under the new `<description>` tag

set -e

if [ "$#" -ne "1" ]; then
    echo "Usage: $0 NEW_VERSION"
    exit 1
fi

NEW_VERSION=$1
DATE_FULL=$(date +%F)
DATE_YEAR=$(date +%Y)

echo "Changing files for new version $NEW_VERSION..."

# meson.build
sed -i -E "s/\bversion: '.+?',/version: '$NEW_VERSION',/" \
    meson.build

# GNOME help (.xml and .omf)
sed -i -E "s#<!ENTITY app-version \".+?\">#<!ENTITY app-version \"$NEW_VERSION\">#" \
    data/usr/share/gnome/help/diffuse/*/diffuse.xml
sed -i -E "s#<!ENTITY app-year \"2006-\d+\">#<!ENTITY app-year \"2006-$DATE_YEAR\">#" \
    data/usr/share/gnome/help/diffuse/*/diffuse.xml
sed -i -E "s#<!ENTITY manual-year \"2009-\d+\">#<!ENTITY manual-year \"2009-$DATE_YEAR\">#" \
    data/usr/share/gnome/help/diffuse/*/diffuse.xml

sed -i -E "s#<version identifier=\".+?\" date=\".+?\"/>#<version identifier=\"$NEW_VERSION\" date=\"$DATE_FULL\"/>#" \
    data/usr/share/omf/diffuse/diffuse-*.omf
sed -i -E "s#<date>.+?</date>#<date>$DATE_FULL</date>#" \
    data/usr/share/omf/diffuse/diffuse-*.omf

# book2manual.xsl
sed -i -E "s#<!ENTITY app-version \".+?\">#<!ENTITY app-version \"$NEW_VERSION\">#" \
    utils/book2manual.xsl
sed -i -E "s#<!ENTITY date \".+?\">#<!ENTITY date \"$DATE_FULL\">#" \
    utils/book2manual.xsl

# Windows installer (unmaintaned)
sed -i -E "s/VERSION = '.+?'/VERSION = '$NEW_VERSION'/" \
    windows-installer/build.py
sed -i -E "s/AppVerName=Diffuse .+?/AppVerName=Diffuse $NEW_VERSION/" \
    windows-installer/diffuse.iss
sed -i -E "s/#define MyAppVersion \".+?\"/#define MyAppVersion \"$NEW_VERSION\"/" \
    windows-installer/diffuse.iss

# AppData
new_release="    <release version=\"$NEW_VERSION\" date=\"$DATE_FULL\">
      <description>
        <p></p>
      </description>
    </release>"
echo "$new_release" | sed -i "/<releases>/r /dev/stdin" \
    data/io.github.mightycreak.Diffuse.appdata.xml.in

# CHANGELOG.md
new_changelog="
## [$NEW_VERSION] - $DATE_FULL"
echo "$new_changelog" | sed -i "/^## Unreleased$/r /dev/stdin" \
    CHANGELOG.md

echo "Changes done."
echo
echo "Don't forget to add the compare link in CHANGELOG.md."
