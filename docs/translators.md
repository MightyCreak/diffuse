# Translators documentation

Below are basic instructions for adding and maintaining Gettext translations
for Diffuse.  The installer will discover .po files in this directory and
compile them into the corresponding .mo files.

The example commands below show how to create and manage the Japanese
translations.  Replace all instances of "ja" with the code for the desired
language.

## Create PO template

To create or update the PO template (`po/diffuse.pot`), use this command at the
repo root:

```sh
xgettext -w 84 -o po/diffuse.pot -f po/POTFILES
```

Regenerating the POT file will add a bunch of new lines coming from
`data/io.github.mightycreak.Diffuse.appdata.xml.in`. Not all the lines need to
be translated in this file. In `diffuse.pot`, look for the comment
`Translators: no need to translate after this comment`, and remove all the
added lines for this file.

_Note:_ why 84 characters, you ask? because the usage text has to be 80-char
wide, plus the beginning and ending `"` and the final `\n` (which is two
characters).

## Create a new translation

To create a new translation file, you'll need a PO template. If not already
created, refer to previous section "Create PO template".

1. Create a .po file for the translation (replace `<lang>` with your language):

   ```sh
   msginit -w 84 -l <lang> -o <lang>.po -i diffuse.pot
   ```

2. Manually complete in the translations in the .po file using either an
   application for that such as [Gtranslator][gtranslator] or directly with a
   text editor such as [gedit][gedit] or [vim][vim].

[gtranslator]: https://www.flathub.org/apps/details/org.gnome.Gtranslator
[gedit]: https://www.flathub.org/apps/details/org.gnome.gedit
[vim]: https://www.vim.org/

## Update a translation

Use `update-translations.py` to update one or more PO files.

Here is an example with the Japanese and Korean translations, respectively
`ja.po` and `ko.po`:

Command-line:

```sh
./update-translations.py ja.po ko.po
```

This command also validate the files, so if you see a message saying "N
untranslated messages", use the text editor of your choice to complete the
translations.

## Validate a translation

Use `update-translations.py` to validate one or more PO files.

Here is an example with `ja.po` and `ko.po`:

Command-line:
```sh
./update-translations.py --check-only ja.po ko.po
```

## Windows-specific files

### Installer

Localized text for the Microsoft Windows installer is stored in separate ISL
files. Copy the [English version][english-win-docs] and replace the text to the
right of each equal sign.

[english-win-docs]: ../windows-installer/en.isl

### DocBook

Diffuse's help documentation is written in the DocBook format and can be easily
converted into other formats using XSLT stylesheets. If the local help
documentation or its browser are unavailable, Diffuse will attempt to display
the on-line help documentation using a web browser.

Start a new translation of the manual by copying the English version of the
[DocBook manual][docbook-manual] and then edit the contents.

The DocBook manual is converted to HTML for Windows and Unix man pages for
POSIX platforms. The conversion tools insert some English text that gets
localized using search and replace. Manually add new search and replace rules
to these files:

    ../windows-installer/translations.txt
    ../utils/translations.txt

The format of each line is: \<language id\>:\<English text\>:\<localised text\>

[docbook-manual]: ../data/usr/share/gnome/help/diffuse/C/diffuse.xml
