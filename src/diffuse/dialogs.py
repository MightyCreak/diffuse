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

from gettext import gettext as _
from typing import Optional

from diffuse import constants
from diffuse import utils

import gi  # type: ignore
gi.require_version('GObject', '2.0')
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gtk  # type: ignore # noqa: E402


# the about dialog
class AboutDialog(Gtk.AboutDialog):
    def __init__(self) -> None:
        Gtk.AboutDialog.__init__(self)
        self.set_logo_icon_name('io.github.mightycreak.Diffuse')
        self.set_program_name(constants.APP_NAME)
        self.set_version(constants.VERSION)
        self.set_comments(_('Diffuse is a graphical tool for merging and comparing text files.'))
        self.set_copyright(constants.COPYRIGHT)
        self.set_website(constants.WEBSITE)
        self.set_authors(['Derrick Moser <derrick_moser@yahoo.com>',
                          'Romain Failliot <romain.failliot@foolstep.com>'])
        self.set_translator_credits(_('translator-credits'))
        license_text = [
            constants.APP_NAME + ' ' + constants.VERSION + '\n\n',
            constants.COPYRIGHT + '\n\n',
            '''This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.''']
        self.set_license(''.join(license_text))


# custom dialogue for picking files with widgets for specifying the encoding
# and revision
class FileChooserDialog(Gtk.FileChooserDialog):
    # record last chosen folder so the file chooser can start at a more useful
    # location for empty panes
    last_chosen_folder = os.path.realpath(os.curdir)

    @staticmethod
    def _current_folder_changed_cb(widget):
        FileChooserDialog.last_chosen_folder = widget.get_current_folder()

    def __init__(self, title, parent, prefs, action, accept, rev=False):
        Gtk.FileChooserDialog.__init__(self, title=title, transient_for=parent, action=action)
        self.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.add_button(accept, Gtk.ResponseType.OK)
        self.prefs = prefs
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0, border_width=5)
        label = Gtk.Label(label=_('Encoding: '))
        hbox.pack_start(label, False, False, 0)
        label.show()
        self._encoding = utils.EncodingMenu(
            prefs=prefs,
            autodetect=action in [Gtk.FileChooserAction.OPEN, Gtk.FileChooserAction.SELECT_FOLDER])
        hbox.pack_start(self._encoding, False, False, 5)
        self._encoding.show()
        if rev:
            self._revision = Gtk.Entry()
            hbox.pack_end(self._revision, False, False, 0)
            self._revision.show()
            label = Gtk.Label(label=_('Revision: '))
            hbox.pack_end(label, False, False, 0)
            label.show()

        self.vbox.pack_start(hbox, False, False, 0)
        hbox.show()
        self.set_current_folder(self.last_chosen_folder)
        self.connect('current-folder-changed', self._current_folder_changed_cb)

    def set_encoding(self, encoding: Optional[str]) -> None:
        self._encoding.set_text(encoding)

    def get_encoding(self) -> Optional[str]:
        return self._encoding.get_text()

    def get_revision(self) -> str:
        return self._revision.get_text()

    def get_filename(self) -> str:
        # convert from UTF-8 string to unicode
        return Gtk.FileChooserDialog.get_filename(self)


# dialogue used to search for text
class NumericDialog(Gtk.Dialog):
    def __init__(self, parent, title, text, val, lower, upper, step=1, page=0):
        Gtk.Dialog.__init__(self, title=title, transient_for=parent, destroy_with_parent=True)
        self.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT)
        self.add_button(Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        vbox.set_border_width(10)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        label = Gtk.Label(label=text)
        hbox.pack_start(label, False, False, 0)
        label.show()

        adj = Gtk.Adjustment(
            value=val,
            lower=lower,
            upper=upper,
            step_increment=step,
            page_increment=page,
            page_size=0)
        self._button = Gtk.SpinButton(adjustment=adj, climb_rate=1.0, digits=0)
        self._button.connect('activate', self._button_cb)
        hbox.pack_start(self._button, True, True, 0)
        self._button.show()

        vbox.pack_start(hbox, True, True, 0)
        hbox.show()

        self.vbox.pack_start(vbox, False, False, 0)
        vbox.show()

    def _button_cb(self, widget: Gtk.SpinButton) -> None:
        self.response(Gtk.ResponseType.ACCEPT)

    def get_value(self) -> int:
        return self._button.get_value_as_int()


# dialogue used to search for text
class SearchDialog(Gtk.Dialog):
    def __init__(self, parent, pattern=None, history=None):
        Gtk.Dialog.__init__(
            self,
            title=_('Find...'),
            transient_for=parent,
            destroy_with_parent=True)
        self.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT)
        self.add_button(Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        vbox.set_border_width(10)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        label = Gtk.Label(label=_('Search For: '))
        hbox.pack_start(label, False, False, 0)
        label.show()
        combo = Gtk.ComboBoxText.new_with_entry()
        self._entry = combo.get_child()
        self._entry.connect('activate', self._entry_cb)

        if pattern is not None:
            self._entry.set_text(pattern)

        if history is not None:
            completion = Gtk.EntryCompletion()
            liststore = Gtk.ListStore(GObject.TYPE_STRING)
            completion.set_model(liststore)
            completion.set_text_column(0)
            for h in history:
                liststore.append([h])
                combo.append_text(h)
            self._entry.set_completion(completion)

        hbox.pack_start(combo, True, True, 0)
        combo.show()
        vbox.pack_start(hbox, False, False, 0)
        hbox.show()

        button = Gtk.CheckButton.new_with_mnemonic(_('Match Case'))
        self.match_case_button = button
        vbox.pack_start(button, False, False, 0)
        button.show()

        button = Gtk.CheckButton.new_with_mnemonic(_('Search Backwards'))
        self.backwards_button = button
        vbox.pack_start(button, False, False, 0)
        button.show()

        self.vbox.pack_start(vbox, False, False, 0)
        vbox.show()

    # callback used when the Enter key is pressed
    def _entry_cb(self, widget: Gtk.Entry) -> None:
        self.response(Gtk.ResponseType.ACCEPT)

    def get_search_text(self) -> str:
        return self._entry.get_text()
