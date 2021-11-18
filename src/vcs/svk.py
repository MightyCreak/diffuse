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
import glob

from diffuse import utils
from diffuse.vcs.svn import Svn

class Svk(Svn):
    def _getVcs(self):
        return 'svk'

    def _getURLPrefix(self):
        return 'Depot Path: '

    def _parseStatusLine(self, s):
        if len(s) < 4 or s[0] not in 'ACDMR':
            return
        return s[0], s[4:]

    def _getPreviousRevision(self, rev):
        if rev is None:
            return 'HEAD'
        if rev.endswith('@'):
            return str(int(rev[:-1]) - 1) + '@'
        return str(int(rev) - 1)

    def getRevision(self, prefs, name, rev):
        return utils.popenRead(
            self.root,
            [
                prefs.getString('svk_bin'),
                'cat',
                '-r',
                rev,
                '{}/{}'.format(
                    self._getURL(prefs),
                    utils.relpath(self.root, os.path.abspath(name)).replace(os.sep, '/'))
            ],
            prefs,
            'svk_bash')
