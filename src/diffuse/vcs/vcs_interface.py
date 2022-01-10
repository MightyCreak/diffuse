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

from abc import ABCMeta, abstractmethod
from typing import List, Optional, Tuple

from diffuse.preferences import Preferences


class VcsInterface(metaclass=ABCMeta):
    """Interface for the VCSs."""

    PathRevisionPair = Tuple[Optional[str], Optional[str]]
    PathRevisionList = List[PathRevisionPair]

    def __init__(self, root: str):
        """The object will initialized with the repository's root folder."""
        self.root = root

    @abstractmethod
    def getFileTemplate(self, prefs: Preferences, name: str) -> PathRevisionList:
        """Indicates which revisions to display for a file when none were explicitly
           requested."""

    @abstractmethod
    def getCommitTemplate(self, prefs, rev, names):
        """Indicates which file revisions to display for a commit."""

    @abstractmethod
    def getFolderTemplate(self, prefs, names):
        """Indicates which file revisions to display for a set of folders."""

    @abstractmethod
    def getRevision(self, prefs: Preferences, name: str, rev: str) -> bytes:
        """Returns the contents of the specified file revision"""
