# Diffuse User's Manual

Graphical tool for merging and comparing text files

This manual describes version 0.4.8 of Diffuse.

**Table of Contents**

1. [Introduction](#introduction)
    - [About](#introduction-about)
    - [Licence](#introduction-licence)
    - [Command Line Usage](#introduction-usage)
    - [Help Options](#introduction-options-help)
        - [Configuration Options](#introduction-options-configuration)
        - [General Options](#introduction-options-general)
        - [Display Options](#introduction-options-display)
2. [File Comparison](#file-comparison)
    - [Comparison Summary](#file-comparison-summary)
    - [Selecting](#file-comparison-selecting)
    - [Matching Lines](#file-comparison-alignment)
    - [Editing](#file-comparison-editing)
    - [Merging](#file-comparison-merging)
3. [Version Control](#version-control)
    - [Viewing Uncommitted Modifications](#version-control-uncommitted-modifications)
    - [Specifying Revisions](#version-control-specifying-revisions)
4. [Resources](#resources)
    - [General](#resources-general)
    - [Key Bindings](#resources-keybindings)
        - [Menu Item Key Bindings](#resources-keybindings-menu)
        - [Line Editing Mode Key Bindings](#resources-keybindings-line_mode)
        - [Alignment Editing Mode Key Bindings](#resources-keybindings-align_mode)
        - [Character Editing Mode Key Bindings](#resources-keybindings-character_mode)
    - [Strings](#resources-strings)
        - [Used String Resources](#resources-strings-used)
    - [Colours](#resources-colours)
        - [Used Colour Resources](#resources-colours-used)
    - [Floating Point Values](#resources-floats)
        - [Used Floating Point Resources](#resources-floats-used)
    - [Syntax Highlighting](#resources-syntax-highlighting)
5. [Files](#files)

# Chapter 1. Introduction

**Table of Contents**

- [About](#introduction-about)
- [Licence](#introduction-licence)
- [Command Line Usage](#introduction-usage)
- [Help Options](#introduction-options-help)
    - [Configuration Options](#introduction-options-configuration)
    - [General Options](#introduction-options-general)
    - [Display Options](#introduction-options-display)

Diffuse is a graphical tool for merging and comparing text files. Diffuse is able to compare an arbitrary number of files side-by-side and gives users the ability to manually adjust line matching and directly edit files. Diffuse can also retrieve revisions of files from Bazaar, CVS, Darcs, Git, Mercurial, Monotone, RCS, Subversion, and SVK repositories for comparison and merging.

## About

Diffuse was written by Derrick Moser .

© 2006-2014 Derrick Moser. All Rights Reserved.

## Licence

Diffuse is free software; you may redistribute it and/or modify it under the terms of the _GNU General Public License_ as published by the Free Software Foundation; either version 2 of the licence, or (at your option) any later version.

Diffuse is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the _GNU General Public License_ for more details.

You should have received a copy of the _GNU General Public License_ along with Diffuse. You may also obtain a copy of the _GNU General Public License_ from the Free Software Foundation by visiting [their web site](http://www.fsf.org/) or by writing to

Free Software Foundation, Inc.  
          51 Franklin St, Fifth Floor,  
          Boston, MA 02110-1301  
          USA



## Command Line Usage

**`diffuse [ -h | -? | --help | -v | --version ]`**

Display information about Diffuse.

**` diffuse [ [ `_`option`_` ]... [ `_`file`_` ]... ]... `**

Compare and merge files.

### Help Options

If a help option is specified, it must be the only argument specified on the command line. Diffuse will immediately quit after displaying the help information.

**`-h`**, **`-?`**, **`--help`**

Display usage information.

**`-v`**, **`--version`**

Display version number and copyright information.

### Configuration Options

If a configuration option is specified, it must be the first argument specified on the command line.

**`--no-rcfile`**

Do not read any initialisation files.

**` --rcfile `_`file`_` `**

Only read initialisation commands from file _`file`_.

### General Options

**`-c`**, **`--commit`** _`rev`_

Open separate file comparison tabs for all files affected by commit _`rev`_ from the remaining paths specified in the command line arguments.

**`-D`**, **`--close-if-same`**

Close all tabs with no differences.

**`-e`**, **`--encoding`** _`codec`_

Use _`codec`_ to read and write files.

**`-L`**, **`--label`** _`label`_

Display _`label`_ instead of the file name.

**`-m`**, **`--modified`**

Open separate file comparison tabs for all modified files from the remaining paths specified in the command line arguments.

**`-r`**, **`--revision`** _`rev`_

Include revision _`rev`_ of the next file named in the command line arguments in a file comparison tab.

**`-s`**, **`--separate`**

Open all remaining files specified in the command line arguments in separate file comparison tabs.

**`-t`**, **`--tab`**

Start a new tab for any remaining files named in the command line arguments.

**` --line`** _`line`_ 

Start with line _`line`_ selected.

**`--null-file`**

Create a blank file comparison pane.

### Display Options

Display options specified in the command line arguments will override saved preference values.

**`-b`**, **`--ignore-space-change`**

Ignore changes to the amount of white space.

**`-B`**, **`--ignore-blank-lines`**

Ignore changes whose lines are all blank.

**`-E`**, **`--ignore-end-of-line`**

Ignore end of line differences.

**`-i`**, **`--ignore-case`**

Ignore case differences in file contents.

**`-w`**, **`--ignore-all-space`**

Ignore all white space.

# Chapter 2. File Comparison

**Table of Contents**

- [Comparison Summary](#file-comparison-summary)
- [Selecting](#file-comparison-selecting)
- [Matching Lines](#file-comparison-alignment)
- [Editing](#file-comparison-editing)
- [Merging](#file-comparison-merging)

Use the File → New 2-Way File Merge, File → New 3-Way File Merge, and File → New N-Way File Merge menu items to create additional tabs for comparing text files. File names and revisions can be specified either in the command line arguments used to invoke Diffuse or in fields on the Open File dialogue.

Diffuse displays files side-by-side inserting gaps to align similar lines of text. Differences are highlighted with a different background colour.

## Comparison Summary

A summary of the compared files is located in the far right margin. The summary illustrates where gaps have been inserted to align matching lines of text and highlights differences using colour. Manual edits are also highlighted in green. A blue cursor identifies the region currently being viewed. The viewed region can be changed by clicking anywhere on the summary.

## Selecting

Lines of text can be selected using the mouse pointer or keyboard. Select lines of text with the mouse pointer by clicking on a line. Click and drag to select multiple lines. Holding down the shift key when clicking will extend the current selection. Select lines using the keyboard by pressing the page up/down or arrow keys. Extend the current selection by holding down the shift key and pressing the page up/down or arrow keys. Move the selection to an adjacent file using the left and right arrow keys.

## Matching Lines

The mouse pointer or keyboard can be used to manually align lines of text with adjacent files. To aligning lines of text using the mouse pointer, select a line of text with the left mouse button, right click on a line of text from an adjacent file, and choose Align with Selection. To align lines of text using the keyboard, move the selection with the cursor keys, press the space bar to pick the current line of text, move the selection with the cursor keys to a line of text in an adjacent file, and press the space bar to pick the target line of text. Pressing the **Escape** key will cancel the operation.

Use the Isolate menu item to prevent the selected lines from being matched with any lines from the adjacent files.

## Editing

Press the **Enter** key or double-click on a text area to enter text editing mode. The cursor will change to indicate text editing mode and the status bar at the bottom of the window will display the cursor's column position.

In text editing mode, text can be selected with the mouse pointer by click and dragging. The current selection can be extended by holding down the shift key and moving the cursor by clicking with the mouse pointer or pressing any of the arrow, home, end or page up/down keys. Individual words can be selected by double-clicking on them with the mouse pointer. Whole lines can be selected by triple-clicking on them with the mouse pointer.

Modify text by typing on the keyword. Modified lines will be highlighted in green. Use the Undo and Redo menu items to undo and redo the previously preformed operations.

Press the **Escape** key or click on another file's text area using the left mouse button to leave editing mode.

## Merging

Use the difference buttons or menu items to navigate between blocks of differences within a file. When navigating, Diffuse will move the selection to the next continuous set of lines with differences or edits.

Use the merge buttons or menu items to copy blocks of text into the selected range of lines. The Undo and Redo menu items can be used to undo and redo the previously preformed operations. All changes to a set of lines can be reverted using the Clear Edits menu item regardless of the order the edits were performed.

# Chapter 3. Version Control

Diffuse can retrieve file revisions from several version control systems via their command line interface. The Microsoft Windows build of Diffuse is able to use both the Cygwin and native versions of the supported version control systems. When using Diffuse with Cygwin, ensure Diffuse's Cygwin preferences correctly describe your system. If the Update paths for Cygwin preference exists for a version control system, it must be enabled to use the Cygwin version.

Version control systems are sensitive to the system path and other environment variable settings. The Launch from a Bash login shell preference may be used to easily set the environment for Cygwin version control systems.

## Viewing Uncommitted Modifications

The **`-m`** option will cause Diffuse to open comparison tabs for each file the version control system indicates has uncommitted modifications. This is convenient for reviewing all changes before committing or resolving a merge conflict. If no paths are specified the current working directory will be used. For example, view all of your uncommitted modifications with this command line:

    diffuse -m

The default revision of a file will be used for comparison if only one file is specified. For example, this will display a 2-way merge between the default revision of `foo.C` and the local `foo.C` file:

    diffuse foo.C

## Specifying Revisions

The **`-r`** option may also be used to explicitly specify a particular file revision. Any revision specifier understood by the version control system may be used. The local file will be used for comparison if only one file revision is specified. For example, this will display a 2-way merge between revision 123 of `foo.C` and the local `foo.C` file:

    diffuse -r 123 foo.C

Multiple file revisions can be compared by specifying multiple **`-r`** options. For example, this will display a 2-way merge between revision 123 of `foo.C` and revision 321 of `foo.C`:

    diffuse -r 123 -r 321 foo.C

Local files can be mixed with files from the version control system. For example, this will display a 3-way merge between revision MERGE_HEAD of `foo.C`, the local `foo.C` file, and revision HEAD of `foo.C`:

    diffuse -r MERGE_HEAD foo.C foo.C -r HEAD foo.C

For the **`-c`** option may be used to easily specify a pair of sequential revisions. For example, this will display a 2-way merge between revision 1.2.2 of `foo.C` and revision 1.2.3 of `foo.C`:

    diffuse -c 1.2.3 foo.C

Diffuse does not limit the number of panes that can be used for comparing files. The inputs to a Git octopus merge could be viewed with a command line like this:
  
    diffuse -r HEAD^1 -r HEAD^2 -r HEAD^3 -r HEAD^4 -r HEAD^5 foo.C

# Chapter 4. Resources

**Table of Contents**
- [General](#resources-general)
- [Key Bindings](#resources-keybindings)
    - [Menu Item Key Bindings](#resources-keybindings-menu)
    - [Line Editing Mode Key Bindings](#resources-keybindings-line_mode)
    - [Alignment Editing Mode Key Bindings](#resources-keybindings-align_mode)
    - [Character Editing Mode Key Bindings](#resources-keybindings-character_mode)
- [Strings](#resources-strings)
    - [Used String Resources](#resources-strings-used)
- [Colours](#resources-colours)
    - [Used Colour Resources](#resources-colours-used)
- [Floating Point Values](#resources-floats)
    - [Used Floating Point Resources](#resources-floats-used)
- [Syntax Highlighting](#resources-syntax-highlighting)

Resources can be used to customise several aspects of Diffuse's appearance and behaviour such as changing the colours used in the user interface, customising the keyboard shortcuts, adding or replacing syntax highlighting rules, or changing the mapping from file extensions to syntax highlighting rules.

When Diffuse is started, it will read commands from the system wide initialisation file `/etc/diffuserc` (`%INSTALL_DIR%\diffuserc` on Microsoft Windows) and then the personal initialisation file `~/.config/diffuse/diffuserc` (`%HOME%\.config\diffuse\diffuserc` on Microsoft Windows). This behaviour can be changed with the **`--no-rcfile`** and **`--rcfile`** configuration options. A Bourne shell-like lexical analyser is used to parse initialisation commands. Comments and special characters can be embedded using the same style of escaping used in Bourne shell scripts.

## General

**` import `_`file`_` `**

Processes initialisation commands from _`file`_. Initialisation files will only be processed once.

## Key Bindings

**` keybinding `_`context`_` `_`action`_` `_`key_combination`_` `**

Binds a key combination to _`action`_ when used in _`context`_. Specify **Shift** and **Control** modifiers by prepending **`Shift+`** and **`Ctrl+`** to _`key_combination`_ respectively. Keys normally modified by the **Shift** key should be specified using their modified value if _`key_combination`_ involves the **Shift** key. For example, **`Ctrl+g`** and **`Shift+Ctrl+G`**. Remove bindings for _`key_combination`_ by specifying **`None`** for the _`action`_.

### Menu Item Key Bindings

Use **`menu`** for the _`context`_ to define key bindings for menu items. The following values are valid for _`action`_:

**`open_file`**

File → Open File... menu item

Default: `Ctrl+o`

**`open_file_in_new_tab`**

File → Open File In New Tab... menu item

Default: `Ctrl+t`

**`open_modified_files`**

File → Open Modified Files... menu item

Default: `Shift+Ctrl+O`

**`open_commit`**

File → Open Commit... menu item

Default: `Shift+Ctrl+T`

**`reload_file`**

File → Reload File menu item

Default: `Shift+Ctrl+R`

**`save_file`**

File → Save File menu item

Default: `Ctrl+s`

**`save_file_as`**

File → Save File As... menu item

Default: `Shift+Ctrl+A`

**`save_all`**

File → Save All menu item

Default: `Shift+Ctrl+S`

**`new_2_way_file_merge`**

File → New 2-Way File Merge menu item

Default: `Ctrl+2`

**`new_3_way_file_merge`**

File → New 3-Way File Merge menu item

Default: `Ctrl+3`

**`new_n_way_file_merge`**

File → New N-Way File Merge menu item

Default: `Ctrl+4`

**`close_tab`**

File → Close Tab menu item

Default: `Ctrl+w`

**`undo_close_tab`**

File → Undo Close Tab menu item

Default: `Shift+Ctrl+w`

**`quit`**

File → Quit menu item

Default: `Ctrl+q`

**`undo`**

Edit → Undo menu item

Default: `Ctrl+z`

**`redo`**

Edit → Redo menu item

Default: `Shift+Ctrl+Z`

**`cut`**

Edit → Cut menu item

Default: `Ctrl+x`

**`copy`**

Edit → Copy menu item

Default: `Ctrl+c`

**`paste`**

Edit → Paste menu item

Default: `Ctrl+v`

**`select_all`**

Edit → Select All menu item

Default: `Ctrl+a`

**`clear_edits`**

Edit → Clear Edits menu item

Default: `Ctrl+r`

**`dismiss_all_edits`**

Edit → Dismiss All Edits menu item

Default: `Ctrl+d`

**`find`**

Edit → Find... menu item

Default: `Ctrl+f`

**`find_next`**

Edit → Find Next menu item

Default: `Ctrl+g`

**`find_previous`**

Edit → Find Previous menu item

Default: `Shift+Ctrl+G`

**`go_to_line`**

Edit → Go To Line... menu item

Default: `Shift+Ctrl+L`

**`preferences`**

Edit → Preferences menu item

Default: None

**`no_syntax_highlighting`**

View → Syntax Highlighting → None menu item

Default: None

**` syntax_highlighting_`**_`syntax`_

View → Syntax Highlighting → _`syntax`_ menu item

Default: None

**`realign_all`**

View → Realign All menu item

Default: `Ctrl+l`

**`isolate`**

View → Isolate menu item

Default: `Ctrl+i`

**`first_difference`**

View → First Difference menu item

Default: `Shift+Ctrl+Up`

**`previous_difference`**

View → Previous Difference menu item

Default: `Ctrl+Up`

**`next_difference`**

View → Next Difference menu item

Default: `Ctrl+Down`

**`last_difference`**

View → Last Difference menu item

Default: `Shift+Ctrl+Down`

**`first_tab`**

View → First Tab menu item

Default: `Shift+Ctrl+Page_Up`

**`previous_tab`**

View → Previous Tab menu item

Default: `Ctrl+Page_Up`

**`next_tab`**

View → Next Tab menu item

Default: `Ctrl+Page_Down`

**`last_tab`**

View → Last Tab menu item

Default: `Shift+Ctrl+Page_Down`

**`shift_pane_right`**

View → Shift Pane Right menu item

Default: `Shift+Ctrl+parenleft`

**`shift_pane_left`**

View → Shift Pane Left menu item

Default: `Shift+Ctrl+parenright`

**`convert_to_upper_case`**

Format → Convert To Upper Case menu item

Default: `Ctrl+u`

**`convert_to_lower_case`**

Format → Convert To Lower Case menu item

Default: `Shift+Ctrl+U`

**`sort_lines_in_ascending_order`**

Format → Sort Lines In Ascending Order menu item

Default: `Ctrl+y`

**`sort_lines_in_descending_order`**

Format → Sort Lines In Descending Order menu item

Default: `Shift+Ctrl+Y`

**`remove_trailing_white_space`**

Format → Remove Trailing White Space menu item

Default: `Ctrl+k`

**`convert_tabs_to_spaces`**

Format → Convert Tabs To Spaces menu item

Default: `Ctrl+b`

**`convert_leading_spaces_to_tabs`**

Format → Convert Leading Spaces To Tabs menu item

Default: `Shift+Ctrl+B`

**`increase_indenting`**

Format → Increase Indenting menu item

Default: `Shift+Ctrl+greater`

**`decrease_indenting`**

Format → Decrease Indenting menu item

Default: `Shift+Ctrl+less`

**`convert_to_dos`**

Format → Convert To DOS Format menu item

Default: `Shift+Ctrl+E`

**`convert_to_mac`**

Format → Convert To Mac Format menu item

Default: `Shift+Ctrl+C`

**`convert_to_unix`**

Format → Convert To Unix Format menu item

Default: `Ctrl+e`

**`copy_selection_right`**

Merge → Copy Selection Right menu item

Default: `Shift+Ctrl+Right`

**`copy_selection_left`**

Merge → Copy Selection Left menu item

Default: `Shift+Ctrl+Left`

**`copy_left_into_selection`**

Merge → Copy Left Into Selection menu item

Default: `Ctrl+Right`

**`copy_right_into_selection`**

Merge → Copy Right Into Selection menu item

Default: `Ctrl+Left`

**`merge_from_left_then_right`**

Merge → Merge From Left Then Right menu item

Default: `Ctrl+m`

**`merge_from_right_then_left`**

Merge → Merge From Right Then Left menu item

Default: `Shift+Ctrl+M`

**`help_contents`**

Help → Help Contents menu item

Default: `F1`

**`about`**

Help → About menu item

Default: None

### Line Editing Mode Key Bindings

Use **`line_mode`** for the _`context`_ to define key bindings for line editing mode. The following values are valid for _`action`_:

**`enter_align_mode`**

enter alignment editing mode

Default: `space`

**`enter_character_mode`**

enter character editing mode

Defaults: `Return`, `KP_Enter`

**`first_line`**

move cursor to the first line

Defaults: `Home`, `g`

**`extend_first_line`**

move cursor to the first line, extending the selection

Default: `Shift+Home`

**`last_line`**

move cursor to the last line

Defaults: `End`, `Shift+G`

**`extend_last_line`**

move cursor to the last line, extending the selection

Default: `Shift+End`

**`up`**

move cursor up one line

Defaults: `Up`, `k`

**`extend_up`**

move cursor up one line, extending the selection

Defaults: `Shift+Up`, `Shift+K`

**`down`**

move cursor down one line

Defaults: `Down`, `j`

**`extend_down`**

move cursor down one line, extending the selection

Defaults: `Shift+Down`, `Shift+J`

**`left`**

move cursor left one file

Defaults: `Left`, `h`

**`extend_left`**

move cursor left one file, extending the selection

Default: `Shift+Left`

**`right`**

move cursor right one file

Defaults: `Right`, `l`

**`extend_right`**

move cursor right one file, extending the selection

Default: `Shift+Right`

**`page_up`**

move cursor up one page

Defaults: `Page_Up`, `Ctrl+u`

**`extend_page_up`**

move cursor up one page, extending the selection

Defaults: `Shift+Page_Up`, `Shift+Ctrl+u`

**`page_down`**

move cursor down one page

Defaults: `Page_Down`, `Ctrl+d`

**`extend_page_down`**

move cursor down one page, extending the selection

Defaults: `Shift+Page_Down`, `Shift+Ctrl+d`

**`delete_text`**

delete the selected text

Defaults: `BackSpace`, `Delete`, `x`

**`first_difference`**

select the first difference

Defaults: `Ctrl+Home`, `Shift+P`

**`previous_difference`**

select the previous difference

Default: `p`

**`next_difference`**

select the next difference

Default: `n`

**`last_difference`**

select the last difference

Defaults: `Ctrl+End`, `Shift+N`

**`clear_edits`**

clear all edits from the selected lines

Default: `r`

**`copy_selection_left`**

copy lines from the selection into the file on the left

Default: None

**`copy_selection_right`**

copy lines from the selection into the file on the right

Default: None

**`copy_left_into_selection`**

copy lines from the file on the left into the selection

Default: `Shift+L`

**`copy_right_into_selection`**

copy lines from the file on the right into the selection

Default: `Shift+H`

**`merge_from_left_then_right`**

merge lines from file on the left then file on the right

Default: `m`

**`merge_from_right_then_left`**

merge lines from file on the right then file on the left

Default: `Shift+M`

**`isolate`**

isolate the selected lines

Default: `i`

### Alignment Editing Mode Key Bindings

Use **`align_mode`** for the _`context`_ to define key bindings for alignment editing mode. The following values are valid for _`action`_:

**`enter_line_mode`**

enter line editing mode

Default: `Escape`

**`enter_character_mode`**

enter character editing mode

Defaults: `Return`, `KP_Enter`

**`first_line`**

move cursor to the first line

Default: `g`

**`last_line`**

move cursor to the last line

Default: `Shift+G`

**`up`**

move cursor up one line

Defaults: `Up`, `k`

**`down`**

move cursor down one line

Defaults: `Down`, `j`

**`left`**

move cursor left one file

Defaults: `Left`, `h`

**`right`**

move cursor right one file

Defaults: `Right`, `l`

**`page_up`**

move cursor up one page

Defaults: `Page_Up`, `Ctrl+u`

**`page_down`**

move cursor down one page

Defaults: `Page_Down`, `Ctrl+d`

**`align`**

align the selected line to the cursor position

Default: `space`

### Character Editing Mode Key Bindings

Use **`character_mode`** for the _`context`_ to define key bindings for character editing mode. The following values are valid for _`action`_:

**`enter_line_mode`**

enter line editing mode

Default: `Escape`

## Strings

**` string `**_`name value`_ 

Declares a string resource called _`name`_ with value _`value`_.

### Used String Resources

The following string resources are used by Diffuse:

**`difference_colours`**

a list of colour resources used to indicate differences

Default: `difference_1 difference_2 difference_3`

## Colours

**` [ colour | color ] `**_`name red green blue`_ 

Declares a colour resource called _`name`_. Individual colour components should be expressed as a value between 0 and 1.

### Used Colour Resources

The following colour resources are used by Diffuse:

**`alignment`**

colour used to indicate a line picked for manual alignment

Default: `1 1 0`

**`character_selection`**

colour used to indicate selected characters

Default: `0.7 0.7 1`

**`cursor`**

colour used for the cursor

Default: `0 0 0`

**`difference_1`**

colour used to identify differences between the first pair of files

Default: `1 0.625 0.625`

**`difference_2`**

colour used to identify differences between the second pair of files

Default: `0.85 0.625 0.775`

**`difference_3`**

colour used to identify differences between the third pair of files

Default: `0.85 0.775 0.625`

**`edited`**

colour used to indicate edited lines

Default: `0.5 1 0.5`

**`hatch`**

colour used for indicating alignment gaps

Default: `0.8 0.8 0.8`

**`line_number`**

colour used for line numbers

Default: `0 0 0`

**`line_number_background`**

background colour for the line number area

Default: `0.75 0.75 0.75`

**`line_selection`**

colour used to indicate selected lines

Default: `0.7 0.7 1`

**`map_background`**

background colour for the map area

Default: `0.6 0.6 0.6`

**`margin`**

colour used to indicate the right margin

Default: `0.8 0.8 0.8`

**`preedit`**

pre-edit text colour

Default: `0 0 0`

**`text`**

regular text colour

Default: `0 0 0`

**`text_background`**

background colour for the text area

Default: `1 1 1`

## Floating Point Values

**` float `**_`name value`_ 

Declares a floating point resource called _`name`_ with value _`value`_.

### Used Floating Point Resources

The following floating point resources are used by Diffuse:

**`alignment_opacity`**

opacity used when compositing the manual alignment colour

Defaults: `1`

**`character_difference_opacity`**

opacity used when compositing character difference colours

Defaults: `0.4`

**`character_selection_opacity`**

opacity used when compositing the character selection colour

Defaults: `0.4`

**`edited_opacity`**

opacity used when compositing the edited line colour

Defaults: `0.4`

**`line_difference_alpha`**

alpha value used when compositing line difference colours

Defaults: `0.3`

**`line_selection_opacity`**

opacity used when compositing the line selection colour

Defaults: `0.4`

## Syntax Highlighting

**` syntax `_`name`_` [`_`initial_state default_tag`_`] `**

Declares a new syntax style called _`name`_. Syntax highlighting uses a simple state machine that transitions between states when certain patterns are matched. The initial state for the state machine will be _`initial_state`_. All characters not matched by a pattern will be tagged as _`default_tag`_ for highlighting. The syntax style called _`name`_ can be removed by omitting _`initial_state`_ and _`default_tag`_.

**` syntax_files `_`name`_` [`_`pattern`_`] `**

Specifies that files with a name matching _`pattern`_ should be highlighted using the syntax style called _`name`_. Patterns used to match files for use with the syntax style called _`name`_ can be removed by omitting _`pattern`_.

**` syntax_magic `_`name`_` [`_`pattern`_` [ignorecase]] `**

Specifies that files with a first line matching _`pattern`_ should be highlighted using the syntax style called _`name`_. Patterns used to match files for use with the syntax style called _`name`_ can be removed by omitting _`pattern`_.

**` syntax_pattern `_`name initial_state final_state tag pattern`_` [ignorecase] `**

Adds a pattern to the previously declared syntax style. Patterns are tried one at a time in the order they were declared until the first match is found. A pattern will only be used to match characters if the state machine is in the state _`initial_state`_. The state machine will transition to _`final_state`_ if the pattern defined by _`pattern`_ is matched. Case insensitive pattern matching will be used if **`ignorecase`** is specified. All characters matched by the pattern will be tagged as _`tag`_ for highlighting.

# Chapter 5. Files

The following files are used by Diffuse:

`/etc/diffuserc`

system wide initialisations (`%INSTALL_DIR%\diffuserc` on Microsoft Windows)

`/usr/share/diffuse/syntax/*.syntax`

syntax files for various languages (`%INSTALL_DIR%\syntax\*.syntax` on Microsoft Windows)

`~/.config/diffuse/diffuserc`

your initialisations (`%HOME%\.config\diffuse\diffuserc` on Microsoft Windows)

`~/.config/diffuse/prefs`

your saved preferences (`%HOME%\.config\diffuse\prefs` on Microsoft Windows)

`~/.local/share/diffuse/state`

data persistent across sessions (`%HOME%\.local\share\diffuse\state` on Microsoft Windows)

Copyright © 2006-2019 Derrick Moser, Henri Menke  
Copyright © 2015-2020 Romain "Creak" Failliot

