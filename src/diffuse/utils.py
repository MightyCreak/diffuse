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

import os
import sys
import locale
import subprocess
import traceback

from enum import IntFlag
from gettext import gettext as _
from typing import Final, List, Optional, TextIO

from diffuse import constants
from diffuse.preferences import Preferences
from diffuse.resources import theResources

import gi  # type: ignore
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk  # type: ignore # noqa: E402


# convenience class for displaying a message dialogue
class MessageDialog(Gtk.MessageDialog):
    def __init__(self, parent, message_type, s):
        if message_type == Gtk.MessageType.ERROR:
            buttons = Gtk.ButtonsType.OK
        else:
            buttons = Gtk.ButtonsType.OK_CANCEL
        Gtk.MessageDialog.__init__(
            self,
            parent=parent,
            destroy_with_parent=True,
            message_type=message_type,
            buttons=buttons,
            text=s)
        self.set_title(constants.APP_NAME)


# widget to help pick an encoding
class EncodingMenu(Gtk.Box):
    def __init__(self, prefs, autodetect=False):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.HORIZONTAL)
        self.combobox = combobox = Gtk.ComboBoxText.new()
        self.encodings = prefs.getEncodings()[:]
        for e in self.encodings:
            combobox.append_text(e)
        if autodetect:
            self.encodings.insert(0, None)
            combobox.prepend_text(_('Auto Detect'))
        self.pack_start(combobox, False, False, 0)
        combobox.show()

    def set_text(self, encoding):
        encoding = norm_encoding(encoding)
        if encoding in self.encodings:
            self.combobox.set_active(self.encodings.index(encoding))

    def get_text(self):
        i = self.combobox.get_active()
        return self.encodings[i] if i >= 0 else None


def isWindows() -> bool:
    '''Returns true if OS is Windows; otherwise false.'''
    return os.name == 'nt'


def _logPrintOutput(msg: str) -> None:
    if theResources.getOptionAsBool('log_print_output'):
        print(msg, file=sys.stderr)
        if theResources.getOptionAsBool('log_print_stack'):
            traceback.print_stack()


def logDebug(msg: str) -> None:
    '''Report debug message.'''
    _logPrintOutput(f'DEBUG: {msg}')


def logError(msg: str) -> None:
    '''Report error message.'''
    _logPrintOutput(f'ERROR: {msg}')


def logErrorAndDialog(msg: str, parent: Gtk.Widget = None) -> None:
    '''Report error message and show dialog.'''
    logError(msg)
    dialog = MessageDialog(parent, Gtk.MessageType.ERROR, msg)
    dialog.run()
    dialog.destroy()


def make_subdirs(p: str, ss: List[str]) -> str:
    '''Create nested subdirectories and return the complete path.'''
    for s in ss:
        p = os.path.join(p, s)
        if not os.path.exists(p):
            try:
                os.mkdir(p)
            except IOError:
                pass
    return p


def _drive_from_path(path: str) -> str:
    '''Returns the Windows drive or share from a from an absolute path.'''
    d = path.split(os.sep)
    if len(d) > 3 and d[0] == '' and d[1] == '':
        return os.path.join(*d[:4])
    return d[0]


def relpath(a: str, b: str) -> str:
    '''Constructs a relative path from 'a' to 'b', both should be absolute paths.'''
    if isWindows():
        if _drive_from_path(a) != _drive_from_path(b):
            return b
    c1 = [c for c in a.split(os.sep) if c != '']
    c2 = [c for c in b.split(os.sep) if c != '']
    i, n = 0, len(c1)
    while i < n and i < len(c2) and c1[i] == c2[i]:
        i += 1
    r = (n - i) * [os.pardir]
    r.extend(c2[i:])
    return os.sep.join(r)


# helper function prevent files from being confused with command line options
# by prepending './' to the basename
def safeRelativePath(abspath1: str, name: str, prefs: Preferences, cygwin_pref: str) -> str:
    s = os.path.join(os.curdir, relpath(abspath1, os.path.abspath(name)))
    if isWindows():
        if prefs.getBool(cygwin_pref):
            s = s.replace('\\', '/')
        else:
            s = s.replace('/', '\\')
    return s


def _bash_escape(s: str) -> str:
    '''Escape arguments for use with bash.'''
    return "'" + s.replace("'", "'\\''") + "'"


def _use_flatpak() -> bool:
    return theResources.getOptionAsBool('use_flatpak')


# use popen to read the output of a command
def popenRead(dn, cmd, prefs, bash_pref, success_results=None):
    if success_results is None:
        success_results = [0]
    if isWindows() and prefs.getBool(bash_pref):
        # launch the command from a bash shell is requested
        cmd = [
            prefs.convertToNativePath('/bin/bash.exe'),
            '-l',
            '-c',
            f"cd {_bash_escape(dn)}; {' '.join([ _bash_escape(arg) for arg in cmd ])}"
        ]
        dn = None
    # use subprocess.Popen to retrieve the file contents
    if isWindows():
        info = subprocess.STARTUPINFO()
        info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        info.wShowWindow = subprocess.SW_HIDE
    else:
        info = None
    if _use_flatpak():
        cmd = ['flatpak-spawn', '--host'] + cmd
    with subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=dn,
            startupinfo=info) as proc:
        proc.stdin.close()
        proc.stderr.close()
        fd = proc.stdout
        # read the command's output
        s = fd.read()
        fd.close()
        if proc.wait() not in success_results:
            raise IOError('Command failed.')
        return s


def len_minus_line_ending(s: str) -> int:
    '''Returns the number of characters in the string excluding any line ending characters.'''
    if s is None:
        return 0
    n = len(s)
    if s.endswith('\r\n'):
        n -= 2
    elif s.endswith('\r') or s.endswith('\n'):
        n -= 1
    return n


def strip_eol(s: str) -> str:
    '''Returns the string without the line ending characters.'''
    if s:
        s = s[:len_minus_line_ending(s)]
    return s


def _strip_eols(ss: List[str]) -> List[str]:
    '''Returns the list of strings without line ending characters.'''
    return [strip_eol(s) for s in ss]


# use popen to read the output of a command
def popenReadLines(dn, cmd, prefs, bash_pref, success_results=None):
    return _strip_eols(splitlines(popenRead(
        dn, cmd, prefs, bash_pref, success_results).decode('utf-8', errors='ignore')))


def readconfiglines(fd: TextIO) -> List[str]:
    return fd.read().replace('\r', '').split('\n')


def globEscape(s: str) -> str:
    '''Escape special glob characters.'''
    m = {c: f'[{c}]' for c in '[]?*'}
    return ''.join([m.get(c, c) for c in s])


# split string into lines based upon DOS, Mac, and Unix line endings
def splitlines(text: str) -> List[str]:
    # split on new line characters
    temp, i, n = [], 0, len(text)
    while i < n:
        j = text.find('\n', i)
        if j < 0:
            temp.append(text[i:])
            break
        j += 1
        temp.append(text[i:j])
        i = j
    # split on carriage return characters
    ss = []
    for s in temp:
        i, n = 0, len(s)
        while i < n:
            j = s.find('\r', i)
            if j < 0:
                ss.append(s[i:])
                break
            j += 1
            if j < n and s[j] == '\n':
                j += 1
            ss.append(s[i:j])
            i = j
    return ss


# also recognize old Mac OS line endings
def readlines(fd: TextIO) -> List[str]:
    return _strip_eols(splitlines(fd.read()))


def norm_encoding(e: Optional[str]) -> Optional[str]:
    '''Map an encoding name to its standard form.'''
    if e is not None:
        return e.replace('-', '_').lower()
    return None


def null_to_empty(s: Optional[str]) -> str:
    if s is None:
        s = ''
    return s


# utility method to step advance an adjustment
def step_adjustment(adj: Gtk.Adjustment, delta: int) -> None:
    v = adj.get_value() + delta
    # clamp to the allowed range
    v = max(v, int(adj.get_lower()))
    v = min(v, int(adj.get_upper() - adj.get_page_size()))
    adj.set_value(v)


def _get_default_lang() -> Optional[str]:
    lang = locale.getdefaultlocale()[0]
    if isWindows():
        # gettext looks for the language using environment variables which
        # are normally not set on Windows so we try setting it for them
        for lang_env in 'LC_ALL', 'LC_CTYPE', 'LANG', 'LANGUAGE':
            if lang_env in os.environ:
                lang = os.environ[lang_env]
                # remove any additional languages, encodings, or modifications
                for c in ':.@':
                    lang = lang.split(c)[0]
                break
        else:
            if lang is not None:
                os.environ['LANG'] = lang
    return lang


class LineEnding(IntFlag):
    '''Enumeration of line endings.

    Values can be used as flags in bitwise operations.'''

    DOS_FORMAT = 1
    MAC_FORMAT = 2
    UNIX_FORMAT = 4


# avoid some dictionary lookups when string.whitespace is used in loops
# this is sorted based upon frequency to speed up code for stripping whitespace
whitespace: Final[str] = ' \t\n\r\x0b\x0c'

# use the program's location as a starting place to search for supporting files
# such as icon and help documentation
app_path: Final[str] = sys.executable if hasattr(sys, 'frozen') else os.path.realpath(sys.argv[0])
bin_dir: Final[str] = os.path.dirname(app_path)

# translation location: '../share/locale/<LANG>/LC_MESSAGES/diffuse.mo'
# where '<LANG>' is the language key
lang: Final[Optional[str]] = _get_default_lang()
