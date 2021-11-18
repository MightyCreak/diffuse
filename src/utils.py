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

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from diffuse import constants

# convenience class for displaying a message dialogue
class MessageDialog(Gtk.MessageDialog):
    def __init__(self, parent, type, s):
        if type == Gtk.MessageType.ERROR:
            buttons = Gtk.ButtonsType.OK
        else:
            buttons = Gtk.ButtonsType.OK_CANCEL
        Gtk.MessageDialog.__init__(self, parent = parent, destroy_with_parent = True, message_type = type, buttons = buttons, text = s)
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

def useFlatpak():
    return constants.use_flatpak

# constructs a relative path from 'a' to 'b', both should be absolute paths
def relpath(a, b):
    if isWindows():
        if drive_from_path(a) != drive_from_path(b):
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
    s = os.path.join(os.curdir, utils.relpath(abspath1, os.path.abspath(name)))
    if utils.isWindows():
        if prefs.getBool(cygwin_pref):
            s = s.replace('\\', '/')
        else:
            s = s.replace('/', '\\')
    return s

# use popen to read the output of a command
def popenRead(dn, cmd, prefs, bash_pref, success_results=None):
    if success_results is None:
        success_results = [ 0 ]
    if isWindows() and prefs.getBool(bash_pref):
        # launch the command from a bash shell is requested
        cmd = [ prefs.convertToNativePath('/bin/bash.exe'), '-l', '-c', 'cd {}; {}'.format(bashEscape(dn), ' '.join([ bashEscape(arg) for arg in cmd ])) ]
        dn = None
    # use subprocess.Popen to retrieve the file contents
    if isWindows():
        info = subprocess.STARTUPINFO()
        info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        info.wShowWindow = subprocess.SW_HIDE
    else:
        info = None
    if useFlatpak():
        cmd = [ 'flatpak-spawn', '--host' ] + cmd
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=dn, startupinfo=info)
    proc.stdin.close()
    proc.stderr.close()
    fd = proc.stdout
    # read the command's output
    s = fd.read()
    fd.close()
    if proc.wait() not in success_results:
        raise IOError('Command failed.')
    return s

# use popen to read the output of a command
def popenReadLines(dn, cmd, prefs, bash_pref, success_results=None):
    return strip_eols(splitlines(popenRead(dn, cmd, prefs, bash_pref, success_results).decode('utf-8', errors='ignore')))

# simulate use of popen with xargs to read the output of a command
def popenXArgsReadLines(dn, cmd, args, prefs, bash_pref):
    # os.sysconf() is only available on Unix
    if hasattr(os, 'sysconf'):
        maxsize = os.sysconf('SC_ARG_MAX')
        maxsize -= sum([ len(k) + len(v) + 2 for k, v in os.environ.items() ])
    else:
        # assume the Window's limit to CreateProcess()
        maxsize = 32767
    maxsize -= sum([ len(k) + 1 for k in cmd ])

    ss = []
    i, s, a = 0, 0, []
    while i < len(args):
        f = (len(a) == 0)
        if f:
            # start a new command line
            a = cmd[:]
        elif s + len(args[i]) + 1 <= maxsize:
            f = True
        if f:
            # append another argument to the current command line
            a.append(args[i])
            s += len(args[i]) + 1
            i += 1
        if i == len(args) or not f:
            ss.extend(popenReadLines(dn, a, prefs, bash_pref))
            s, a = 0, []
    return ss

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
            for v in ':.@':
                lang = lang.split(v)[0]
            break
    else:
        if lang is not None:
            os.environ['LANG'] = lang
