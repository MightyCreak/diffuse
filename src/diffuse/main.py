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
import encodings

from gettext import gettext as _

from diffuse import constants, utils
from diffuse.resources import theResources
from diffuse.window import DiffuseWindow

import gi  # type: ignore
gi.require_version('Gtk', '3.0')
from gi.repository import Gio, GLib, Gtk  # type: ignore # noqa: E402


class DiffuseApplication(Gtk.Application):
    """The main application class."""

    def __init__(self, sysconfigdir):
        super().__init__(
            application_id=constants.APP_ID,
            flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE | Gio.ApplicationFlags.NON_UNIQUE)

        self.window = None
        self.sysconfigdir = sysconfigdir

        self.connect('shutdown', self.on_shutdown)

        self.add_main_option(
            'version',
            ord('v'),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.NONE,
            _('Display version and copyright information'),
            None,
        )
        self.add_main_option(
            'no-rcfile',
            0,
            GLib.OptionFlags.NONE,
            GLib.OptionArg.NONE,
            _('Do not read any resource files'),
            None,
        )
        self.add_main_option(
            'rcfile',
            0,
            GLib.OptionFlags.NONE,
            GLib.OptionArg.STRING,
            _('Specify explicit resource file'),
            'file',
        )
        self.add_main_option(
            'commit',
            ord('c'),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.STRING,
            _('File revisions <rev-1> and <rev>'),
            'rev',
        )
        self.add_main_option(
            'close-if-same',
            ord('D'),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.NONE,
            _('Close all tabs with no differences'),
        )
        self.add_main_option(
            'encoding',
            ord('e'),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.STRING,
            _('Use <codec> to read and write files'),
            'codec',
        )
        self.add_main_option(
            'label',
            ord('L'),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.STRING,
            _('Display <label> instead of the file name'),
            'label',
        )
        self.add_main_option(
            'modified',
            ord('m'),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.NONE,
            _('Create a new tab for each modified file'),
        )
        self.add_main_option(
            'revision',
            ord('r'),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.STRING,
            _('File revision <rev>'),
            'rev',
        )
        self.add_main_option(
            'separate',
            ord('s'),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.NONE,
            _('Create a new tab for each file'),
        )
        self.add_main_option(
            'tab',
            ord('t'),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.NONE,
            _('Start a new tab'),
        )
        self.add_main_option(
            'vcs',
            ord('V'),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.STRING,
            _('Version control system search order'),
            'vcs-list',
        )
        self.add_main_option(
            'line',
            0,
            GLib.OptionFlags.NONE,
            GLib.OptionArg.STRING,
            _('Start with line <line> selected'),
            'line',
        )
        self.add_main_option(
            'null-file',
            0,
            GLib.OptionFlags.NONE,
            GLib.OptionArg.NONE,
            _('Create a blank file comparison pane'),
        )
        self.add_main_option(
            'ignore-space-change',
            ord('b'),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.NONE,
            _('Ignore changes to white space'),
        )
        self.add_main_option(
            'ignore-blank-lines',
            ord('B'),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.NONE,
            _('Ignore changes in blank lines'),
        )
        self.add_main_option(
            'ignore-end-of-line',
            ord('E'),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.NONE,
            _('Ignore end of line differences'),
        )
        self.add_main_option(
            'ignore-case',
            ord('i'),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.NONE,
            _('Ignore case differences'),
        )
        self.add_main_option(
            'ignore-all-space',
            ord('w'),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.NONE,
            _('Ignore white space differences'),
        )
        self.set_option_context_summary(_(
            '''Diffuse is a graphical tool for merging and comparing text files. Diffuse is
able to compare an arbitrary number of files side-by-side and gives users the
ability to manually adjust line matching and directly edit files. Diffuse can
also retrieve revisions of files from several VCSs for comparison and merging.'''
        ))

    def do_activate(self) -> None:
        """Called when the application is activated."""
        self.window.present()

    def do_command_line(self, command_line):
        """Called to treat the command line options."""
        options = command_line.get_options_dict()
        # convert GVariantDict -> GVariant -> dict
        options = options.end().unpack()

        if 'version' in options:
            print('%s %s\n%s' % (constants.APP_NAME, constants.VERSION, constants.COPYRIGHT))
            return 0

        # find the config directory and create it if it didn't exist
        rc_dir = os.environ.get('XDG_CONFIG_HOME', None)
        subdirs = ['diffuse']
        if rc_dir is None:
            rc_dir = os.path.expanduser('~')
            subdirs.insert(0, '.config')
        rc_dir = utils.make_subdirs(rc_dir, subdirs)

        # find the local data directory and create it if it didn't exist
        data_dir = os.environ.get('XDG_DATA_HOME', None)
        subdirs = ['diffuse']
        if data_dir is None:
            data_dir = os.path.expanduser('~')
            subdirs[:0] = ['.local', 'share']
        data_dir = utils.make_subdirs(data_dir, subdirs)

        # load resource files
        rc_files = []
        if 'no-rcfile' not in options:
            # parse system wide then personal initialization files
            if utils.isWindows():
                rc_file = os.path.join(utils.bin_dir, 'diffuserc')
            else:
                rc_file = os.path.join(utils.bin_dir, self.sysconfigdir, 'diffuserc')
            for rc_file in rc_file, os.path.join(rc_dir, 'diffuserc'):
                if os.path.isfile(rc_file):
                    rc_files.append(rc_file)
        if 'rcfile' in options:
            rc_files.append(options['rcfile'])
        for rc_file in rc_files:
            # convert to absolute path so the location of any processing errors are
            # reported with normalized file names
            rc_file = os.path.abspath(rc_file)
            try:
                theResources.parse(rc_file)
            except IOError:
                utils.logError(_('Error reading %s.') % (rc_file,))

        diff_window = DiffuseWindow(rc_dir, application=self)
        self.window = diff_window

        # load state
        self.statepath = os.path.join(data_dir, 'state')
        diff_window.load_state(self.statepath)

        # process remaining command line arguments
        encoding = None
        revs = []
        close_on_same = False
        specs = []
        had_specs = False
        labels = []
        funcs = {
            'modified': diff_window.createModifiedFileTabs,
            'commit': diff_window.createCommitFileTabs,
            'separate': diff_window.createSeparateTabs,
            'single': diff_window.createSingleTab,
        }
        mode = 'single'
        opts = {}
        if 'commit' in options:
            # specified revision
            funcs[mode](specs, labels, options)
            specs, labels, opts = [], [], {'commit': options['commit']}
            mode = 'commit'
        if 'close-if-same' in options:
            close_on_same = True
        if 'encoding' in options:
            encoding = options['encoding']
            encoding = encodings.aliases.aliases.get(encoding, encoding)
        if 'modified' in options:
            funcs[mode](specs, labels, opts)
            specs, labels, opts = [], [], {}
            mode = 'modified'
        if 'revision' in options:
            # specified revision
            revs.append((options['revision'], encoding))
        if 'separate' in options:
            funcs[mode](specs, labels, opts)
            specs, labels, opts = [], [], {}
            # open items in separate tabs
            mode = 'separate'
        if 'tab' in options:
            funcs[mode](specs, labels, opts)
            specs, labels, opts = [], [], {}
            # start a new tab
            mode = 'single'
        if 'vcs' in options:
            diff_window.prefs.setString('vcs_search_order', options['vcs'])
            diff_window.preferences_updated()
        if 'ignore-space-change' in options:
            diff_window.prefs.setBool('display_ignore_whitespace_changes', True)
            diff_window.prefs.setBool('align_ignore_whitespace_changes', True)
            diff_window.preferences_updated()
        if 'ignore-blank-lines' in options:
            diff_window.prefs.setBool('display_ignore_blanklines', True)
            diff_window.prefs.setBool('align_ignore_blanklines', True)
            diff_window.preferences_updated()
        if 'ignore-end-of-line' in options:
            diff_window.prefs.setBool('display_ignore_endofline', True)
            diff_window.prefs.setBool('align_ignore_endofline', True)
            diff_window.preferences_updated()
        if 'ignore-case' in options:
            diff_window.prefs.setBool('display_ignore_case', True)
            diff_window.prefs.setBool('align_ignore_case', True)
            diff_window.preferences_updated()
        if 'ignore-all-space' in options:
            diff_window.prefs.setBool('display_ignore_whitespace', True)
            diff_window.prefs.setBool('align_ignore_whitespace', True)
            diff_window.preferences_updated()
        if 'label' in options:
            labels.append(options['label'])
        if 'line' in options:
            try:
                opts['line'] = int(options['line'])
            except ValueError:
                utils.logError(_('Error parsing line number.'))
        if 'null-file' in options:
            # add a blank file pane
            if mode == 'single' or mode == 'separate':
                if len(revs) == 0:
                    revs.append((None, encoding))
                specs.append((None, revs))
                revs = []
            had_specs = True
        for arg in command_line.get_arguments()[1:]:
            filename = diff_window.prefs.convertToNativePath(arg)
            if (mode == 'single' or mode == 'separate') and os.path.isdir(filename):
                if len(specs) > 0:
                    filename = os.path.join(filename, os.path.basename(specs[-1][0]))
                else:
                    utils.logError(
                        _('Error processing argument "%s".  Directory not expected.') % (arg,))
                    filename = None
            if filename is not None:
                if len(revs) == 0:
                    revs.append((None, encoding))
                specs.append((filename, revs))
                revs = []
            had_specs = True
        if mode in ['modified', 'commit'] and len(specs) == 0:
            specs.append((os.curdir, [(None, encoding)]))
            had_specs = True
        funcs[mode](specs, labels, opts)

        # create a file diff viewer if the command line arguments haven't
        # implicitly created any
        if not had_specs:
            diff_window.newLoadedFileDiffViewer([])
        elif close_on_same:
            diff_window.closeOnSame()
        nb = diff_window.notebook
        n = nb.get_n_pages()
        if n > 0:
            nb.set_show_tabs(diff_window.prefs.getBool('tabs_always_show') or n > 1)
            nb.get_nth_page(0).grab_focus()

        self.activate()
        return 0

    def on_shutdown(self, application: Gio.Application) -> None:
        self.window.save_state(self.statepath)


def main(version: str, sysconfigdir: str) -> int:
    """The application's entry point."""
    constants.VERSION = version

    app = DiffuseApplication(sysconfigdir)
    return app.run(sys.argv)
