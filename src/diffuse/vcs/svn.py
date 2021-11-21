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
from diffuse.vcs.folder_set import FolderSet
from diffuse.vcs.vcs_interface import VcsInterface

# Subversion support
# SVK support subclasses from this
class Svn(VcsInterface):
    def __init__(self, root):
        VcsInterface.__init__(self, root)
        self.url = None

    @staticmethod
    def _getVcs():
        return 'svn'

    @staticmethod
    def _getURLPrefix():
        return 'URL: '

    @staticmethod
    def _parseStatusLine(s):
        if len(s) < 8 or s[0] not in 'ACDMR':
            return '', ''
        # subversion 1.6 adds a new column
        k = 7
        if k < len(s) and s[k] == ' ':
            k += 1
        return s[0], s[k:]

    @staticmethod
    def _getPreviousRevision(rev):
        if rev is None:
            return 'BASE'
        m = int(rev)
        return str(max(m > 1, 0))

    def _getURL(self, prefs):
        if self.url is None:
            vcs, prefix = self._getVcs(), self._getURLPrefix()
            n = len(prefix)
            args = [ prefs.getString(vcs + '_bin'), 'info' ]
            for s in utils.popenReadLines(self.root, args, prefs, vcs + '_bash'):
                if s.startswith(prefix):
                    self.url = s[n:]
                    break
        return self.url

    def getFileTemplate(self, prefs, name):
        # FIXME: verify this
        # merge conflict
        escaped_name = utils.globEscape(name)
        left = glob.glob(escaped_name + '.merge-left.r*')
        right = glob.glob(escaped_name + '.merge-right.r*')
        if len(left) > 0 and len(right) > 0:
            return [ (left[-1], None), (name, None), (right[-1], None) ]
        # update conflict
        left = sorted(glob.glob(escaped_name + '.r*'))
        right = glob.glob(escaped_name + '.mine')
        right.extend(glob.glob(escaped_name + '.working'))
        if len(left) > 0 and len(right) > 0:
            return [ (left[-1], None), (name, None), (right[0], None) ]
        # default case
        return [ (name, self._getPreviousRevision(None)), (name, None) ]

    def _getCommitTemplate(self, prefs, rev, names):
        result = []
        try:
            prev = self._getPreviousRevision(rev)
        except ValueError:
            utils.logError(_('Error parsing revision %s.') % (rev, ))
            return result

        # build command
        vcs = self._getVcs()
        vcs_bin, vcs_bash = prefs.getString(vcs + '_bin'), vcs + '_bash'
        if rev is None:
            args = [ vcs_bin, 'status', '-q' ]
        else:
            args = [ vcs_bin, 'diff', '--summarize', '-c', rev ]
        # build list of interesting files
        pwd, isabs = os.path.abspath(os.curdir), False
        for name in names:
            isabs |= os.path.isabs(name)
            if rev is None:
                args.append(utils.safeRelativePath(self.root, name, prefs, vcs + '_cygwin'))
        # run command
        fs = FolderSet(names)
        modified, added, removed = {}, set(), set()
        for s in utils.popenReadLines(self.root, args, prefs, vcs_bash):
            status = self._parseStatusLine(s)
            if status is None:
                continue
            v, k = status
            rel = prefs.convertToNativePath(k)
            k = os.path.join(self.root, rel)
            if fs.contains(k):
                if v == 'D':
                    # deleted file or directory
                    # the contents of deleted folders are not reported
                    # by "svn diff --summarize -c <rev>"
                    removed.add(rel)
                elif v == 'A':
                    # new file or directory
                    added.add(rel)
                elif v == 'M':
                    # modified file or merge conflict
                    k = os.path.join(self.root, k)
                    if not isabs:
                        k = utils.relpath(pwd, k)
                    modified[k] = [ (k, prev), (k, rev) ]
                elif v == 'C':
                    # merge conflict
                    modified[k] = self.getFileTemplate(prefs, k)
                elif v == 'R':
                    # replaced file
                    removed.add(rel)
                    added.add(rel)
        # look for files in the added items
        if rev is None:
            m, added = added, {}
            for k in m:
                if not os.path.isdir(k):
                    # confirmed as added file
                    k = os.path.join(self.root, k)
                    if not isabs:
                        k = utils.relpath(pwd, k)
                    added[k] = [ (None, None), (k, None) ]
        else:
            m = {}
            for k in added:
                d, b = os.path.dirname(k), os.path.basename(k)
                if d not in m:
                    m[d] = set()
                m[d].add(b)
            # remove items we can easily determine to be directories
            for k in m:
                d = os.path.dirname(k)
                if d in m:
                    m[d].discard(os.path.basename(k))
                    if not m[d]:
                        del m[d]
            # determine which are directories
            added = {}
            for p, v in m.items():
                lines = utils.popenReadLines(
                    self.root,
                    [
                        vcs_bin,
                        'list',
                        '-r',
                        rev,
                        f"{self._getURL(prefs)}/{p.replace(os.sep, '/')}"
                    ],
                    prefs,
                    vcs_bash)
                for s in lines:
                    if s in v:
                        # confirmed as added file
                        k = os.path.join(self.root, os.path.join(p, s))
                        if not isabs:
                            k = utils.relpath(pwd, k)
                        added[k] = [ (None, None), (k, rev) ]
        # determine if removed items are files or directories
        if prev == 'BASE':
            m, removed = removed, {}
            for k in m:
                if not os.path.isdir(k):
                    # confirmed item as file
                    k = os.path.join(self.root, k)
                    if not isabs:
                        k = utils.relpath(pwd, k)
                    removed[k] = [ (k, prev), (None, None) ]
        else:
            m = {}
            for k in removed:
                d, b = os.path.dirname(k), os.path.basename(k)
                if d not in m:
                    m[d] = set()
                m[d].add(b)
            removed_dir, removed = set(), {}
            for p, v in m.items():
                lines = utils.popenReadLines(
                    self.root,
                    [
                        vcs_bin,
                        'list',
                        '-r',
                        prev,
                        f"{self._getURL(prefs)}/{p.replace(os.sep, '/')}"
                    ],
                    prefs,
                    vcs_bash)
                for s in lines:
                    if s.endswith('/'):
                        s = s[:-1]
                        if s in v:
                            # confirmed item as directory
                            removed_dir.add(os.path.join(p, s))
                    else:
                        if s in v:
                            # confirmed item as file
                            k = os.path.join(self.root, os.path.join(p, s))
                            if not isabs:
                                k = utils.relpath(pwd, k)
                            removed[k] = [ (k, prev), (None, None) ]
            # recursively find all unreported removed files
            while removed_dir:
                tmp = removed_dir
                removed_dir = set()
                for p in tmp:
                    lines = utils.popenReadLines(
                        self.root,
                        [
                            vcs_bin,
                            'list',
                            '-r',
                            prev,
                            f"{self._getURL(prefs)}/{p.replace(os.sep, '/')}"
                        ],
                        prefs,
                        vcs_bash)
                    for s in lines:
                        if s.endswith('/'):
                            # confirmed item as directory
                            removed_dir.add(os.path.join(p, s[:-1]))
                        else:
                            # confirmed item as file
                            k = os.path.join(self.root, os.path.join(p, s))
                            if not isabs:
                                k = utils.relpath(pwd, k)
                            removed[k] = [ (k, prev), (None, None) ]
        # sort the results
        r = set()
        for m in removed, added, modified:
            r.update(m.keys())
        for k in sorted(r):
            for m in removed, added, modified:
                if k in m:
                    result.append(m[k])
        return result

    def getCommitTemplate(self, prefs, rev, names):
        return self._getCommitTemplate(prefs, rev, names)

    def getFolderTemplate(self, prefs, names):
        return self._getCommitTemplate(prefs, None, names)

    def getRevision(self, prefs, name, rev):
        vcs_bin = prefs.getString('svn_bin')
        if rev in [ 'BASE', 'COMMITTED', 'PREV' ]:
            return utils.popenRead(
                self.root,
                [
                    vcs_bin,
                    'cat',
                    f"{utils.safeRelativePath(self.root, name, prefs, 'svn_cygwin')}@{rev}"
                ],
                prefs,
                'svn_bash')
        return utils.popenRead(
            self.root,
            [
                vcs_bin,
                'cat',
                (
                    f"{self._getURL(prefs)}/"
                    f"{utils.relpath(self.root, os.path.abspath(name)).replace(os.sep, '/')}@{rev}"
                )
            ],
            prefs,
            'svn_bash')
