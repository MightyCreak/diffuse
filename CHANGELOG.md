# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added

- Language: initial support for Rust language (@alopatindev)
- Translation: added Turkish translation (@libreajans)

### Changed

- Translation: updated Swedish translation (@eson57)
- Dialog: prompt only once if several files needs to be reloaded (@yuriiz)

### Fixed

- "Go to line..." dialog didn't show up (@MightyCreak)
- Tech debt: use `transient_for` instead of the deprecated `parent` when creating
  a `Gtk.Widget` (@MightyCreak)
- Documentation: prefer `pip3` over `pip` to ensure it works everywhere (@krlmlr)
- Flatpak: add missing `--filesystem=xdg-run/gvfsd` privilege (@MightyCreak)

## 0.7.7 - 2022-10-23

### Changed

- Translation: updated Spanish translation (@oscfdezdz)
- Translation: updated POT file
- Translation: fixed issue with commented string that still needs translation

## 0.7.6 - 2022-10-23

### Added

- Port to Mac OS (@hugoholgersson)

### Changed

- Documentation: added dev setup for MacOS
- Documentation: updated the dependencies
- CI/CD: GitHub actions warnings

### Fixed

- Fixed MyPy errors

## 0.7.5 - 2022-04-15

### Added

- Documentation: added release process instructions
- Translation: added French translation

### Fixed

- Fixed #156: Preferences cannot be saved in latest release
- Cleanups: use constructors instead of `new()` whenever possible in GTK
  classes

## 0.7.4 - 2022-04-03

### Added

- Added a `--remove-obsolete` option for the update-translation.py script
- Added links to VCSs in README.md
- New keyword in config file: "option"
- Added instructions to install and run from a custom directory

### Changed

- Updated the translation files
- Renamed POTFILES.in to POTFILES
- Renamed io.github.mightycreak.Diffuse.metadata.xml.in to
  io.github.mightycreak.Diffuse.appdata.xml.in
- Leaner README.md
- Moved the documentation to docs/
- Renamed application name from "Diffuse Merge Tool" to "Diffuse"
- Linters can be run sooner (before installation)
- Better messages when an error occurs while parsing the config file
- Start converting the code to static types
- Add more information about the dependencies in the documentation
- Upgrade Flatpak GNOME's runtime to 42

### Fixed

- Removed the lasting lint errors (i.e. in main.py)
- Fix Flatpak runtime version in documentation

## 0.7.3 - 2021-11-22

### Added

- Added linters (flake8 and mypy) and fixed some errors
- Added lint jobs for both in the CI
- Added a flatpak job in the CI
- Created a requirements.dev.txt just for the developers

### Changed

- main.py slimmed down by about 5000 lines
- The new widgets.py is a bit fat though (~4000 lines)

### Fixed

- The intense code cleaning seems to have fixed a bug with the `-c` argument
  (#120)

## 0.7.2 - 2021-11-18

### Added

- New options: log_print_output and log_print_stack, to print the log messages
  on the output and code stack
- New log function: utils.logErrorAndDialog, to both log and show a dialog
  message

### Changed

- Modularized the VCSs (reducing main.py by around 1300 lines)
- Bump GNOME runtime version from 3.38 to 41

### Fixed

- Fixed 'APP_NAME' error when opening non existing file
- Fixed the Portuguese Brazilian (pt_BR) translation

## 0.7.1 - 2021-11-17

### Fixed

- Fixed #103: the flatpak app can now call binaries on the host, such as `git`,
  `svn`, etc. (PR #105)

## 0.7.0 - 2021-11-16

### Added

- Added MetaInfo file
- New SVG icon (thanks @creepertron95, @jimmac and @freddii)
- Started modularizing the code

### Changed

- Changed AppID to io.github.mightycreak.Diffuse (as explained in
  [Flatpak documentation](https://docs.flatpak.org/en/latest/conventions.html#application-ids))
- Renamed `translations/` to `po/`
- Now uses POTFILES.in to list the files to translate
- Translation strings are no longer sorted alphabetically, this will help when
  there will be several files in POTFILES.in
- Updated the documentation and script in the `po/` directory
- Add .desktop translations in .po files

### Fixed

- Fixed some GTK deprecation warnings

## 0.6.0 - 2020-11-29

### Added

- New Flatpak package, published on Flathub: com.github.mightycreak.Diffuse

### Changed

- Replace old install.py with the more standard Meson
- Remove `u` string prefixes since Python 3 is in UTF-8 by default
- Replaced some interpolation operators (`%`) for the `f` string prefix
- Use the window scale factor for the icons generation

## 0.5.0 - 2020-07-18

### Added

- added Pedro Albuquerque's Portuguese translation
- added Åke Engelbrektson's Swedish translation
- added Guillaume Hoffmann's Darcs support improvements
- added support for Git submodules
- added Akom Chotiphantawanon's Thai translation
- added a preference and command line option to specify the version control
  system search order
- added .editorconfig file
- added .gitignore file
- added message when removing files during uninstallation
- added Python script to update all the translation files at once

### Changed

- convert to Python 3
- convert to GTK 3
- updated Python highlighting for Python 3 grammar
- updated copyrights years and authors
- improve Spanish translation
- convert translation README to MarkDown
- updated all the translation files

### Fixed

- fixed wrong icons directory for gtk-update-icon-cache
- fixed missing directories when uninstalling
- fixed bug introduced by r420 with RCS VCS
- fixed broken drag'n'drop since migration to Python3/GTK3
- fixed error when using '-m' in an SVN repo

## 0.4.8 - 2014-07-18

### Added

- updated use of gtk.SpinButton and gtk.Entry to avoid quirks seen on some platforms
- updated C/C++ syntax highlighting to recognise C11/C++11 keywords
- improved image quality of icons
- added Chi Ming and Wei-Lun Chao's Traditional Chinese translation

### Fixed

- fixed a bug that prevented Diffuse from reviewing large git merge conflicts
- fixed a bug that prevented drag-and-drop of file paths with non-ASCII characters

## 0.4.7 - 2013-05-13

### Added

- added Jindřich Šesták's Czech translation
- improved character editing to allow easy indenting and moving the cursor by
  whole words
- added Miś Uszatek's Polish translation
- improved auto-detection of utf_16 and utf_32
- added "New N-Way File Merge..." menu item
- added syntax highlighting for Erlang and OpenCL files

## 0.4.6 - 2011-11-02

### Added

- added support for Subversion 1.7
- added "Open Commit..." menu item
- "-c" option now works for all supported version control systems
- Git support distinguishes between staged and unstaged files
- added syntax highlighting for R files

### Fixed

- fixed a bug that caused the wrong revision to be shown when working on a
  branch in Mercurial

## 0.4.5 - 2011-07-13

### Added

- added syntax highlighting for JSON files
- added menu items and keyboard shortcuts for "First Tab" and "Last Tab"
- added "--line" command line option
- Diffuse now uses a patience diff-based algorithm to align lines
- added command line option to specify a label to display instead of the file name
- added preference to display the right margin
- added Cristian Marchi's Italian translation

### Changed

- state information is now stored in ~/.local/share/diffuse

### Fixed

- fixed a bug in CVS and Subversion support that prevented Diffuse from
  displaying some removed files
- fixed a bug that caused deleted files to be ignored when using the '-m' option
- fixed a bug that incorrectly encoded pasted text if utf_8 was not specified in
  the Region Settings preferences
- fixed a bug that could cause "Save As..." to fail with some user specified encodings

## 0.4.4 - 2010-10-21

### Added

- Git support now recognises conflicts when re-applying the stash
- search dialog is now automatically populated with the currently selected text
- added Oleg Pakhtusov's Russian translation
- added Kang Bundo's Korean translation
- pane headers tooltips
- Shift-ScrollWheel can now be used to scroll horizontally

### Fixed

- double clicking on text can now select full words with non-English characters
- fixed a bug that prevented opening files with non-ASCII characters in their path

## 0.4.3 - 2010-04-15

### Fixed

- fixed a bug that prevented the "-m" option from opening a 3-way merge for
  Subversion and Bazaar conflicts

## 0.4.2 - 2010-04-13

### Added

- support for detached Git repositories
- better removal of unnecessary spacer lines
- added support for horizontal mouse scrolling
- renamed some resources to more user friendly names
- RCS support
- added Henri Menke's Spanish translation
- "#!" interpreter lines are now used to select proper highlighting rules

### Changed

- syntax highlighting is now indicated by radio menu items

## 0.4.1 - 2009-10-12

### Added

- added Japanese translation
- added Liu Hao's simplified Chinese translation
- added a 'Dismiss All Edits' menu item
- localised manuals are now supported on Windows
- new command line option for specifying blank file comparison panes
- new preference to enable/disable line numbers
- added "Undo Close Tab" menu item
- added new menu items and buttons for copying lines between panes

### Changed

- personal configuration files are now stored in ~/.config/diffuse/ (the README
  file describes how to migrate old settings)
- Diffuse now quits if no viewers were created with the -m option
- replaced "Closing last tab quits Diffuse" preference with a "Warn me when
  closing a tab will quit Diffuse" preference
- MMB on a notebook tab now closes the tab
- RMB on a notebook tab creates a popup menu to set the current page
- changed the default hotkeys for merging to reflect the direction text "moves"

## 0.4.0 - 2009-08-17

### Added

- added format menu with new items for changing case, sorting, and manipulating
  white space
- optimised redraws when only the cursor position has changed
- input methods that use pre-editing can now be used when editing text
- dead keys can now be used when editing text
- updated Monotone support to use 'mtn automate inventory'
- Git support now handles files flagged as 'unmerged'
- added version control section to the manual

### Changed

- replaced 'Hide end of line characters' preference with 'Show white space characters'
- errors are now reported in a dialogue instead of printing to stderr

### Fixed

- graceful handling of non-zero exit codes from 'git status'
- minor bug fixes

## 0.3.4 - 2009-07-03

### Added

- syntax highlighting for .plist, GLSL, SConscript, and SConstruct files
- status bar now explains how to navigate between modes
- added labels to indicate syntax highlighting rules, encoding, and format
- Subversion 1.6 support
- added Henri Menke's German translation
- added '--examplesdir=' and '--mandir=' options to install.py
- renamed the '--python-interpreter=' installer option to '--pythonbin='

### Fixed

- minor bug fixes

## 0.3.3 - 2009-04-13

### Fixed

- fixed a bug handling the backspace key with the cursor in the first column

## 0.3.2 - 2009-04-13

### Added

- POSIX installer with `--destdir=` and `--files-only` options for packagers
- vi-like keybindings for line mode
- `-m` option to open modified files in separate tabs
- 'Merge From Left Then Right' and 'Merge From Right Then Left' menu items
- drag-n-drop support
- preferences for behaviour of tabs
- files with edits now tagged with '*'
- auto indent
- 'Open File In New Tab...' and 'Open Modified Files...' menu items
- 'Save All' menu item
- mac-style line ending support

### Changed

- new end of line display behaviour
- improved organisation of menu items
- errors are now reported on stderr

### Fixed

- button bar no longer grabs keyboard focus
- minor bug fixes

### Removed

- removed dependence on urllib module
- removed TODO list

## 0.3.1 - 2009-03-05

### Fixed

- fixed a typo that broke the 'Find...' dialogue

## 0.3.0 - 2009-03-03

### Added

- new Windows installer
- notification on focus change when files change on disk
- menu items for adjusting indentation
- syntax highlighting for Objective-C++
- `-c` option now works with CVS-style revision numbers
- window title now describes current tab
- search settings now persist across sessions

### Fixed

- minor bug fixes

## 0.2.15 - 2008-12-03

### Added

- smoother scrolling
- panes and tabs can now be manually re-organised
- preferences for tab key behaviour
- 'go to line' menu item
- '-c' option for viewing the changes of a particular commit
- home/end keys can now be used in line mode
- confirmation requested before overriding changed files
- position of window now saved
- syntax files for more file types
- reading /etc/diffuserc now optional when using a personal configuration file

### Fixed

- minor bug fixes

## 0.2.14 - 2008-10-20

### Added

- svk support
- syntax files for more file types
- DOS / Unix line endings now respected in edit operations
- improved difference map
- more robust launching of help browsers
- man page
- command line display options
- file revisions can now be specified in the open file dialogue

### Changed

- moved some resources to the preferences dialogue

### Fixed

- minor bug fixes

## 0.2.13 - 2008-05-16

### Added

- bazaar, darcs, and monotone support
- configurable key bindings
- persistent preference settings
- optimisations

### Fixed

- minor bug fixes

## 0.2.12 - 2008-05-06

### Added

- alternate codecs for reading and writing files
- more search options
- editor support for primary selection

### Fixed

- minor bug fixes

## 0.2.11 - 2008-04-27

### Added

- cvs, subversion, git, mercurial support
- python re-write
- syntax highlighting
- search and replace
- customisable through configuration files
- tabbed viewer panes

## 0.1.14 - 2006-01-28

### Added

- initial public release
