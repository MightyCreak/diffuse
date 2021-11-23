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

from diffuse import utils
from diffuse.vcs.folder_set import FolderSet
from diffuse.vcs.vcs_interface import VcsInterface


# Git support
class Git(VcsInterface):
    def getFileTemplate(self, prefs, name):
        return [(name, 'HEAD'), (name, None)]

    def getCommitTemplate(self, prefs, rev, names):
        # build command
        args = [prefs.getString('git_bin'), 'show', '--pretty=format:', '--name-status', rev]
        # build list of interesting files
        pwd = os.path.abspath(os.curdir)
        isabs = False
        for name in names:
            isabs |= os.path.isabs(name)
        # run command
        prev = rev + '^'
        fs = FolderSet(names)
        modified = {}
        for s in utils.popenReadLines(self.root, args, prefs, 'git_bash'):
            # parse response
            if len(s) < 2 or s[0] not in 'ADM':
                continue
            k = self._extractPath(s[2:], prefs)
            if fs.contains(k):
                if not isabs:
                    k = utils.relpath(pwd, k)
                if s[0] == 'D':
                    # removed
                    modified[k] = [(k, prev), (None, None)]
                elif s[0] == 'A':
                    # added
                    modified[k] = [(None, None), (k, rev)]
                else:
                    # modified
                    modified[k] = [(k, prev), (k, rev)]
        # sort the results
        return [modified[k] for k in sorted(modified.keys())]

    def _extractPath(self, s, prefs):
        return os.path.join(self.root, prefs.convertToNativePath(s.strip()))

    def getFolderTemplate(self, prefs, names):
        # build command
        args = [
            prefs.getString('git_bin'),
            'status',
            '--porcelain',
            '-s',
            '--untracked-files=no',
            '--ignore-submodules=all'
        ]
        # build list of interesting files
        pwd = os.path.abspath(os.curdir)
        isabs = False
        for name in names:
            isabs |= os.path.isabs(name)
        # run command
        prev = 'HEAD'
        fs = FolderSet(names)
        modified, renamed = {}, {}
        # 'git status' will return 1 when a commit would fail
        for s in utils.popenReadLines(self.root, args, prefs, 'git_bash', [0, 1]):
            # parse response
            if len(s) < 3:
                continue
            x, y, k = s[0], s[1], s[2:]
            if x == 'R':
                # renamed
                k = k.split(' -> ')
                if len(k) == 2:
                    k0 = self._extractPath(k[0], prefs)
                    k1 = self._extractPath(k[1], prefs)
                    if fs.contains(k0) or fs.contains(k1):
                        if not isabs:
                            k0 = utils.relpath(pwd, k0)
                            k1 = utils.relpath(pwd, k1)
                        renamed[k1] = [(k0, prev), (k1, None)]
            elif x == 'U' or y == 'U' or (x == 'D' and y == 'D'):
                # merge conflict
                k = self._extractPath(k, prefs)
                if fs.contains(k):
                    if not isabs:
                        k = utils.relpath(pwd, k)
                    if x == 'D':
                        panes = [(None, None)]
                    else:
                        panes = [(k, ':2')]
                    panes.append((k, None))
                    if y == 'D':
                        panes.append((None, None))
                    else:
                        panes.append((k, ':3'))
                    if x != 'A' and y != 'A':
                        panes.append((k, ':1'))
                    modified[k] = panes
            else:
                k = self._extractPath(k, prefs)
                if fs.contains(k):
                    if not isabs:
                        k = utils.relpath(pwd, k)
                    if x == 'A':
                        # added
                        panes = [(None, None)]
                    else:
                        panes = [(k, prev)]
                    # staged changes
                    if x == 'D':
                        panes.append((None, None))
                    elif x != ' ':
                        panes.append((k, ':0'))
                    # working copy changes
                    if y == 'D':
                        panes.append((None, None))
                    elif y != ' ':
                        panes.append((k, None))
                    modified[k] = panes
        # sort the results
        result, r = [], set()
        for m in modified, renamed:
            r.update(m.keys())
        for k in sorted(r):
            for m in modified, renamed:
                if k in m:
                    result.append(m[k])
        return result

    def getRevision(self, prefs, name, rev):
        relpath = utils.relpath(self.root, os.path.abspath(name)).replace(os.sep, '/')
        return utils.popenRead(
            self.root,
            [
                prefs.getString('git_bin'),
                'show',
                f'{rev}:{relpath}'
            ],
            prefs,
            'git_bash')
