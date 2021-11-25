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

import codecs
import encodings
import os
import shlex
import sys

from diffuse import constants
from diffuse import utils

import gi  # type: ignore
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk  # type: ignore # noqa: E402


# class to store preferences and construct a dialogue for manipulating them
class Preferences:
    def __init__(self, path):
        self.bool_prefs = {}
        self.int_prefs = {}
        self.string_prefs = {}
        self.int_prefs_min = {}
        self.int_prefs_max = {}
        self.string_prefs_enums = {}

        # find available encodings
        self.encodings = sorted(set(encodings.aliases.aliases.values()))

        if utils.isWindows():
            svk_bin = 'svk.bat'
        else:
            svk_bin = 'svk'

        auto_detect_codecs = ['utf_8', 'utf_16', 'latin_1']
        e = utils.norm_encoding(sys.getfilesystemencoding())
        if e not in auto_detect_codecs:
            # insert after UTF-8 as the default encoding may prevent UTF-8 from
            # being tried
            auto_detect_codecs.insert(2, e)

        # self.template describes how preference dialogue layout
        #
        # this will be traversed later to build the preferences dialogue and
        # discover which preferences exist
        #
        # folders are described using:
        #    [ 'FolderSet', label1, template1, label2, template2, ... ]
        # lists are described using:
        #    [ 'List', template1, template2, template3, ... ]
        # individual preferences are described using one of the following
        # depending upon its type and the desired widget:
        #    [ 'Boolean', name, default, label ]
        #    [ 'Integer', name, default, label ]
        #    [ 'String', name, default, label ]
        #    [ 'File', name, default, label ]
        #    [ 'Font', name, default, label ]
        self.template = [
            'FolderSet',
            _('Display'),
            [
                'List',
                ['Font', 'display_font', 'Monospace 10', _('Font')],
                ['Integer', 'display_tab_width', 8, _('Tab width'), 1, 1024],
                ['Boolean', 'display_show_right_margin', True, _('Show right margin')],
                ['Integer', 'display_right_margin', 80, _('Right margin'), 1, 8192],
                ['Boolean', 'display_show_line_numbers', True, _('Show line numbers')],
                ['Boolean', 'display_show_whitespace', False, _('Show white space characters')],
                ['Boolean', 'display_ignore_case', False, _('Ignore case differences')],
                ['Boolean', 'display_ignore_whitespace', False, _('Ignore white space differences')],  # noqa: E501
                ['Boolean', 'display_ignore_whitespace_changes', False, _('Ignore changes to white space')],  # noqa: E501
                ['Boolean', 'display_ignore_blanklines', False, _('Ignore blank line differences')],
                ['Boolean', 'display_ignore_endofline', False, _('Ignore end of line differences')]
            ],
            _('Alignment'),
            [
                'List',
                ['Boolean', 'align_ignore_case', False, _('Ignore case')],
                ['Boolean', 'align_ignore_whitespace', True, _('Ignore white space')],
                ['Boolean', 'align_ignore_whitespace_changes', False, _('Ignore changes to white space')],  # noqa: E501
                ['Boolean', 'align_ignore_blanklines', False, _('Ignore blank lines')],
                ['Boolean', 'align_ignore_endofline', True, _('Ignore end of line characters')]
            ],
            _('Editor'),
            [
                'List',
                ['Boolean', 'editor_auto_indent', True, _('Auto indent')],
                ['Boolean', 'editor_expand_tabs', False, _('Expand tabs to spaces')],
                ['Integer', 'editor_soft_tab_width', 8, _('Soft tab width'), 1, 1024]
            ],
            _('Tabs'),
            [
                'List',
                ['Integer', 'tabs_default_panes', 2, _('Default panes'), 2, 16],
                ['Boolean', 'tabs_always_show', False, _('Always show the tab bar')],
                ['Boolean', 'tabs_warn_before_quit', True, _('Warn me when closing a tab will quit %s') % constants.APP_NAME]  # noqa: E501
            ],
            _('Regional Settings'),
            [
                'List',
                ['Encoding', 'encoding_default_codec', sys.getfilesystemencoding(), _('Default codec')],  # noqa: E501
                ['String', 'encoding_auto_detect_codecs', ' '.join(auto_detect_codecs), _('Order of codecs used to identify encoding')]  # noqa: E501
            ],
        ]

        # conditions used to determine if a preference should be greyed out
        self.disable_when = {
            'display_right_margin': ('display_show_right_margin', False),
            'display_ignore_whitespace_changes': ('display_ignore_whitespace', True),
            'display_ignore_blanklines': ('display_ignore_whitespace', True),
            'display_ignore_endofline': ('display_ignore_whitespace', True),
            'align_ignore_whitespace_changes': ('align_ignore_whitespace', True),
            'align_ignore_blanklines': ('align_ignore_whitespace', True),
            'align_ignore_endofline': ('align_ignore_whitespace', True)
        }
        if utils.isWindows():
            root = os.environ.get('SYSTEMDRIVE', None)
            if root is None:
                root = 'C:\\'
            elif not root.endswith('\\'):
                root += '\\'
            self.template.extend([
                    _('Cygwin'),
                    ['List',
                        ['File', 'cygwin_root', os.path.join(root, 'cygwin'), _('Root directory')],
                        ['String', 'cygwin_cygdrive_prefix', '/cygdrive', _('Cygdrive prefix')]]
                ])

        # create template for Version Control options
        vcs = [('bzr', 'Bazaar', 'bzr'),
               ('cvs', 'CVS', 'cvs'),
               ('darcs', 'Darcs', 'darcs'),
               ('git', 'Git', 'git'),
               ('hg', 'Mercurial', 'hg'),
               ('mtn', 'Monotone', 'mtn'),
               ('rcs', 'RCS', None),
               ('svn', 'Subversion', 'svn'),
               ('svk', 'SVK', svk_bin)]

        vcs_template = [
            'List', [
                'String',
                'vcs_search_order',
                'bzr cvs darcs git hg mtn rcs svn svk',
                _('Version control system search order')
            ]
        ]
        vcs_folders_template = ['FolderSet']
        for key, name, cmd in vcs:
            temp = ['List']
            if key == 'rcs':
                # RCS uses multiple commands
                temp.extend([['File', key + '_bin_co', 'co', _('"co" command')],
                             ['File', key + '_bin_rlog', 'rlog', _('"rlog" command')]])
            else:
                temp.extend([['File', key + '_bin', cmd, _('Command')]])
            if utils.isWindows():
                temp.append([
                    'Boolean',
                    key + '_bash',
                    False,
                    _('Launch from a Bash login shell')
                ])
                if key != 'git':
                    temp.append([
                        'Boolean',
                        key + '_cygwin',
                        False,
                        _('Update paths for Cygwin')
                    ])
            vcs_folders_template.extend([name, temp])
        vcs_template.append(vcs_folders_template)

        self.template.extend([_('Version Control'), vcs_template])
        self._initFromTemplate(self.template)
        self.default_bool_prefs = self.bool_prefs.copy()
        self.default_int_prefs = self.int_prefs.copy()
        self.default_string_prefs = self.string_prefs.copy()
        # load the user's preferences
        self.path = path
        if os.path.isfile(self.path):
            try:
                with open(self.path, 'r',  encoding='utf-8') as f:
                    ss = utils.readconfiglines(f)
                for j, s in enumerate(ss):
                    try:
                        a = shlex.split(s, True)
                        if len(a) > 0:
                            p = a[0]
                            if len(a) == 2 and p in self.bool_prefs:
                                self.bool_prefs[p] = (a[1] == 'True')
                            elif len(a) == 2 and p in self.int_prefs:
                                self.int_prefs[p] = max(
                                    self.int_prefs_min[p],
                                    min(int(a[1]), self.int_prefs_max[p]))
                            elif len(a) == 2 and p in self.string_prefs:
                                self.string_prefs[p] = a[1]
                            else:
                                raise ValueError()
                    except ValueError:
                        # this may happen if the prefs were written by a
                        # different version -- don't bother the user
                        utils.logDebug(f'Error processing line {j + 1} of {self.path}.')
            except IOError:
                # bad $HOME value? -- don't bother the user
                utils.logDebug(f'Error reading {self.path}.')

    # recursively traverses 'template' to discover the preferences and
    # initialise their default values in self.bool_prefs, self.int_prefs, and
    # self.string_prefs
    def _initFromTemplate(self, template):
        if template[0] == 'FolderSet' or template[0] == 'List':
            i = 1
            while i < len(template):
                if template[0] == 'FolderSet':
                    i += 1
                self._initFromTemplate(template[i])
                i += 1
        elif template[0] == 'Boolean':
            self.bool_prefs[template[1]] = template[2]
        elif template[0] == 'Integer':
            self.int_prefs[template[1]] = template[2]
            self.int_prefs_min[template[1]] = template[4]
            self.int_prefs_max[template[1]] = template[5]
        elif template[0] in ['String', 'File', 'Font', 'Encoding']:
            self.string_prefs[template[1]] = template[2]

    # callback used when a preference is toggled
    def _toggled_cb(self, widget, widgets, name):
        # disable any preferences than are no longer relevant
        for k, v in self.disable_when.items():
            p, t = v
            if p == name:
                widgets[k].set_sensitive(widgets[p].get_active() != t)

    # display the dialogue and update the preference values if the accept
    # button was pressed
    def runDialog(self, parent):
        dialog = Gtk.Dialog(_('Preferences'), parent=parent, destroy_with_parent=True)
        dialog.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT)
        dialog.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)

        widgets = {}
        w = self._buildPrefsDialog(parent, widgets, self.template)
        # disable any preferences than are not relevant
        for k, v in self.disable_when.items():
            p, t = v
            if widgets[p].get_active() == t:
                widgets[k].set_sensitive(False)
        dialog.vbox.add(w)
        w.show()

        accept = (dialog.run() == Gtk.ResponseType.OK)
        if accept:
            for k in self.bool_prefs:
                self.bool_prefs[k] = widgets[k].get_active()
            for k in self.int_prefs:
                self.int_prefs[k] = widgets[k].get_value_as_int()
            for k in self.string_prefs:
                self.string_prefs[k] = utils.null_to_empty(widgets[k].get_text())
            try:
                ss = []
                for k, v in self.bool_prefs.items():
                    if v != self.default_bool_prefs[k]:
                        ss.append(f'{k} {v}\n')
                for k, v in self.int_prefs.items():
                    if v != self.default_int_prefs[k]:
                        ss.append(f'{k} {v}\n')
                for k, v in self.string_prefs.items():
                    if v != self.default_string_prefs[k]:
                        v_escaped = v.replace('\\', '\\\\').replace('"', '\\"')
                        ss.append(f'{k} "{v_escaped}"\n')
                ss.sort()
                with open(self.path, 'w', encoding='utf-8') as f:
                    f.write(f'# This prefs file was generated by {constants.APP_NAME} {constants.VERSION}.\n\n')  # noqa: E501
                    for s in ss:
                        f.write(s)
            except IOError:
                utils.logErrorAndDialog(_('Error writing %s.') % (self.path, ), parent)
        dialog.destroy()
        return accept

    # recursively traverses 'template' to build the preferences dialogue
    # and the individual preference widgets into 'widgets' so their value
    # can be easily queried by the caller
    def _buildPrefsDialog(self, parent, widgets, template):
        tpl_section = template[0]
        if tpl_section == 'FolderSet':
            notebook = Gtk.Notebook.new()
            notebook.set_border_width(10)
            i = 1
            while i < len(template):
                label = Gtk.Label.new(template[i])
                i += 1
                w = self._buildPrefsDialog(parent, widgets, template[i])
                i += 1
                notebook.append_page(w, label)
                w.show()
                label.show()
            return notebook

        table = Gtk.Grid.new()
        table.set_border_width(10)
        for i, tpl in enumerate(template[1:]):
            tpl_section = tpl[0]
            if tpl_section == 'FolderSet':
                w = self._buildPrefsDialog(parent, widgets, tpl)
                table.attach(w, 0, i, 2, 1)
                w.show()
            elif tpl_section == 'Boolean':
                button = Gtk.CheckButton.new_with_mnemonic(tpl[3])
                button.set_active(self.bool_prefs[tpl[1]])
                widgets[tpl[1]] = button
                table.attach(button, 1, i, 1, 1)
                button.connect('toggled', self._toggled_cb, widgets, tpl[1])
                button.show()
            else:
                label = Gtk.Label.new(tpl[3] + ': ')
                label.set_xalign(1.0)
                label.set_yalign(0.5)
                table.attach(label, 0, i, 1, 1)
                label.show()
                if tpl[0] in ['Font', 'Integer']:
                    entry = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 0)
                    if tpl[0] == 'Font':
                        button = _FontButton()
                        button.set_font(self.string_prefs[tpl[1]])
                    else:
                        button = Gtk.SpinButton.new(
                            Gtk.Adjustment.new(self.int_prefs[tpl[1]], tpl[4], tpl[5], 1, 0, 0),
                            1.0,
                            0)
                    widgets[tpl[1]] = button
                    entry.pack_start(button, False, False, 0)
                    button.show()
                else:
                    if tpl[0] == 'Encoding':
                        entry = utils.EncodingMenu(self)
                        entry.set_text(tpl[3])
                    elif tpl[0] == 'File':
                        entry = _FileEntry(parent, tpl[3])
                    else:
                        entry = Gtk.Entry.new()
                    widgets[tpl[1]] = entry
                    entry.set_text(self.string_prefs[tpl[1]])
                table.attach(entry, 1, i, 1, 1)
                entry.show()
            table.show()
        return table

    # get/set methods to manipulate the preference values
    def getBool(self, name):
        return self.bool_prefs[name]

    def setBool(self, name, value):
        self.bool_prefs[name] = value

    def getInt(self, name):
        return self.int_prefs[name]

    def getString(self, name):
        return self.string_prefs[name]

    def setString(self, name, value):
        self.string_prefs[name] = value

    def getEncodings(self):
        return self.encodings

    def _getDefaultEncodings(self):
        return self.string_prefs['encoding_auto_detect_codecs'].split()

    def getDefaultEncoding(self):
        return self.string_prefs['encoding_default_codec']

    # attempt to convert a string to unicode from an unknown encoding
    def convertToUnicode(self, s):
        # a BOM is required for autodetecting UTF16 and UTF32
        magic = {'utf16': [codecs.BOM_UTF16_BE, codecs.BOM_UTF16_LE],
                 'utf32': [codecs.BOM_UTF32_BE, codecs.BOM_UTF32_LE]}
        for encoding in self._getDefaultEncodings():
            try:
                encoding = encoding.lower().replace('-', '').replace('_', '')
                for m in magic.get(encoding, [b'']):
                    if s.startswith(m):
                        break
                else:
                    continue
                return str(s, encoding=encoding), encoding
            except (UnicodeDecodeError, LookupError):
                pass
        return ''.join([chr(ord(c)) for c in s]), None

    # cygwin and native applications can be used on windows, use this method
    # to convert a path to the usual form expected on sys.platform
    def convertToNativePath(self, s):
        if utils.isWindows() and s.find('/') >= 0:
            # treat as a cygwin path
            s = s.replace(os.sep, '/')
            # convert to a Windows native style path
            p = [a for a in s.split('/') if a != '']
            if s.startswith('//'):
                p[:0] = ['', '']
            elif s.startswith('/'):
                pr = [a for a in self.getString('cygwin_cygdrive_prefix').split('/') if a != '']
                n = len(pr)
                if len(p) > n and len(p[n]) == 1 and p[:n] == pr:
                    # path starts with cygdrive prefix
                    p[:n + 1] = [p[n] + ':']
                else:
                    # full path
                    p[:0] = [a for a in self.getString('cygwin_root').split(os.sep) if a != '']
            # add trailing slash
            if p[-1] != '' and s.endswith('/'):
                p.append('')
            s = os.sep.join(p)
        return s


# adaptor class to allow a Gtk.FontButton to be read like a Gtk.Entry
class _FontButton(Gtk.FontButton):
    def __init__(self):
        Gtk.FontButton.__init__(self)

    def get_text(self):
        return self.get_font_name()


# text entry widget with a button to help pick file names
class _FileEntry(Gtk.Box):
    def __init__(self, parent, title):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.HORIZONTAL)
        self.toplevel = parent
        self.title = title
        self.entry = entry = Gtk.Entry.new()
        self.pack_start(entry, True, True, 0)
        entry.show()
        button = Gtk.Button.new()
        image = Gtk.Image.new()
        image.set_from_stock(Gtk.STOCK_OPEN, Gtk.IconSize.MENU)
        button.add(image)
        image.show()
        button.connect('clicked', self.chooseFile)
        self.pack_start(button, False, False, 0)
        button.show()

    # action performed when the pick file button is pressed
    def chooseFile(self, widget):
        dialog = Gtk.FileChooserDialog(
            self.title,
            self.toplevel,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        dialog.set_current_folder(os.path.realpath(os.curdir))
        if dialog.run() == Gtk.ResponseType.OK:
            self.entry.set_text(dialog.get_filename())
        dialog.destroy()

    def set_text(self, s):
        self.entry.set_text(s)

    def get_text(self):
        return self.entry.get_text()
