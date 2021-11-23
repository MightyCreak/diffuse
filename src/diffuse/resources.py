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

# This class to hold all customisable behaviour not exposed in the preferences
# dialogue: hotkey assignment, colours, syntax highlighting, etc.
# Syntax highlighting is implemented in supporting '*.syntax' files normally
# read from the system wide initialisation file '/etc/diffuserc'.
# The personal initialisation file '~/diffuse/diffuserc' can be used to change
# default behaviour.

import glob
import os
import re
import shlex

from diffuse import utils

import gi  # type: ignore
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk  # type: ignore # noqa: E402


class Resources:
    def __init__(self):
        # default keybindings
        self.keybindings = {}
        self.keybindings_lookup = {}
        set_binding = self.setKeyBinding
        set_binding('menu', 'open_file', 'Ctrl+o')
        set_binding('menu', 'open_file_in_new_tab', 'Ctrl+t')
        set_binding('menu', 'open_modified_files', 'Shift+Ctrl+O')
        set_binding('menu', 'open_commit', 'Shift+Ctrl+T')
        set_binding('menu', 'reload_file', 'Shift+Ctrl+R')
        set_binding('menu', 'save_file', 'Ctrl+s')
        set_binding('menu', 'save_file_as', 'Shift+Ctrl+A')
        set_binding('menu', 'save_all', 'Shift+Ctrl+S')
        set_binding('menu', 'new_2_way_file_merge', 'Ctrl+2')
        set_binding('menu', 'new_3_way_file_merge', 'Ctrl+3')
        set_binding('menu', 'new_n_way_file_merge', 'Ctrl+4')
        set_binding('menu', 'close_tab', 'Ctrl+w')
        set_binding('menu', 'undo_close_tab', 'Shift+Ctrl+W')
        set_binding('menu', 'quit', 'Ctrl+q')
        set_binding('menu', 'undo', 'Ctrl+z')
        set_binding('menu', 'redo', 'Shift+Ctrl+Z')
        set_binding('menu', 'cut', 'Ctrl+x')
        set_binding('menu', 'copy', 'Ctrl+c')
        set_binding('menu', 'paste', 'Ctrl+v')
        set_binding('menu', 'select_all', 'Ctrl+a')
        set_binding('menu', 'clear_edits', 'Ctrl+r')
        set_binding('menu', 'dismiss_all_edits', 'Ctrl+d')
        set_binding('menu', 'find', 'Ctrl+f')
        set_binding('menu', 'find_next', 'Ctrl+g')
        set_binding('menu', 'find_previous', 'Shift+Ctrl+G')
        set_binding('menu', 'go_to_line', 'Shift+Ctrl+L')
        set_binding('menu', 'realign_all', 'Ctrl+l')
        set_binding('menu', 'isolate', 'Ctrl+i')
        set_binding('menu', 'first_difference', 'Shift+Ctrl+Up')
        set_binding('menu', 'previous_difference', 'Ctrl+Up')
        set_binding('menu', 'next_difference', 'Ctrl+Down')
        set_binding('menu', 'last_difference', 'Shift+Ctrl+Down')
        set_binding('menu', 'first_tab', 'Shift+Ctrl+Page_Up')
        set_binding('menu', 'previous_tab', 'Ctrl+Page_Up')
        set_binding('menu', 'next_tab', 'Ctrl+Page_Down')
        set_binding('menu', 'last_tab', 'Shift+Ctrl+Page_Down')
        set_binding('menu', 'shift_pane_right', 'Shift+Ctrl+parenright')
        set_binding('menu', 'shift_pane_left', 'Shift+Ctrl+parenleft')
        set_binding('menu', 'convert_to_upper_case', 'Ctrl+u')
        set_binding('menu', 'convert_to_lower_case', 'Shift+Ctrl+U')
        set_binding('menu', 'sort_lines_in_ascending_order', 'Ctrl+y')
        set_binding('menu', 'sort_lines_in_descending_order', 'Shift+Ctrl+Y')
        set_binding('menu', 'remove_trailing_white_space', 'Ctrl+k')
        set_binding('menu', 'convert_tabs_to_spaces', 'Ctrl+b')
        set_binding('menu', 'convert_leading_spaces_to_tabs', 'Shift+Ctrl+B')
        set_binding('menu', 'increase_indenting', 'Shift+Ctrl+greater')
        set_binding('menu', 'decrease_indenting', 'Shift+Ctrl+less')
        set_binding('menu', 'convert_to_dos', 'Shift+Ctrl+E')
        set_binding('menu', 'convert_to_mac', 'Shift+Ctrl+C')
        set_binding('menu', 'convert_to_unix', 'Ctrl+e')
        set_binding('menu', 'copy_selection_right', 'Shift+Ctrl+Right')
        set_binding('menu', 'copy_selection_left', 'Shift+Ctrl+Left')
        set_binding('menu', 'copy_left_into_selection', 'Ctrl+Right')
        set_binding('menu', 'copy_right_into_selection', 'Ctrl+Left')
        set_binding('menu', 'merge_from_left_then_right', 'Ctrl+m')
        set_binding('menu', 'merge_from_right_then_left', 'Shift+Ctrl+M')
        set_binding('menu', 'help_contents', 'F1')
        set_binding('line_mode', 'enter_align_mode', 'space')
        set_binding('line_mode', 'enter_character_mode', 'Return')
        set_binding('line_mode', 'enter_character_mode', 'KP_Enter')
        set_binding('line_mode', 'first_line', 'Home')
        set_binding('line_mode', 'first_line', 'g')
        set_binding('line_mode', 'extend_first_line', 'Shift+Home')
        set_binding('line_mode', 'last_line', 'End')
        set_binding('line_mode', 'last_line', 'Shift+G')
        set_binding('line_mode', 'extend_last_line', 'Shift+End')
        set_binding('line_mode', 'up', 'Up')
        set_binding('line_mode', 'up', 'k')
        set_binding('line_mode', 'extend_up', 'Shift+Up')
        set_binding('line_mode', 'extend_up', 'Shift+K')
        set_binding('line_mode', 'down', 'Down')
        set_binding('line_mode', 'down', 'j')
        set_binding('line_mode', 'extend_down', 'Shift+Down')
        set_binding('line_mode', 'extend_down', 'Shift+J')
        set_binding('line_mode', 'left', 'Left')
        set_binding('line_mode', 'left', 'h')
        set_binding('line_mode', 'extend_left', 'Shift+Left')
        set_binding('line_mode', 'right', 'Right')
        set_binding('line_mode', 'right', 'l')
        set_binding('line_mode', 'extend_right', 'Shift+Right')
        set_binding('line_mode', 'page_up', 'Page_Up')
        set_binding('line_mode', 'page_up', 'Ctrl+u')
        set_binding('line_mode', 'extend_page_up', 'Shift+Page_Up')
        set_binding('line_mode', 'extend_page_up', 'Shift+Ctrl+U')
        set_binding('line_mode', 'page_down', 'Page_Down')
        set_binding('line_mode', 'page_down', 'Ctrl+d')
        set_binding('line_mode', 'extend_page_down', 'Shift+Page_Down')
        set_binding('line_mode', 'extend_page_down', 'Shift+Ctrl+D')
        set_binding('line_mode', 'delete_text', 'BackSpace')
        set_binding('line_mode', 'delete_text', 'Delete')
        set_binding('line_mode', 'delete_text', 'x')
        set_binding('line_mode', 'clear_edits', 'r')
        set_binding('line_mode', 'isolate', 'i')
        set_binding('line_mode', 'first_difference', 'Ctrl+Home')
        set_binding('line_mode', 'first_difference', 'Shift+P')
        set_binding('line_mode', 'previous_difference', 'p')
        set_binding('line_mode', 'next_difference', 'n')
        set_binding('line_mode', 'last_difference', 'Ctrl+End')
        set_binding('line_mode', 'last_difference', 'Shift+N')
        # set_binding('line_mode', 'copy_selection_right', 'Shift+L')
        # set_binding('line_mode', 'copy_selection_left', 'Shift+H')
        set_binding('line_mode', 'copy_left_into_selection', 'Shift+L')
        set_binding('line_mode', 'copy_right_into_selection', 'Shift+H')
        set_binding('line_mode', 'merge_from_left_then_right', 'm')
        set_binding('line_mode', 'merge_from_right_then_left', 'Shift+M')
        set_binding('align_mode', 'enter_line_mode', 'Escape')
        set_binding('align_mode', 'align', 'space')
        set_binding('align_mode', 'enter_character_mode', 'Return')
        set_binding('align_mode', 'enter_character_mode', 'KP_Enter')
        set_binding('align_mode', 'first_line', 'g')
        set_binding('align_mode', 'last_line', 'Shift+G')
        set_binding('align_mode', 'up', 'Up')
        set_binding('align_mode', 'up', 'k')
        set_binding('align_mode', 'down', 'Down')
        set_binding('align_mode', 'down', 'j')
        set_binding('align_mode', 'left', 'Left')
        set_binding('align_mode', 'left', 'h')
        set_binding('align_mode', 'right', 'Right')
        set_binding('align_mode', 'right', 'l')
        set_binding('align_mode', 'page_up', 'Page_Up')
        set_binding('align_mode', 'page_up', 'Ctrl+u')
        set_binding('align_mode', 'page_down', 'Page_Down')
        set_binding('align_mode', 'page_down', 'Ctrl+d')
        set_binding('character_mode', 'enter_line_mode', 'Escape')

        # default colours
        self.colours = {
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
        self.floats = {
            'alignment_opacity': 1.0,
            'character_difference_opacity': 0.4,
            'character_selection_opacity': 0.4,
            'edited_opacity': 0.4,
            'line_difference_opacity': 0.3,
            'line_selection_opacity': 0.4
        }

        # default strings
        self.strings = {}

        # syntax highlighting support
        self.syntaxes = {}
        self.syntax_file_patterns = {}
        self.syntax_magic_patterns = {}
        self.current_syntax = None

        # list of imported resources files (we only import each file once)
        self.resource_files = set()

        # special string resources
        self.setDifferenceColours('difference_1 difference_2 difference_3')

    # keyboard action processing
    def setKeyBinding(self, ctx, s, v):
        action_tuple = (ctx, s)
        modifiers = Gdk.ModifierType(0)
        key = None
        for token in v.split('+'):
            if token == 'Shift':
                modifiers |= Gdk.ModifierType.SHIFT_MASK
            elif token == 'Ctrl':
                modifiers |= Gdk.ModifierType.CONTROL_MASK
            elif token == 'Alt':
                modifiers |= Gdk.ModifierType.MOD1_MASK
            elif len(token) == 0 or token[0] == '_':
                raise ValueError()
            else:
                token = 'KEY_' + token
                if not hasattr(Gdk, token):
                    raise ValueError()
                key = getattr(Gdk, token)
        if key is None:
            raise ValueError()
        key_tuple = (ctx, (key, modifiers))

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

    def getActionForKey(self, ctx, key, modifiers):
        try:
            return self.keybindings_lookup[(ctx, (key, modifiers))][1]
        except KeyError:
            return None

    def getKeyBindings(self, ctx, s):
        try:
            return [t for c, t in self.keybindings[(ctx, s)].keys()]
        except KeyError:
            return []

    # colours used for indicating differences
    def setDifferenceColours(self, s):
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

    # string resources
    def getString(self, symbol):
        try:
            return self.strings[symbol]
        except KeyError:
            utils.logDebug(f'Warning: unknown string "{symbol}"')
            self.strings[symbol] = v = ''
            return v

    # syntax highlighting
    def getSyntaxNames(self):
        return list(self.syntaxes.keys())

    def getSyntax(self, name):
        return self.syntaxes.get(name, None)

    def guessSyntaxForFile(self, name, ss):
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
    def parse(self, file_name):
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
                if args[0] == 'import' and len(args) == 2:
                    path = os.path.expanduser(args[1])
                    # relative paths are relative to the parsed file
                    path = os.path.join(utils.globEscape(os.path.dirname(file_name)), path)
                    paths = glob.glob(path)
                    if len(paths) == 0:
                        paths = [path]
                    for path in paths:
                        # convert to absolute path so the location of
                        # any processing errors are reported with
                        # normalised file names
                        self.parse(os.path.abspath(path))
                # eg. make Ctrl+o trigger the open_file menu item
                #    keybinding menu open_file Ctrl+o
                elif args[0] == 'keybinding' and len(args) == 4:
                    self.setKeyBinding(args[1], args[2], args[3])
                # eg. set the regular background colour to white
                #    colour text_background 1.0 1.0 1.0
                elif args[0] in ['colour', 'color'] and len(args) == 5:
                    self.colours[args[1]] = _Colour(float(args[2]), float(args[3]), float(args[4]))
                # eg. set opacity of the line_selection colour
                #    float line_selection_opacity 0.4
                elif args[0] == 'float' and len(args) == 3:
                    self.floats[args[1]] = float(args[2])
                # eg. set the help browser
                #    string help_browser gnome-help
                elif args[0] == 'string' and len(args) == 3:
                    self.strings[args[1]] = args[2]
                    if args[1] == 'difference_colours':
                        self.setDifferenceColours(args[2])
                # eg. start a syntax specification for Python
                #    syntax Python normal text
                # where 'normal' is the name of the default state and
                # 'text' is the classification of all characters not
                # explicitly matched by a syntax highlighting rule
                elif args[0] == 'syntax' and (len(args) == 2 or len(args) == 4):
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
                elif (
                    args[0] == 'syntax_pattern' and
                    self.current_syntax is not None and
                    len(args) >= 5
                ):
                    flags = 0
                    for arg in args[5:]:
                        if arg == 'ignorecase':
                            flags |= re.IGNORECASE
                        else:
                            raise ValueError()
                    self.current_syntax.addPattern(
                        args[1],
                        args[2],
                        args[3],
                        re.compile(args[4], flags))
                # eg. default to the Python syntax rules when viewing
                # a file ending with '.py' or '.pyw'
                #    syntax_files Python '\.pyw?$'
                elif args[0] == 'syntax_files' and (len(args) == 2 or len(args) == 3):
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
                elif args[0] == 'syntax_magic' and len(args) > 1:
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
                                raise ValueError()
                        self.syntax_magic_patterns[key] = re.compile(args[2], flags)
                else:
                    raise ValueError()
            # except ValueError:
            except:  # noqa: E722 # Grr... the 're' module throws weird errors
                utils.logError(_(f'Error processing line {i + 1} of {file_name}.'))


# colour resources
class _Colour:
    def __init__(self, r, g, b, a=1.0):
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
    def __init__(self, initial_state, default_token_type):
        # initial state for the state machine when parsing a new file
        self.initial_state = initial_state
        # default classification of characters that are not explicitly matched
        # by any state transition patterns
        self.default_token_type = default_token_type
        # mappings from a state to a list of (pattern, token_type, next_state)
        # tuples indicating the new state for the state machine when 'pattern'
        # is matched and how to classify the matched characters
        self.transitions_lookup = {initial_state: []}

    # Adds a new edge to the finite state machine from prev_state to
    # next_state.  Characters will be identified as token_type when pattern is
    # matched.  Any newly referenced state will be added.  Patterns for edges
    # leaving a state will be tested in the order they were added to the finite
    # state machine.
    def addPattern(self, prev_state, next_state, token_type, pattern):
        lookup = self.transitions_lookup
        for state in prev_state, next_state:
            if state not in lookup:
                lookup[state] = []
        lookup[prev_state].append([pattern, token_type, next_state])

    # given a string and an initial state, identify the final state and tokens
    def parse(self, state_name, s):
        lookup = self.transitions_lookup
        transitions, blocks, start = lookup[state_name], [], 0
        while start < len(s):
            for pattern, token_type, next_state in transitions:
                m = pattern.match(s, start)
                if m is not None:
                    end, state_name = m.span()[1], next_state
                    transitions = lookup[state_name]
                    break
            else:
                end, token_type = start + 1, self.default_token_type
            if len(blocks) > 0 and blocks[-1][2] == token_type:
                blocks[-1][1] = end
            else:
                blocks.append([start, end, token_type])
            start = end
        return state_name, blocks


theResources = Resources()
