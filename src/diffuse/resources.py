# Diffuse: a graphical tool for merging and comparing text files.
#
# Copyright (C) 2019 Derrick Moser <derrick_moser@yahoo.com>
# Copyright (C) 2021 Romain Failliot <romain.failliot@foolstep.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

# This class to hold all customizable behavior not exposed in the preferences
# dialogue: hotkey assignment, colours, syntax highlighting, etc.
# Syntax highlighting is implemented in supporting '*.syntax' files normally
# read from the system wide initialization file '/etc/diffuserc'.
# The personal initialization file '~/diffuse/diffuserc' can be used to change
# default behavior.

import glob
import os
import platform
import re
import shlex

from gettext import gettext as _
from typing import Dict, Final, List, Optional, Pattern, Set, Tuple

from diffuse import utils

import gi  # type: ignore
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk  # type: ignore # noqa: E402


class Resources:
    def __init__(self):
        # default keybindings
        defaultModKey = 'Cmd+' if platform.system() == 'Darwin' else 'Ctrl+'
        self.keybindings = {}
        self.keybindings_lookup = {}
        self.setKeyBinding('menu', 'open-file', defaultModKey + 'o')
        self.setKeyBinding('menu', 'open-file-in-new-tab', defaultModKey + 't')
        self.setKeyBinding('menu', 'open-modified-files', 'Shift+Ctrl+O')
        self.setKeyBinding('menu', 'open-commit', 'Shift+Ctrl+T')
        self.setKeyBinding('menu', 'reload-file', 'Shift+Ctrl+R')
        self.setKeyBinding('menu', 'save-file', defaultModKey + 's')
        self.setKeyBinding('menu', 'save-file-as', defaultModKey + 'Shift+A')
        self.setKeyBinding('menu', 'save-all', defaultModKey + 'Shift+S')
        self.setKeyBinding('menu', 'new-2-way-file-merge', 'Ctrl+2')
        self.setKeyBinding('menu', 'new-3-way-file-merge', 'Ctrl+3')
        self.setKeyBinding('menu', 'new-n-way-file-merge', 'Ctrl+4')
        self.setKeyBinding('menu', 'close-tab', defaultModKey + 'w')
        self.setKeyBinding('menu', 'undo-close-tab', defaultModKey + 'Shift+W')
        self.setKeyBinding('menu', 'quit', defaultModKey + 'q')
        self.setKeyBinding('menu', 'undo', defaultModKey + 'z')
        self.setKeyBinding('menu', 'redo', defaultModKey + 'Shift+Z')
        self.setKeyBinding('menu', 'cut', defaultModKey + 'x')
        self.setKeyBinding('menu', 'copy', defaultModKey + 'c')
        self.setKeyBinding('menu', 'paste', defaultModKey + 'v')
        self.setKeyBinding('menu', 'select-all', defaultModKey + 'a')
        self.setKeyBinding('menu', 'clear-edits', defaultModKey + 'r')
        self.setKeyBinding('menu', 'dismiss-all-edits', defaultModKey + 'd')
        self.setKeyBinding('menu', 'find', defaultModKey + 'f')
        self.setKeyBinding('menu', 'find-next', defaultModKey + 'g')
        self.setKeyBinding('menu', 'find-previous', defaultModKey + 'Shift+G')
        self.setKeyBinding('menu', 'go-to-line', defaultModKey + 'Shift+l')
        self.setKeyBinding('menu', 'realign-all', defaultModKey + 'l')
        self.setKeyBinding('menu', 'isolate', defaultModKey + 'i')
        self.setKeyBinding('menu', 'first-difference', defaultModKey + 'Shift+Up')
        self.setKeyBinding('menu', 'previous-difference', defaultModKey + 'Up')
        self.setKeyBinding('menu', 'next-difference', defaultModKey + 'Down')
        self.setKeyBinding('menu', 'last-difference', defaultModKey + 'Shift+Down')
        self.setKeyBinding('menu', 'first-tab', 'Shift+Ctrl+Page_Up')
        self.setKeyBinding('menu', 'previous-tab', 'Ctrl+Page_Up')
        self.setKeyBinding('menu', 'next-tab', 'Ctrl+Page_Down')
        self.setKeyBinding('menu', 'last-tab', 'Shift+Ctrl+Page_Down')
        self.setKeyBinding('menu', 'shift-pane-right', 'Shift+Ctrl+parenright')
        self.setKeyBinding('menu', 'shift-pane-left', 'Shift+Ctrl+parenleft')
        self.setKeyBinding('menu', 'convert-to-upper-case', defaultModKey + 'u')
        self.setKeyBinding('menu', 'convert-to-lower-case', defaultModKey + 'Shift+U')
        self.setKeyBinding('menu', 'sort-lines-in-ascending-order', defaultModKey + 'y')
        self.setKeyBinding('menu', 'sort-lines-in-descending-order', defaultModKey + 'Shift+Y')
        self.setKeyBinding('menu', 'remove-trailing-white-space', defaultModKey + 'k')
        self.setKeyBinding('menu', 'convert-tabs-to-spaces', defaultModKey + 'b')
        self.setKeyBinding('menu', 'convert-leading-spaces-to-tabs', 'Shift+Ctrl+B')
        self.setKeyBinding('menu', 'increase-indenting', defaultModKey + 'Shift+greater')
        self.setKeyBinding('menu', 'decrease-indenting', defaultModKey + 'Shift+less')
        self.setKeyBinding('menu', 'convert-to-dos', defaultModKey + 'Shift+E')
        self.setKeyBinding('menu', 'convert-to-mac', defaultModKey + 'Shift+C')
        self.setKeyBinding('menu', 'convert-to-unix', defaultModKey + 'e')
        self.setKeyBinding('menu', 'copy-selection-right', defaultModKey + 'Shift+Right')
        self.setKeyBinding('menu', 'copy-selection-left', defaultModKey + 'Shift+Left')
        self.setKeyBinding('menu', 'copy-left-into-selection', defaultModKey + 'Right')
        self.setKeyBinding('menu', 'copy-right-into-selection', defaultModKey + 'Left')
        self.setKeyBinding('menu', 'merge-from-left-then-right', defaultModKey + 'm')
        self.setKeyBinding('menu', 'merge-from-right-then-left', defaultModKey + 'Shift+M')
        self.setKeyBinding('menu', 'help-contents', 'F1')
        self.setKeyBinding('line_mode', 'enter-align-mode', 'space')
        self.setKeyBinding('line_mode', 'enter-character-mode', 'Return')
        self.setKeyBinding('line_mode', 'enter-character-mode', 'KP_Enter')
        self.setKeyBinding('line_mode', 'first-line', 'Home')
        self.setKeyBinding('line_mode', 'first-line', 'g')
        self.setKeyBinding('line_mode', 'extend-first-line', 'Shift+Home')
        self.setKeyBinding('line_mode', 'last-line', 'End')
        self.setKeyBinding('line_mode', 'last-line', 'Shift+G')
        self.setKeyBinding('line_mode', 'extend-last-line', 'Shift+End')
        self.setKeyBinding('line_mode', 'up', 'Up')
        self.setKeyBinding('line_mode', 'up', 'k')
        self.setKeyBinding('line_mode', 'extend-up', 'Shift+Up')
        self.setKeyBinding('line_mode', 'extend-up', 'Shift+K')
        self.setKeyBinding('line_mode', 'down', 'Down')
        self.setKeyBinding('line_mode', 'down', 'j')
        self.setKeyBinding('line_mode', 'extend-down', 'Shift+Down')
        self.setKeyBinding('line_mode', 'extend-down', 'Shift+J')
        self.setKeyBinding('line_mode', 'left', 'Left')
        self.setKeyBinding('line_mode', 'left', 'h')
        self.setKeyBinding('line_mode', 'extend-left', 'Shift+Left')
        self.setKeyBinding('line_mode', 'right', 'Right')
        self.setKeyBinding('line_mode', 'right', 'l')
        self.setKeyBinding('line_mode', 'extend-right', 'Shift+Right')
        self.setKeyBinding('line_mode', 'page-up', 'Page_Up')
        self.setKeyBinding('line_mode', 'page-up', defaultModKey + 'u')
        self.setKeyBinding('line_mode', 'extend-page-up', 'Shift+Page_Up')
        self.setKeyBinding('line_mode', 'extend-page-up', defaultModKey + 'Shift+U')
        self.setKeyBinding('line_mode', 'page-down', 'Page_Down')
        self.setKeyBinding('line_mode', 'page-down', defaultModKey + 'd')
        self.setKeyBinding('line_mode', 'extend-page-down', 'Shift+Page_Down')
        self.setKeyBinding('line_mode', 'extend-page-down', defaultModKey + 'Shift+D')
        self.setKeyBinding('line_mode', 'delete-text', 'BackSpace')
        self.setKeyBinding('line_mode', 'delete-text', 'Delete')
        self.setKeyBinding('line_mode', 'delete-text', 'x')
        self.setKeyBinding('line_mode', 'clear-edits', 'r')
        self.setKeyBinding('line_mode', 'isolate', 'i')
        self.setKeyBinding('line_mode', 'first-difference', 'Ctrl+Home')
        self.setKeyBinding('line_mode', 'first-difference', 'Shift+P')
        self.setKeyBinding('line_mode', 'previous-difference', 'p')
        self.setKeyBinding('line_mode', 'next-difference', 'n')
        self.setKeyBinding('line_mode', 'last-difference', 'Ctrl+End')
        self.setKeyBinding('line_mode', 'last-difference', 'Shift+N')
        # self.setKeyBinding('line_mode', 'copy-selection-right', 'Shift+L')
        # self.setKeyBinding('line_mode', 'copy-selection-left', 'Shift+H')
        self.setKeyBinding('line_mode', 'copy-left-into-selection', 'Shift+L')
        self.setKeyBinding('line_mode', 'copy-right-into-selection', 'Shift+H')
        self.setKeyBinding('line_mode', 'merge-from-left-then-right', 'm')
        self.setKeyBinding('line_mode', 'merge-from-right-then-left', 'Shift+M')
        self.setKeyBinding('align_mode', 'enter-line-mode', 'Escape')
        self.setKeyBinding('align_mode', 'align', 'space')
        self.setKeyBinding('align_mode', 'enter-character-mode', 'Return')
        self.setKeyBinding('align_mode', 'enter-character-mode', 'KP_Enter')
        self.setKeyBinding('align_mode', 'first-line', 'g')
        self.setKeyBinding('align_mode', 'last-line', 'Shift+G')
        self.setKeyBinding('align_mode', 'up', 'Up')
        self.setKeyBinding('align_mode', 'up', 'k')
        self.setKeyBinding('align_mode', 'down', 'Down')
        self.setKeyBinding('align_mode', 'down', 'j')
        self.setKeyBinding('align_mode', 'left', 'Left')
        self.setKeyBinding('align_mode', 'left', 'h')
        self.setKeyBinding('align_mode', 'right', 'Right')
        self.setKeyBinding('align_mode', 'right', 'l')
        self.setKeyBinding('align_mode', 'page-up', 'Page_Up')
        self.setKeyBinding('align_mode', 'page-up', defaultModKey + 'u')
        self.setKeyBinding('align_mode', 'page-down', 'Page_Down')
        self.setKeyBinding('align_mode', 'page-down', defaultModKey + 'd')
        self.setKeyBinding('character_mode', 'enter-line-mode', 'Escape')

        # default colours
        self.colours: Dict[str, _Colour] = {
            'alignment': _Colour(1.0, 1.0, 0.0),
            'character_selection': _Colour(0.7, 0.7, 1.0),
            'cursor': _Colour(0.0, 0.0, 0.0),
            'difference_1': _Colour(1.0, 0.625, 0.625),
            'difference_2': _Colour(0.85, 0.625, 0.775),
            'difference_3': _Colour(0.85, 0.775, 0.625),
            'hatch': _Colour(0.8, 0.8, 0.8),
            'line_number': _Colour(0.0, 0.0, 0.0),
            'line_number_background': _Colour(0.75, 0.75, 0.75),
            'line_selection': _Colour(0.7, 0.7, 1.0),
            'map_background': _Colour(0.6, 0.6, 0.6),
            'margin': _Colour(0.8, 0.8, 0.8),
            'edited': _Colour(0.5, 1.0, 0.5),
            'preedit': _Colour(0.0, 0.0, 0.0),
            'text': _Colour(0.0, 0.0, 0.0),
            'text_background': _Colour(1.0, 1.0, 1.0)
        }

        # default floats
        self.floats: Dict[str, float] = {
            'alignment_opacity': 1.0,
            'character_difference_opacity': 0.4,
            'character_selection_opacity': 0.4,
            'edited_opacity': 0.4,
            'line_difference_opacity': 0.3,
            'line_selection_opacity': 0.4
        }

        # default options
        self.options: Dict[str, str] = {
            'log_print_output': 'False',
            'log_print_stack': 'False',
            'use_flatpak': 'False'
        }

        # default strings
        self.strings: Dict[str, str] = {}

        # syntax highlighting support
        self.syntaxes: Dict[str, _SyntaxParser] = {}
        self.syntax_file_patterns: Dict[str, Pattern] = {}
        self.syntax_magic_patterns: Dict[str, Pattern] = {}
        self.current_syntax: Optional[_SyntaxParser] = None

        # list of imported resources files (we only import each file once)
        self.resource_files: Set[str] = set()

        # special string resources
        self.setDifferenceColours('difference_1 difference_2 difference_3')

    # keyboard action processing
    def setKeyBinding(self, ctx: str, name: str, modifiers: str) -> None:
        action_tuple = (ctx, name)
        modifier_flags = Gdk.ModifierType(0)
        key = None
        for token in modifiers.split('+'):
            if token == 'Shift':
                modifier_flags |= Gdk.ModifierType.SHIFT_MASK
            elif token == 'Ctrl':
                modifier_flags |= Gdk.ModifierType.CONTROL_MASK
            elif token == 'Cmd':
                modifier_flags |= Gdk.ModifierType.META_MASK
            elif token == 'Alt':
                modifier_flags |= Gdk.ModifierType.MOD1_MASK
            elif len(token) == 0 or token[0] == '_':
                raise ValueError(_('The key binding "{key}" is invalid').format(key=modifiers))
            else:
                token = 'KEY_' + token
                if not hasattr(Gdk, token):
                    raise ValueError(_('The key binding "{key}" is invalid').format(key=modifiers))
                key = getattr(Gdk, token)
        if key is None:
            raise ValueError(_('The key binding "{key}" is invalid').format(key=modifiers))
        key_tuple = (ctx, (key, modifier_flags))

        # remove any existing binding
        if key_tuple in self.keybindings_lookup:
            self._removeKeyBinding(key_tuple)

        # ensure we have a set to hold this action
        if action_tuple not in self.keybindings:
            self.keybindings[action_tuple] = {}
        bindings = self.keybindings[action_tuple]

        # menu items can only have one binding
        if ctx == 'menu':
            for k in bindings.keys():
                self._removeKeyBinding(k)

        # add the binding
        bindings[key_tuple] = None
        self.keybindings_lookup[key_tuple] = action_tuple

    def _removeKeyBinding(self, key_tuple):
        action_tuple = self.keybindings_lookup[key_tuple]
        del self.keybindings_lookup[key_tuple]
        del self.keybindings[action_tuple][key_tuple]

    def getKeyBindings(self, ctx, name):
        try:
            return [t for _, t in self.keybindings[(ctx, name)].keys()]
        except KeyError:
            return []

    def getActionForKey(self, ctx, key, modifiers):
        try:
            return self.keybindings_lookup[(ctx, (key, modifiers))][1]
        except KeyError:
            return None

    # colours used for indicating differences
    def setDifferenceColours(self, s: str) -> None:
        colours = s.split()
        if len(colours) > 0:
            self.difference_colours = colours

    def getDifferenceColour(self, i):
        n = len(self.difference_colours)
        return self.getColour(self.difference_colours[(i + n - 1) % n])

    # colour resources
    def getColour(self, symbol):
        try:
            return self.colours[symbol]
        except KeyError:
            utils.logDebug(f'Warning: unknown colour "{symbol}"')
            self.colours[symbol] = v = _Colour(0.0, 0.0, 0.0)
            return v

    # float resources
    def getFloat(self, symbol):
        try:
            return self.floats[symbol]
        except KeyError:
            utils.logDebug(f'Warning: unknown float "{symbol}"')
            self.floats[symbol] = v = 0.5
            return v

    def getOption(self, option: str) -> str:
        '''Get the option value.'''
        try:
            return self.options[option]
        except KeyError:
            utils.logDebug(f'Warning: unknown option "{option}"')
            return ''

    def getOptionAsBool(self, option: str) -> bool:
        '''Get the option value, casted as a boolean.'''
        return bool(self.getOption(option).lower() in ['true', '1'])

    # string resources
    def getString(self, symbol: str) -> str:
        try:
            return self.strings[symbol]
        except KeyError:
            utils.logDebug(f'Warning: unknown string "{symbol}"')
            return ''

    # syntax highlighting
    def getSyntaxNames(self):
        return list(self.syntaxes.keys())

    def getSyntax(self, name):
        return self.syntaxes.get(name, None)

    def guessSyntaxForFile(self, name: str, ss: List[str]) -> Optional[str]:
        name = os.path.basename(name)
        for key, pattern in self.syntax_file_patterns.items():
            if pattern.search(name):
                return key
        # fallback to analysing the first line of the file
        if len(ss) > 0:
            s = ss[0]
            for key, pattern in self.syntax_magic_patterns.items():
                if pattern.search(s):
                    return key
        return None

    # parse resource files
    def parse(self, file_name: str) -> None:
        # only process files once
        if file_name in self.resource_files:
            return

        self.resource_files.add(file_name)
        with open(file_name, 'r', encoding='utf-8') as f:
            ss = utils.readconfiglines(f)

        # FIXME: improve validation
        for i, s in enumerate(ss):
            args = shlex.split(s, True)
            if len(args) == 0:
                continue

            try:
                # eg. add Python syntax highlighting:
                #    import /usr/share/diffuse/syntax/python.syntax
                if args[0] == 'import':
                    if len(args) != 2:
                        raise SyntaxError(_('Imports must have one argument'))
                    path = os.path.expanduser(args[1])
                    # relative paths are relative to the parsed file
                    path = os.path.join(utils.globEscape(os.path.dirname(file_name)), path)
                    paths = glob.glob(path)
                    if len(paths) == 0:
                        paths = [path]
                    for path in paths:
                        # convert to absolute path so the location of
                        # any processing errors are reported with
                        # normalized file names
                        self.parse(os.path.abspath(path))
                # eg. make Ctrl+o trigger the open_file menu item
                #    keybinding menu open_file Ctrl+o
                elif args[0] == 'keybinding':
                    if len(args) != 4:
                        raise SyntaxError(_('Key bindings must have three arguments'))
                    self.setKeyBinding(args[1], args[2], args[3])
                # eg. set the regular background colour to white
                #    colour text_background 1.0 1.0 1.0
                elif args[0] in ['colour', 'color']:
                    if len(args) != 5:
                        raise SyntaxError(_('Colors must have four arguments'))
                    self.colours[args[1]] = _Colour(float(args[2]), float(args[3]), float(args[4]))
                # eg. set opacity of the line_selection colour
                #    float line_selection_opacity 0.4
                elif args[0] == 'float':
                    if len(args) != 3:
                        raise SyntaxError(_('Floats must have two arguments'))
                    self.floats[args[1]] = float(args[2])
                # eg. enable option log_print_output
                #    option log_print_output true
                elif args[0] == 'option':
                    if len(args) != 3:
                        raise SyntaxError(_('Options must have two arguments'))
                    if args[1] not in self.options:
                        raise SyntaxError(
                            _('Option "{option}" is unknown').format(option=args[1])
                        )
                    self.options[args[1]] = args[2]
                # eg. set the help browser
                #    string help_browser gnome-help
                elif args[0] == 'string':
                    if len(args) != 3:
                        raise SyntaxError(_('Strings must have two arguments'))
                    self.strings[args[1]] = args[2]
                    if args[1] == 'difference_colours':
                        self.setDifferenceColours(args[2])
                # eg. start a syntax specification for Python
                #    syntax Python normal text
                # where 'normal' is the name of the default state and
                # 'text' is the classification of all characters not
                # explicitly matched by a syntax highlighting rule
                elif args[0] == 'syntax':
                    if len(args) != 3 and len(args) != 4:
                        raise SyntaxError(_('Syntaxes must have two or three arguments'))
                    key = args[1]
                    if len(args) == 2:
                        # remove file pattern for a syntax specification
                        try:
                            del self.syntax_file_patterns[key]
                        except KeyError:
                            pass
                        # remove magic pattern for a syntax specification
                        try:
                            del self.syntax_magic_patterns[key]
                        except KeyError:
                            pass
                        # remove a syntax specification
                        self.current_syntax = None
                        try:
                            del self.syntaxes[key]
                        except KeyError:
                            pass
                    else:
                        self.current_syntax = _SyntaxParser(args[2], args[3])
                        self.syntaxes[key] = self.current_syntax
                # eg. transition from state 'normal' to 'comment' when
                # the pattern '#' is matched and classify the matched
                # characters as 'python_comment'
                #    syntax_pattern normal comment python_comment '#'
                elif args[0] == 'syntax_pattern' and self.current_syntax is not None:
                    if len(args) < 5:
                        raise SyntaxError(_('Syntax patterns must have at least four arguments'))
                    flags = 0
                    for arg in args[5:]:
                        if arg == 'ignorecase':
                            flags |= re.IGNORECASE
                        else:
                            raise SyntaxError(_('Value "{value}" is unknown').format(value=arg))
                    self.current_syntax.addPattern(
                        args[1],
                        args[2],
                        args[3],
                        re.compile(args[4], flags))
                # eg. default to the Python syntax rules when viewing
                # a file ending with '.py' or '.pyw'
                #    syntax_files Python '\.pyw?$'
                elif args[0] == 'syntax_files':
                    if len(args) != 2 and len(args) != 3:
                        raise SyntaxError(_('Syntax files must have one or two arguments'))
                    key = args[1]
                    if len(args) == 2:
                        # remove file pattern for a syntax specification
                        try:
                            del self.syntax_file_patterns[key]
                        except KeyError:
                            pass
                    else:
                        flags = 0
                        if utils.isWindows():
                            flags |= re.IGNORECASE
                        self.syntax_file_patterns[key] = re.compile(args[2], flags)
                # eg. default to the Python syntax rules when viewing
                # a files starting with patterns like #!/usr/bin/python
                #    syntax_magic Python '^#!/usr/bin/python$'
                elif args[0] == 'syntax_magic':
                    if len(args) < 2:
                        raise SyntaxError(_('Syntax magics must have at least one argument'))
                    key = args[1]
                    if len(args) == 2:
                        # remove magic pattern for a syntax specification
                        try:
                            del self.syntax_magic_patterns[key]
                        except KeyError:
                            pass
                    else:
                        flags = 0
                        for arg in args[3:]:
                            if arg == 'ignorecase':
                                flags |= re.IGNORECASE
                            else:
                                raise SyntaxError(
                                    _('Value "{value}" is unknown').format(value=arg)
                                )
                        self.syntax_magic_patterns[key] = re.compile(args[2], flags)
                else:
                    raise SyntaxError(_('Keyword "{keyword}" is unknown').format(keyword=args[0]))
            except SyntaxError as e:
                error_msg = _('Syntax error at line {line} of {file}').format(
                    line=i + 1,
                    file=file_name
                )
                utils.logError(f'{error_msg}: {e.msg}')
            except ValueError:
                error_msg = _('Value error at line {line} of {file}').format(
                    line=i + 1,
                    file=file_name
                )
                utils.logError(error_msg)
            except re.error:
                error_msg = _('Regex error at line {line} of {file}.')
                utils.logError(error_msg.format(line=i + 1, file=file_name))
            except:  # noqa: E722
                error_msg = _('Unhandled error at line {line} of {file}.')
                utils.logError(error_msg.format(line=i + 1, file=file_name))


# colour resources
class _Colour:
    def __init__(self, r: float, g: float, b: float, a: float = 1.0):
        # the individual colour components as floats in the range [0, 1]
        self.red = r
        self.green = g
        self.blue = b
        self.alpha = a

    # multiply by scalar
    def __mul__(self, s):
        return _Colour(s * self.red, s * self.green, s * self.blue, s * self.alpha)

    # add colours
    def __add__(self, other):
        return _Colour(
            self.red + other.red,
            self.green + other.green,
            self.blue + other.blue,
            self.alpha + other.alpha)

    # over operator
    def over(self, other):
        return self + other * (1 - self.alpha)


# class to build and run a finite state machine for identifying syntax tokens
class _SyntaxParser:
    # create a new state machine that begins in initial_state and classifies
    # all characters not matched by the patterns as default_token_type
    def __init__(self, initial_state: str, default_token_type: str) -> None:
        # initial state for the state machine when parsing a new file
        self.initial_state = initial_state
        # default classification of characters that are not explicitly matched
        # by any state transition patterns
        self.default_token_type = default_token_type
        # mappings from a state to a list of (pattern, token_type, next_state)
        # tuples indicating the new state for the state machine when 'pattern'
        # is matched and how to classify the matched characters
        self.transitions_lookup: Dict[str, List[Tuple[Pattern, str, str]]] = {initial_state: []}

    # Adds a new edge to the finite state machine from prev_state to
    # next_state.  Characters will be identified as token_type when pattern is
    # matched.  Any newly referenced state will be added.  Patterns for edges
    # leaving a state will be tested in the order they were added to the finite
    # state machine.
    def addPattern(
            self,
            prev_state: str,
            next_state: str,
            token_type: str,
            pattern: Pattern) -> None:
        for state in prev_state, next_state:
            if state not in self.transitions_lookup:
                self.transitions_lookup[state] = []
        self.transitions_lookup[prev_state].append((pattern, token_type, next_state))

    # given a string and an initial state, identify the final state and tokens
    def parse(self, state_name, s):
        transitions, blocks, start = self.transitions_lookup[state_name], [], 0
        while start < len(s):
            for pattern, token_type, next_state in transitions:
                m = pattern.match(s, start)
                if m is not None:
                    end, state_name = m.span()[1], next_state
                    transitions = self.transitions_lookup[state_name]
                    break
            else:
                end, token_type = start + 1, self.default_token_type
            if len(blocks) > 0 and blocks[-1][2] == token_type:
                blocks[-1][1] = end
            else:
                blocks.append([start, end, token_type])
            start = end
        return state_name, blocks


theResources: Final = Resources()
