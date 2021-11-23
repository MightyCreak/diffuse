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


# Darcs support
class Darcs(VcsInterface):
    def getFileTemplate(self, prefs, name):
        return [(name, ''), (name, None)]

    def _getCommitTemplate(self, prefs, names, rev):
        mods = (rev is None)
        # build command
        args = [prefs.getString('darcs_bin')]
        if mods:
            args.extend(['whatsnew', '-s'])
        else:
            args.extend(['log', '--number', '-s'])
            try:
                args.extend(['-n', str(int(rev))])
            except ValueError:
                args.extend(['-h', rev])
        # build list of interesting files
        pwd, isabs = os.path.abspath(os.curdir), False
        for name in names:
            isabs |= os.path.isabs(name)
            if mods:
                args.append(utils.safeRelativePath(self.root, name, prefs, 'darcs_cygwin'))
        # run command
        # 'darcs whatsnew' will return 1 if there are no changes
        ss = utils.popenReadLines(self.root, args, prefs, 'darcs_bash', [0, 1])
        # parse response
        i, n = 0, len(ss)
        if mods:
            prev = ''
            rev = None
        else:
            try:
                rev = ss[0].split(':')[0]
                prev = str(int(rev) + 1)
                # skip to the beginning of the summary
                while i < n and len(ss[i]):
                    i += 1
            except (ValueError, IndexError):
                i = n
        fs = FolderSet(names)
        added, modified, removed, renamed = {}, {}, {}, {}
        while i < n:
            s = ss[i]
            i += 1
            if not mods:
                if s.startswith('    '):
                    s = s[4:]
                else:
                    continue
            if len(s) < 2:
                continue
            x = s[0]
            if x == 'R':
                # removed
                k = prefs.convertToNativePath(s[2:])
                if not k.endswith(os.sep):
                    k = os.path.join(self.root, k)
                    if fs.contains(k):
                        if not isabs:
                            k = utils.relpath(pwd, k)
                        removed[k] = [(k, prev), (None, None)]
            elif x == 'A':
                # added
                k = prefs.convertToNativePath(s[2:])
                if not k.endswith(os.sep):
                    k = os.path.join(self.root, k)
                    if fs.contains(k):
                        if not isabs:
                            k = utils.relpath(pwd, k)
                        added[k] = [(None, None), (k, rev)]
            elif x == 'M':
                # modified
                k = prefs.convertToNativePath(s[2:].split(' ')[0])
                if not k.endswith(os.sep):
                    k = os.path.join(self.root, k)
                    if fs.contains(k):
                        if not isabs:
                            k = utils.relpath(pwd, k)
                        if k not in renamed:
                            modified[k] = [(k, prev), (k, rev)]
            elif x == ' ':
                # renamed
                k = s[1:].split(' -> ')
                if len(k) == 2:
                    k0 = prefs.convertToNativePath(k[0])
                    k1 = prefs.convertToNativePath(k[1])
                    if not k0.endswith(os.sep):
                        k0 = os.path.join(self.root, k0)
                        k1 = os.path.join(self.root, k1)
                        if fs.contains(k0) or fs.contains(k1):
                            if not isabs:
                                k0 = utils.relpath(pwd, k0)
                                k1 = utils.relpath(pwd, k1)
                            renamed[k1] = [(k0, prev), (k1, rev)]
        # sort the results
        result, r = [], set()
        for m in added, modified, removed, renamed:
            r.update(m.keys())
        for k in sorted(r):
            for m in removed, added, modified, renamed:
                if k in m:
                    result.append(m[k])
        return result

    def getCommitTemplate(self, prefs, rev, names):
        return self._getCommitTemplate(prefs, names, rev)

    def getFolderTemplate(self, prefs, names):
        return self._getCommitTemplate(prefs, names, None)

    def getRevision(self, prefs, name, rev):
        args = [prefs.getString('darcs_bin'), 'show', 'contents']
        try:
            args.extend(['-n', str(int(rev))])
        except ValueError:
            args.extend(['-h', rev])
        args.append(utils.safeRelativePath(self.root, name, prefs, 'darcs_cygwin'))
        return utils.popenRead(self.root, args, prefs, 'darcs_bash')
