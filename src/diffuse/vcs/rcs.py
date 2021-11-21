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
from diffuse.vcs.vcs_interface import VcsInterface

# RCS support
class Rcs(VcsInterface):
    def getFileTemplate(self, prefs, name):
        args = [
            prefs.getString('rcs_bin_rlog'),
            '-L',
            '-h',
            utils.safeRelativePath(self.root, name, prefs, 'rcs_cygwin')
        ]
        rev = ''
        for line in utils.popenReadLines(self.root, args, prefs, 'rcs_bash'):
            if line.startswith('head: '):
                rev = line[6:]
        return [ (name, rev), (name, None) ]

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

    # simulate use of popen with xargs to read the output of a command
    def _popen_xargs_readlines(self, cmd, args, prefs, bash_pref):
        # os.sysconf() is only available on Unix
        if hasattr(os, 'sysconf'):
            maxsize = os.sysconf('SC_ARG_MAX')
            maxsize -= sum([ len(k) + len(v) + 2 for k, v in os.environ.items() ])
        else:
            # assume the Window's limit to CreateProcess()
            maxsize = 32767
        maxsize -= sum([ len(k) + 1 for k in cmd ])

        ss = []
        i, s, a = 0, 0, []
        while i < len(args):
            f = (len(a) == 0)
            if f:
                # start a new command line
                a = cmd[:]
            elif s + len(args[i]) + 1 <= maxsize:
                f = True
            if f:
                # append another argument to the current command line
                a.append(args[i])
                s += len(args[i]) + 1
                i += 1
            if i == len(args) or not f:
                ss.extend(utils.popenReadLines(self.root, a, prefs, bash_pref))
                s, a = 0, []
        return ss

    def getFolderTemplate(self, prefs, names):
        # build command
        cmd = [ prefs.getString('rcs_bin_rlog'), '-L', '-h' ]
        # build list of interesting files
        pwd, isabs = os.path.abspath(os.curdir), False
        r = []
        for k in names:
            if os.path.isdir(k):
                # the user specified a folder
                n, ex = [ k ], True
                while len(n) > 0:
                    s = n.pop()
                    recurse = os.path.isdir(os.path.join(s, 'RCS'))
                    if ex or recurse:
                        ex = False
                        for d in os.listdir(s):
                            dn = os.path.join(s, d)
                            if d.endswith(',v') and os.path.isfile(dn):
                                # map to checkout name
                                r.append(dn[:-2])
                            elif d == 'RCS' and os.path.isdir(dn):
                                for v in os.listdir(dn):
                                    if os.path.isfile(os.path.join(dn, v)):
                                        if v.endswith(',v'):
                                            v = v[:-2]
                                        r.append(os.path.join(s, v))
                            elif recurse and os.path.isdir(dn) and not os.path.islink(dn):
                                n.append(dn)
            else:
                # the user specified a file
                s = k + ',v'
                if os.path.isfile(s):
                    r.append(k)
                    continue
                s = k.split(os.sep)
                s.insert(-1, 'RCS')
                # old-style RCS repository
                if os.path.isfile(os.sep.join(s)):
                    r.append(k)
                    continue
                # new-style RCS repository
                s[-1] += ',v'
                if os.path.isfile(os.sep.join(s)):
                    r.append(k)
        for k in r:
            isabs |= os.path.isabs(k)
        args = [ utils.safeRelativePath(self.root, k, prefs, 'rcs_cygwin') for k in r ]
        # run command
        r, k = {}, ''
        for line in self._popen_xargs_readlines(cmd, args, prefs, 'rcs_bash'):
            # parse response
            if line.startswith('Working file: '):
                k = prefs.convertToNativePath(line[14:])
                k = os.path.join(self.root, os.path.normpath(k))
                if not isabs:
                    k = utils.relpath(pwd, k)
            elif line.startswith('head: '):
                r[k] = line[6:]
        # sort the results
        return [ [ (k, r[k]), (k, None) ] for k in sorted(r.keys()) ]

    def getRevision(self, prefs, name, rev):
        return utils.popenRead(
            self.root,
            [
                prefs.getString('rcs_bin_co'),
                '-p',
                '-q',
                '-r' + rev,
                utils.safeRelativePath(self.root, name, prefs, 'rcs_cygwin')
            ],
            prefs,
            'rcs_bash')
