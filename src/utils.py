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

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# convenience class for displaying a message dialogue
class MessageDialog(Gtk.MessageDialog):
    def __init__(self, parent, type, s):
        if type == Gtk.MessageType.ERROR:
            buttons = Gtk.ButtonsType.OK
        else:
            buttons = Gtk.ButtonsType.OK_CANCEL
        Gtk.MessageDialog.__init__(self, parent = parent, destroy_with_parent = True, message_type = type, buttons = buttons, text = s)
        self.set_title(APP_NAME)

# platform test
def isWindows():
    return os.name == 'nt'

# convenience function to display debug messages
def logDebug(s):
    pass #sys.stderr.write(f'{APP_NAME}: {s}\n')

# report error messages
def logError(s):
    m = MessageDialog(None, Gtk.MessageType.ERROR, s)
    m.run()
    m.destroy()

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

APP_NAME = 'Diffuse'
VERSION = '0.0.0'
COPYRIGHT =  '''{copyright} © 2006-2019 Derrick Moser
{copyright} © 2015-2021 Romain Failliot'''.format(copyright=_("Copyright"))
WEBSITE = 'https://mightycreak.github.io/diffuse/'
