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

Use `update-translations.py` to update one or more PO files.

Here is an example with `ja.po` and `ko.po`:

Command-line:
```sh
./update-translations.py ja.po ko.po
```

Output:
```
Generate 'diffuse.pot'.
Updating translation file 'ja.po'...
Created /tmp/tmp0gtniydu/ja.empty.po.
Validate ja.po:
183 translated messages, 2 untranslated messages.
Update done.
Updating translation file 'ko.po'...
Created /tmp/tmp0gtniydu/ko.empty.po.
Validate ko.po:
183 translated messages, 2 untranslated messages.
Update done.
```

Then use the text editor of your choice to complete the translations.

Validate a translation
----------------------

Use `update-translations.py` to validate one or more PO files.

Here is an example with `ja.po` and `ko.po`:

Command-line:
```sh
./update-translations.py --check-only ja.po ko.po
```

Output:
```
Validate ja.po:
183 translated messages, 2 untranslated messages.
Validate ko.po:
183 translated messages, 2 untranslated messages.
```

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
