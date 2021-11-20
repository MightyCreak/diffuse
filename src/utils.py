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

# pylint: disable=wrong-import-position
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
# pylint: enable=wrong-import-position

from diffuse import constants

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

# platform test
def isWindows():
    return os.name == 'nt'

def _logPrintOutput(msg):
    if constants.log_print_output:
        print(msg, file=sys.stderr)
        if constants.log_print_stack:
            traceback.print_stack()

# convenience function to display debug messages
def logDebug(msg):
    _logPrintOutput(f'DEBUG: {msg}')

# report error messages
def logError(msg):
    _logPrintOutput(f'ERROR: {msg}')

# report error messages and show dialog
def logErrorAndDialog(msg,parent=None):
    logError(msg)
    dialog = MessageDialog(parent, Gtk.MessageType.ERROR, msg)
    dialog.run()
    dialog.destroy()

# create nested subdirectories and return the complete path
def make_subdirs(p, ss):
    for s in ss:
        p = os.path.join(p, s)
        if not os.path.exists(p):
            try:
                os.mkdir(p)
            except IOError:
                pass
    return p

# returns the Windows drive or share from a from an absolute path
def _drive_from_path(path):
    d = path.split(os.sep)
    if len(d) > 3 and d[0] == '' and d[1] == '':
        return os.path.join(d[:4])
    return d[0]

# constructs a relative path from 'a' to 'b', both should be absolute paths
def relpath(a, b):
    if isWindows():
        if _drive_from_path(a) != _drive_from_path(b):
            return b
    c1 = [ c for c in a.split(os.sep) if c != '' ]
    c2 = [ c for c in b.split(os.sep) if c != '' ]
    i, n = 0, len(c1)
    while i < n and i < len(c2) and c1[i] == c2[i]:
        i += 1
    r = (n - i) * [ os.pardir ]
    r.extend(c2[i:])
    return os.sep.join(r)

# helper function prevent files from being confused with command line options
# by prepending './' to the basename
def safeRelativePath(abspath1, name, prefs, cygwin_pref):
    s = os.path.join(os.curdir, relpath(abspath1, os.path.abspath(name)))
    if isWindows():
        if prefs.getBool(cygwin_pref):
            s = s.replace('\\', '/')
        else:
            s = s.replace('/', '\\')
    return s

# escape arguments for use with bash
def _bash_escape(s):
    return "'" + s.replace("'", "'\\''") + "'"

def _use_flatpak():
    return constants.use_flatpak

# use popen to read the output of a command
def popenRead(dn, cmd, prefs, bash_pref, success_results=None):
    if success_results is None:
        success_results = [ 0 ]
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
        cmd = [ 'flatpak-spawn', '--host' ] + cmd
    with (
        subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=dn,
        startupinfo=info) as proc
    ):
        proc.stdin.close()
        proc.stderr.close()
        fd = proc.stdout
        # read the command's output
        s = fd.read()
        fd.close()
        if proc.wait() not in success_results:
            raise IOError('Command failed.')
        return s

# returns the number of characters in the string excluding any line ending
# characters
def len_minus_line_ending(s):
    if s is None:
        return 0
    n = len(s)
    if s.endswith('\r\n'):
        n -= 2
    elif s.endswith('\r') or s.endswith('\n'):
        n -= 1
    return n

# returns the string without the line ending characters
def strip_eol(s):
    if s:
        s = s[:len_minus_line_ending(s)]
    return s

# returns the list of strings without line ending characters
def _strip_eols(ss):
    return [ strip_eol(s) for s in ss ]

# use popen to read the output of a command
def popenReadLines(dn, cmd, prefs, bash_pref, success_results=None):
    return _strip_eols(splitlines(popenRead(
        dn, cmd, prefs, bash_pref, success_results).decode('utf-8', errors='ignore')))

# escape special glob characters
def globEscape(s):
    m = { c: f'[{c}]' for c in '[]?*' }
    return ''.join([ m.get(c, c) for c in s ])

# split string into lines based upon DOS, Mac, and Unix line endings
def splitlines(text: str) -> list[str]:
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
def readlines(fd):
    return _strip_eols(splitlines(fd.read()))

# use the program's location as a starting place to search for supporting files
# such as icon and help documentation
if hasattr(sys, 'frozen'):
    app_path = sys.executable
else:
    app_path = os.path.realpath(sys.argv[0])
bin_dir = os.path.dirname(app_path)

# translation location: '../share/locale/<LANG>/LC_MESSAGES/diffuse.mo'
# where '<LANG>' is the language key
lang = locale.getdefaultlocale()[0]
if isWindows():
    # gettext looks for the language using environment variables which
    # are normally not set on Windows so we try setting it for them
    for v in 'LC_ALL', 'LC_CTYPE', 'LANG', 'LANGUAGE':
        if v in os.environ:
            lang = os.environ[v]
            # remove any additional languages, encodings, or modifications
            for c in ':.@':
                lang = lang.split(c)[0]
            break
    else:
        if lang is not None:
            os.environ['LANG'] = lang
