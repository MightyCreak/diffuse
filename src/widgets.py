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

# pylint: disable=wrong-import-position
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk
# pylint: enable=wrong-import-position

from diffuse import utils

# This is a replacement for Gtk.ScrolledWindow as it forced expose events to be
# handled immediately after changing the viewport position.  This could cause
# the application to become unresponsive for a while as it processed a large
# queue of keypress and expose event pairs.
class ScrolledWindow(Gtk.Grid):
    scroll_directions = set((Gdk.ScrollDirection.UP,
                             Gdk.ScrollDirection.DOWN,
                             Gdk.ScrollDirection.LEFT,
                             Gdk.ScrollDirection.RIGHT))

    def __init__(self, hadj, vadj):
        Gtk.Grid.__init__(self)
        self.position = (0, 0)
        self.scroll_count = 0
        self.partial_redraw = False

        self.hadj, self.vadj = hadj, vadj
        vport = Gtk.Viewport.new()
        darea = Gtk.DrawingArea.new()
        darea.add_events(Gdk.EventMask.SCROLL_MASK)
        self.darea = darea
        # replace darea's queue_draw_area with our own so we can tell when
        # to disable/enable our scrolling optimisation
        self.darea_queue_draw_area = darea.queue_draw_area
        darea.queue_draw_area = self.redraw_region
        vport.add(darea)
        darea.show()
        self.attach(vport, 0, 0, 1, 1)
        vport.set_vexpand(True)
        vport.set_hexpand(True)
        vport.show()

        self.vbar = Gtk.Scrollbar.new(Gtk.Orientation.VERTICAL, vadj)
        self.attach(self.vbar, 1, 0, 1, 1)
        self.vbar.show()

        self.hbar = Gtk.Scrollbar.new(Gtk.Orientation.HORIZONTAL, hadj)
        self.attach(self.hbar, 0, 1, 1, 1)
        self.hbar.show()

        # listen to our signals
        hadj.connect('value-changed', self.value_changed_cb)
        vadj.connect('value-changed', self.value_changed_cb)
        darea.connect('configure-event', self.configure_cb)
        darea.connect('scroll-event', self.scroll_cb)
        darea.connect('draw', self.draw_cb)

    # updates the adjustments to match the new widget size
    def configure_cb(self, widget, event):
        w, h = event.width, event.height
        for adj, d in (self.hadj, w), (self.vadj, h):
            v = adj.get_value()
            if v + d > adj.get_upper():
                adj.set_value(max(0, adj.get_upper() - d))
            adj.set_page_size(d)
            adj.set_page_increment(d)

    # update the vertical adjustment when the mouse's scroll wheel is used
    def scroll_cb(self, widget, event):
        d = event.direction
        if d in self.scroll_directions:
            delta = 100
            if d in (Gdk.ScrollDirection.UP, Gdk.ScrollDirection.LEFT):
                delta = -delta
            vertical = (d in (Gdk.ScrollDirection.UP, Gdk.ScrollDirection.DOWN))
            if event.state & Gdk.ModifierType.SHIFT_MASK:
                vertical = not vertical
            if vertical:
                adj = self.vadj
            else:
                adj = self.hadj
            utils.step_adjustment(adj, delta)

    def value_changed_cb(self, widget):
        old_x, old_y = self.position
        pos_x = int(self.hadj.get_value())
        pos_y = int(self.vadj.get_value())
        self.position = (pos_x, pos_y)
        if self.darea.get_window() is not None:
            # window.scroll() although visually nice, is slow, revert to
            # queue_draw() if scroll a lot without seeing an expose event
            if self.scroll_count < 2 and not self.partial_redraw:
                self.scroll_count += 1
                self.darea.get_window().scroll(old_x - pos_x, old_y - pos_y)
            else:
                self.partial_redraw = False
                self.darea.queue_draw()

    def draw_cb(self, widget, cr):
        self.scroll_count = 0

    # replacement for darea.queue_draw_area that notifies us when a partial
    # redraw happened
    def redraw_region(self, x, y, w, h):
        self.partial_redraw = True
        self.darea_queue_draw_area(x, y, w, h)
