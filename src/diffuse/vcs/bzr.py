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


# Bazaar support
class Bzr(VcsInterface):
    def getFileTemplate(self, prefs, name):
        # merge conflict
        left = name + '.OTHER'
        right = name + '.THIS'
        if os.path.isfile(left) and os.path.isfile(right):
            return [(left, None), (name, None), (right, None)]
        # default case
        return [(name, '-1'), (name, None)]

    def getCommitTemplate(self, prefs, rev, names):
        # build command
        args = [prefs.getString('bzr_bin'), 'log', '-v', '-r', rev]
        # build list of interesting files
        pwd, isabs = os.path.abspath(os.curdir), False
        for name in names:
            isabs |= os.path.isabs(name)
            args.append(utils.safeRelativePath(self.root, name, prefs, 'bzr_cygwin'))
        # run command
        ss = utils.popenReadLines(self.root, args, prefs, 'bzr_bash')
        # parse response
        prev = 'before:' + rev
        fs = FolderSet(names)
        added, modified, removed, renamed = {}, {}, {}, {}
        i, n = 0, len(ss)
        while i < n:
            s = ss[i]
            i += 1
            if s.startswith('added:'):
                # added files
                while i < n and ss[i].startswith('  '):
                    k = prefs.convertToNativePath(ss[i][2:])
                    i += 1
                    if not k.endswith(os.sep):
                        k = os.path.join(self.root, k)
                        if fs.contains(k):
                            if not isabs:
                                k = utils.relpath(pwd, k)
                            added[k] = [(None, None), (k, rev)]
            elif s.startswith('modified:'):
                # modified files
                while i < n and ss[i].startswith('  '):
                    k = prefs.convertToNativePath(ss[i][2:])
                    i += 1
                    if not k.endswith(os.sep):
                        k = os.path.join(self.root, k)
                        if fs.contains(k):
                            if not isabs:
                                k = utils.relpath(pwd, k)
                            modified[k] = [(k, prev), (k, rev)]
            elif s.startswith('removed:'):
                # removed files
                while i < n and ss[i].startswith('  '):
                    k = prefs.convertToNativePath(ss[i][2:])
                    i += 1
                    if not k.endswith(os.sep):
                        k = os.path.join(self.root, k)
                        if fs.contains(k):
                            if not isabs:
                                k = utils.relpath(pwd, k)
                            removed[k] = [(k, prev), (None, None)]
            elif s.startswith('renamed:'):
                # renamed files
                while i < n and ss[i].startswith('  '):
                    k = ss[i][2:].split(' => ')
                    i += 1
                    if len(k) == 2:
                        k0 = prefs.convertToNativePath(k[0])
                        k1 = prefs.convertToNativePath(k[1])
                        if not k0.endswith(os.sep) and not k1.endswith(os.sep):
                            k0 = os.path.join(self.root, k0)
                            k1 = os.path.join(self.root, k1)
                            if fs.contains(k0) or fs.contains(k1):
                                if not isabs:
                                    k0 = utils.relpath(pwd, k0)
                                    k1 = utils.relpath(pwd, k1)
                                renamed[k1] = [(k0, prev), (k1, rev)]
        # sort the results
        result, r = [], set()
        for m in removed, added, modified, renamed:
            r.update(m.keys())
        for k in sorted(r):
            for m in removed, added, modified, renamed:
                if k in m:
                    result.append(m[k])
        return result

    def getFolderTemplate(self, prefs, names):
        # build command
        args = [prefs.getString('bzr_bin'), 'status', '-SV']
        # build list of interesting files
        pwd, isabs = os.path.abspath(os.curdir), False
        for name in names:
            isabs |= os.path.isabs(name)
            args.append(utils.safeRelativePath(self.root, name, prefs, 'bzr_cygwin'))
        # run command
        prev = '-1'
        fs = FolderSet(names)
        added, modified, removed, renamed = {}, {}, {}, {}
        for s in utils.popenReadLines(self.root, args, prefs, 'bzr_bash'):
            # parse response
            if len(s) < 5:
                continue
            y, k = s[1], s[4:]
            if y == 'D':
                # removed
                k = prefs.convertToNativePath(k)
                if not k.endswith(os.sep):
                    k = os.path.join(self.root, k)
                    if fs.contains(k):
                        if not isabs:
                            k = utils.relpath(pwd, k)
                        removed[k] = [(k, prev), (None, None)]
            elif y == 'N':
                # added
                k = prefs.convertToNativePath(k)
                if not k.endswith(os.sep):
                    k = os.path.join(self.root, k)
                    if fs.contains(k):
                        if not isabs:
                            k = utils.relpath(pwd, k)
                        added[k] = [(None, None), (k, None)]
            elif y == 'M':
                # modified or merge conflict
                k = prefs.convertToNativePath(k)
                if not k.endswith(os.sep):
                    k = os.path.join(self.root, k)
                    if fs.contains(k):
                        if not isabs:
                            k = utils.relpath(pwd, k)
                        modified[k] = self.getFileTemplate(prefs, k)
            elif s[0] == 'R':
                # renamed
                k = k.split(' => ')
                if len(k) == 2:
                    k0 = prefs.convertToNativePath(k[0])
                    k1 = prefs.convertToNativePath(k[1])
                    if not k0.endswith(os.sep) and not k1.endswith(os.sep):
                        k0 = os.path.join(self.root, k0)
                        k1 = os.path.join(self.root, k1)
                        if fs.contains(k0) or fs.contains(k1):
                            if not isabs:
                                k0 = utils.relpath(pwd, k0)
                                k1 = utils.relpath(pwd, k1)
                            renamed[k1] = [(k0, prev), (k1, None)]
        # sort the results
        result, r = [], set()
        for m in removed, added, modified, renamed:
            r.update(m.keys())
        for k in sorted(r):
            for m in removed, added, modified, renamed:
                if k in m:
                    result.append(m[k])
        return result

    def getRevision(self, prefs, name, rev):
        return utils.popenRead(
            self.root,
            [
                prefs.getString('bzr_bin'),
                'cat',
                '--name-from-revision',
                '-r',
                rev,
                utils.safeRelativePath(self.root, name, prefs, 'bzr_cygwin')
            ],
            prefs,
            'bzr_bash')
