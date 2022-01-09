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
import shlex

from diffuse import utils
from diffuse.preferences import Preferences
from diffuse.vcs.folder_set import FolderSet
from diffuse.vcs.vcs_interface import VcsInterface


# Monotone support
class Mtn(VcsInterface):
    def getFileTemplate(self, prefs: Preferences, name: str) -> VcsInterface.PathRevisionList:
        # FIXME: merge conflicts?
        return [(name, 'h:'), (name, None)]

    def getCommitTemplate(self, prefs, rev, names):
        # build command
        vcs_bin = prefs.getString('mtn_bin')
        lines = utils.popenReadLines(
            self.root,
            [vcs_bin, 'automate', 'select', '-q', rev],
            prefs,
            'mtn_bash')
        if len(lines) != 1:
            raise IOError('Ambiguous revision specifier')
        args = [vcs_bin, 'automate', 'get_revision', lines[0]]
        # build list of interesting files
        fs = FolderSet(names)
        pwd, isabs = os.path.abspath(os.curdir), False
        for name in names:
            isabs |= os.path.isabs(name)
        # run command
        prev = None
        removed, added, modified, renamed = {}, {}, {}, {}
        lines = utils.popenReadLines(self.root, args, prefs, 'mtn_bash')
        i = 0
        while i < len(lines):
            # process results
            line_args = shlex.split(lines[i])
            i += 1
            if len(line_args) < 2:
                continue
            arg, arg1 = line_args[0], line_args[1]
            if arg == 'old_revision' and len(arg1) > 2:
                if prev is not None:
                    break
                prev = arg1[1:-1]
                continue
            if prev is None:
                continue
            if arg == 'delete':
                # deleted file
                k = os.path.join(self.root, prefs.convertToNativePath(arg1))
                if fs.contains(k):
                    removed[arg1] = k
            elif arg == 'add_file':
                # new file
                k = os.path.join(self.root, prefs.convertToNativePath(arg1))
                if fs.contains(k):
                    added[arg1] = k
            elif arg == 'patch':
                # modified file
                k = os.path.join(self.root, prefs.convertToNativePath(arg1))
                if fs.contains(k):
                    modified[arg1] = k
            elif arg == 'rename':
                line_args = shlex.split(lines[i])
                i += 1
                if len(line_args) > 1 and line_args[0] == 'to':
                    # renamed file
                    k0 = os.path.join(self.root, prefs.convertToNativePath(arg1))
                    k1 = os.path.join(self.root, prefs.convertToNativePath(line_args[1]))
                    if fs.contains(k0) or fs.contains(k1):
                        renamed[line_args[1]] = (arg1, k0, k1)
        if removed or renamed:
            # remove directories
            removed_dirs = set()
            lines = utils.popenReadLines(
                self.root,
                [vcs_bin, 'automate', 'get_manifest_of', prev],
                prefs,
                'mtn_bash'
            )
            for line in lines:
                line_args = shlex.split(line)
                if len(line_args) > 1 and line_args[0] == 'dir':
                    removed_dirs.add(line_args[1])
            for k in removed_dirs:
                for m in removed, modified:
                    if k in m:
                        del m[k]
            for k, v in renamed.items():
                arg1, k0, k1 = v
                if arg1 in removed_dirs:
                    del renamed[k]
        # sort results
        result, r = [], set()
        for m in removed, added, modified, renamed:
            r.update(m)
        for k in sorted(r):
            if k in removed:
                k = removed[k]
                if not isabs:
                    k = utils.relpath(pwd, k)
                result.append([(k, prev), (None, None)])
            elif k in added:
                k = added[k]
                if not isabs:
                    k = utils.relpath(pwd, k)
                result.append([(None, None), (k, rev)])
            else:
                if k in renamed:
                    arg1, k0, k1 = renamed[k]
                else:
                    k0 = k1 = modified[k]
                if not isabs:
                    k0 = utils.relpath(pwd, k0)
                    k1 = utils.relpath(pwd, k1)
                result.append([(k0, prev), (k1, rev)])
        return result

    def getFolderTemplate(self, prefs, names):
        fs = FolderSet(names)
        result = []
        pwd, isabs = os.path.abspath(os.curdir), False
        args = [
            prefs.getString('mtn_bin'),
            'automate',
            'inventory',
            '--no-ignored',
            '--no-unchanged',
            '--no-unknown'
        ]
        for name in names:
            isabs |= os.path.isabs(name)
        # build list of interesting files
        prev = 'h:'
        ss = utils.popenReadLines(self.root, args, prefs, 'mtn_bash')
        removed, added, modified, renamed = {}, {}, {}, {}
        i = 0
        while i < len(ss):
            # parse properties
            m = {}
            while i < len(ss):
                s = ss[i]
                i += 1
                # properties are terminated by a blank line
                s = shlex.split(s)
                if len(s) == 0:
                    break
                m[s[0]] = s[1:]
            # scan the list of properties for files that interest us
            if len(m.get('path', [])) > 0:
                p, s, processed = m['path'][0], m.get('status', []), False
                if 'dropped' in s and 'file' in m.get('old_type', []):
                    # deleted file
                    k = os.path.join(self.root, prefs.convertToNativePath(p))
                    if fs.contains(k):
                        if not isabs:
                            k = utils.relpath(pwd, k)
                        removed[k] = [(k, prev), (None, None)]
                    processed = True
                if 'added' in s and 'file' in m.get('new_type', []):
                    # new file
                    k = os.path.join(self.root, prefs.convertToNativePath(p))
                    if fs.contains(k):
                        if not isabs:
                            k = utils.relpath(pwd, k)
                        added[k] = [(None, None), (k, None)]
                    processed = True
                if (
                    'rename_target' in s and
                    'file' in m.get('new_type', []) and
                    len(m.get('old_path', [])) > 0
                ):
                    # renamed file
                    k0 = os.path.join(self.root, prefs.convertToNativePath(m['old_path'][0]))
                    k1 = os.path.join(self.root, prefs.convertToNativePath(p))
                    if fs.contains(k0) or fs.contains(k1):
                        if not isabs:
                            k0 = utils.relpath(pwd, k0)
                            k1 = utils.relpath(pwd, k1)
                        renamed[k1] = [(k0, prev), (k1, None)]
                    processed = True
                if not processed and 'file' in m.get('fs_type', []):
                    # modified file or merge conflict
                    k = os.path.join(self.root, prefs.convertToNativePath(p))
                    if fs.contains(k):
                        if not isabs:
                            k = utils.relpath(pwd, k)
                        modified[k] = [(k, prev), (k, None)]
        # sort the results
        r = set()
        for m in removed, added, modified, renamed:
            r.update(m.keys())
        for k in sorted(r):
            for m in removed, added, modified, renamed:
                if k in m:
                    result.append(m[k])
        return result

    def getRevision(self, prefs: Preferences, name: str, rev: str) -> bytes:
        return utils.popenRead(
            self.root,
            [
                prefs.getString('mtn_bin'),
                'automate',
                'get_file_of',
                '-q',
                '-r',
                rev,
                utils.safeRelativePath(self.root, name, prefs, 'mtn_cygwin')
            ],
            prefs,
            'mtn_bash')
