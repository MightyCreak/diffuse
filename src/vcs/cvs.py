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

# CVS support
class Cvs(VcsInterface):
    def getFileTemplate(self, prefs, name):
        return [ (name, 'BASE'), (name, None) ]

    def getCommitTemplate(self, prefs, rev, names):
        result = []
        try:
            r, prev = rev.split('.'), None
            if len(r) > 1:
                m = int(r.pop())
                if m > 1:
                    r.append(str(m - 1))
                else:
                    m = int(r.pop())
                if len(r):
                    prev = '.'.join(r)
            for k in sorted(names):
                 if prev is None:
                     k0 = None
                 else:
                     k0 = k
                 result.append([ (k0, prev), (k, rev) ])
        except ValueError:
            utils.logError(_('Error parsing revision %s.') % (rev, ))
        return result

    def getFolderTemplate(self, prefs, names):
        # build command
        args = [ prefs.getString('cvs_bin'), '-nq', 'update', '-R' ]
        # build list of interesting files
        pwd, isabs = os.path.abspath(os.curdir), False
        for name in names:
            isabs |= os.path.isabs(name)
            args.append(utils.safeRelativePath(self.root, name, prefs, 'cvs_cygwin'))
        # run command
        prev = 'BASE'
        fs = FolderSet(names)
        modified = {}
        for s in utils.popenReadLines(self.root, args, prefs, 'cvs_bash'):
            # parse response
            if len(s) < 3 or s[0] not in 'ACMR':
                continue
            k = os.path.join(self.root, prefs.convertToNativePath(s[2:]))
            if fs.contains(k):
                if not isabs:
                    k = utils.relpath(pwd, k)
                if s[0] == 'R':
                    # removed
                    modified[k] = [ (k, prev), (None, None) ]
                    pass
                elif s[0] == 'A':
                    # added
                    modified[k] = [ (None, None), (k, None) ]
                else:
                    # modified
                    modified[k] = [ (k, prev), (k, None) ]
        # sort the results
        return [ modified[k] for k in sorted(modified.keys()) ]

    def getRevision(self, prefs, name, rev):
        if rev == 'BASE' and not os.path.exists(name):
            # find revision for removed files
            for s in utils.popenReadLines(
                self.root,
                [
                    prefs.getString('cvs_bin'),
                    'status',
                    utils.safeRelativePath(self.root, name, prefs, 'cvs_cygwin')
                ],
                prefs,
                'cvs_bash'):
                if s.startswith('   Working revision:\t-'):
                    rev = s.split('\t')[1][1:]
        return utils.popenRead(
            self.root,
            [
                prefs.getString('cvs_bin'),
                '-Q',
                'update',
                '-p',
                '-r',
                rev,
                utils.safeRelativePath(self.root, name, prefs, 'cvs_cygwin')
            ],
            prefs,
            'cvs_bash')
