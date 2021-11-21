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

class VcsInterface:
    """Interface for the VCSs."""

    def __init__(self, root):
        """The object will initialized with the repository's root folder."""
        self.root = root

    def getFileTemplate(self, prefs, name):
        """Indicates which revisions to display for a file when none were explicitly
           requested."""

    def getCommitTemplate(self, prefs, rev, names):
        """Indicates which file revisions to display for a commit."""

    def getFolderTemplate(self, prefs, names):
        """Indicates which file revisions to display for a set of folders."""

    def getRevision(self, prefs, name, rev):
        """Returns the contents of the specified file revision"""
