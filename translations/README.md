User Interface
==============

Below are basic instructions for adding and maintaining Gettext translations
for Diffuse.  The installer will discover .po files in this directory and
compile them into the corresponding .mo files.

The example commands below show how to create and manage the Japanese
translations.  Replace all instances of "ja" with the code for the desired
language.

Creating a new translation
--------------------------

1. Create a .pot file for Diffuse:

        $ xgettext -s -o diffuse.pot -L Python ../src/usr/bin/diffuse

2. Create a .po file for the translation:

        $ msginit -l ja -o ja.po -i diffuse.pot

3. Manually complete in the translations in the .po file:

        $ vi ja.po

Updating an existing translation
--------------------------------

1. Move the existing .po file:

        $ mv ja.po old.po

2. Create an empty .po file for the translation:

        $ xgettext -s -o diffuse.pot -L Python ../src/usr/bin/diffuse
        $ msginit -l ja -o empty.po -i diffuse.pot

3. Merge the old translations:

        $ msgmerge old.po empty.po -o ja.po

4. Clean up:

        $ rm old.po empty.po

5. Manually complete in the translations in the .po file:

        $ vi ja.po

Validate a translation
----------------------

1. Attempt to compile the .po file and note any warnings:

        $ msgfmt -c -v ja.po

System Integration
==================

Localised text for the system menu (name and comment) should be manually
added to the desktop file:

    ../src/usr/share/applications/diffuse.desktop

Localised text for the Microsoft Windows installer is stored in separate ISL
files.  Copy the English version (../windows-installer/en.isl) and replace the
text to the right of each equal sign.

Documentation
=============

Documentation is stored in DocBook format.  Start a new translation of the
manual by copying the English version of the DocBook manual
(../src/usr/share/gnome/help/diffuse/C/diffuse.xml) and then edit the
contents.

The DocBook manual is converted to HTML for Windows and Unix man pages for
POSIX platforms.  The conversion tools insert some English text that gets
localised using search and replace.  Manually add new search and replace rules
to these files:

    ../windows-installer/translations.txt
    ../utils/translations.txt

The format of each line is: \<language id\>:\<English text\>:\<localised text\>
