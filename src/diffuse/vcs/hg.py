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

from typing import Optional

from diffuse import utils
from diffuse.preferences import Preferences
from diffuse.vcs.folder_set import FolderSet
from diffuse.vcs.vcs_interface import VcsInterface


# Mercurial support
class Hg(VcsInterface):
    def __init__(self, root: str):
        super().__init__(root)
        self.working_rev: Optional[str] = None

    def _getPreviousRevision(self, prefs, rev):
        if rev is None:
            if self.working_rev is None:
                ss = utils.popenReadLines(
                    self.root,
                    [prefs.getString('hg_bin'), 'id', '-i', '-t'],
                    prefs,
                    'hg_bash')
                if len(ss) != 1:
                    raise IOError('Unknown working revision')
                ss = ss[0].split(' ')
                prev = ss[-1]
                if len(ss) == 1 and prev.endswith('+'):
                    # remove local modifications indicator
                    prev = prev[:-1]
                self.working_rev = prev
            return self.working_rev
        return f'p1({rev})'

    def getFileTemplate(self, prefs: Preferences, name: str) -> VcsInterface.PathRevisionList:
        return [(name, self._getPreviousRevision(prefs, None)), (name, None)]

    def _getCommitTemplate(self, prefs, names, cmd, rev):
        # build command
        args = [prefs.getString('hg_bin')]
        args.extend(cmd)
        # build list of interesting files
        pwd, isabs = os.path.abspath(os.curdir), False
        for name in names:
            isabs |= os.path.isabs(name)
            args.append(utils.safeRelativePath(self.root, name, prefs, 'hg_cygwin'))
        # run command
        prev = self._getPreviousRevision(prefs, rev)
        if rev is not None:
            if '..' in rev:
                prev, rev = rev.split('..')
                args.extend(['-r',prev,'-r',rev])
            else:
                args.extend(['-r',rev])
        fs = FolderSet(names)
        modified = {}
        for s in utils.popenReadLines(self.root, args, prefs, 'hg_bash'):
            # parse response
            if len(s) < 3 or s[0] not in 'AMR':
                continue
            k = os.path.join(self.root, prefs.convertToNativePath(s[2:]))
            if fs.contains(k):
                if not isabs:
                    k = utils.relpath(pwd, k)
                if s[0] == 'R':
                    # removed
                    modified[k] = [(k, prev), (None, None)]
                elif s[0] == 'A':
                    # added
                    modified[k] = [(None, None), (k, rev)]
                else:
                    # modified or merge conflict
                    modified[k] = [(k, prev), (k, rev)]
        # sort the results
        return [modified[k] for k in sorted(modified.keys())]

    def getCommitTemplate(self, prefs, rev, names):
        return self._getCommitTemplate(
            prefs,
            names,
            ['log', '--template', 'A\t{file_adds}\nM\t{file_mods}\nR\t{file_dels}\n'],
            rev)

    def getFolderTemplate(self, prefs, names):
        return self._getCommitTemplate(prefs, names, ['status', '-q'], None)

    def getRevision(self, prefs: Preferences, name: str, rev: str) -> bytes:
        return utils.popenRead(
            self.root,
            [
                prefs.getString('hg_bin'),
                'cat',
                '-r',
                rev,
                utils.safeRelativePath(self.root, name, prefs, 'hg_cygwin')
            ],
            prefs,
            'hg_bash')
