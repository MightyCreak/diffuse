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

from typing import Optional, Tuple

from diffuse import utils
from diffuse.vcs.svn import Svn


class Svk(Svn):
    @staticmethod
    def _getVcs() -> str:
        return 'svk'

    @staticmethod
    def _getURLPrefix() -> str:
        return 'Depot Path: '

    @staticmethod
    def _parseStatusLine(s: str) -> Tuple[str, str]:
        if len(s) < 4 or s[0] not in 'ACDMR':
            return '', ''
        return s[0], s[4:]

    @staticmethod
    def _getPreviousRevision(rev: Optional[str]) -> str:
        if rev is None:
            return 'HEAD'
        if rev.endswith('@'):
            return str(int(rev[:-1]) - 1) + '@'
        return str(int(rev) - 1)

    def getRevision(self, prefs, name, rev):
        relpath = utils.relpath(self.root, os.path.abspath(name)).replace(os.sep, '/')
        return utils.popenRead(
            self.root,
            [
                prefs.getString('svk_bin'),
                'cat',
                '-r',
                rev,
                f'{self._getURL(prefs)}/{relpath}'
            ],
            prefs,
            'svk_bash')
