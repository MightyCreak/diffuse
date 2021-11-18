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

class FolderSet:
    '''Utility class to help support Git and Monotone.
       Represents a set of files and folders of interest for "git status" or
       "mtn automate inventory."'''

    def __init__(self, names):
        self.folders = f = []
        for name in names:
            name = os.path.abspath(name)
            # ensure all names end with os.sep
            if not name.endswith(os.sep):
                name += os.sep
            f.append(name)

    # returns True if the given abspath is a file that should be included in
    # the interesting file subset
    def contains(self, abspath):
        if not abspath.endswith(os.sep):
            abspath += os.sep
        for f in self.folders:
            if abspath.startswith(f):
                return True
        return False

