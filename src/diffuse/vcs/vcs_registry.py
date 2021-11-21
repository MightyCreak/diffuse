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
from diffuse.vcs.bzr import Bzr
from diffuse.vcs.cvs import Cvs
from diffuse.vcs.darcs import Darcs
from diffuse.vcs.git import Git
from diffuse.vcs.hg import Hg
from diffuse.vcs.mtn import Mtn
from diffuse.vcs.rcs import Rcs
from diffuse.vcs.svk import Svk
from diffuse.vcs.svn import Svn

class VcsRegistry:
    def __init__(self):
        # initialise the VCS objects
        self._get_repo = {
            'bzr': _get_bzr_repo,
            'cvs': _get_cvs_repo,
            'darcs': _get_darcs_repo,
            'git': _get_git_repo,
            'hg': _get_hg_repo,
            'mtn': _get_mtn_repo,
            'rcs': _get_rcs_repo,
            'svk': _get_svk_repo,
            'svn': _get_svn_repo
        }

    # determines which VCS to use for files in the named folder
    def findByFolder(self, path, prefs):
        path = os.path.abspath(path)
        for vcs in prefs.getString('vcs_search_order').split():
            if vcs in self._get_repo:
                repo = self._get_repo[vcs](path, prefs)
                if repo:
                    return repo
        return None

    # determines which VCS to use for the named file
    def findByFilename(self, name, prefs):
        if name is not None:
            return self.findByFolder(os.path.dirname(name), prefs)
        return None


# utility method to help find folders used by version control systems
def _find_parent_dir_with(path, dir_name):
    while True:
        name = os.path.join(path, dir_name)
        if os.path.isdir(name):
            return path
        newpath = os.path.dirname(path)
        if newpath == path:
            break
        path = newpath

def _get_bzr_repo(path, prefs):
    p = _find_parent_dir_with(path, '.bzr')
    return Bzr(p) if p else None

def _get_cvs_repo(path, prefs):
    return Cvs(path) if os.path.isdir(os.path.join(path, 'CVS')) else None

def _get_darcs_repo(path, prefs):
    p = _find_parent_dir_with(path, '_darcs')
    return Darcs(p) if p else None

def _get_git_repo(path, prefs):
    if 'GIT_DIR' in os.environ:
        try:
            d = path
            ss = utils.popenReadLines(
                d,
                [
                    prefs.getString('git_bin'),
                    'rev-parse',
                    '--show-prefix'
                ],
                prefs,
                'git_bash')
            if len(ss) > 0:
                # be careful to handle trailing slashes
                d = d.split(os.sep)
                if d[-1] != '':
                    d.append('')
                ss = utils.strip_eol(ss[0]).split('/')
                if ss[-1] != '':
                    ss.append('')
                n = len(ss)
                if n <= len(d):
                    del d[-n:]
                if len(d) == 0:
                    d = os.curdir
                else:
                    d = os.sep.join(d)
            return Git(d)
        except (IOError, OSError):
            # working tree not found
            pass
    # search for .git directory (project) or .git file (submodule)
    while True:
        name = os.path.join(path, '.git')
        if os.path.isdir(name) or os.path.isfile(name):
            return Git(path)
        newpath = os.path.dirname(path)
        if newpath == path:
            break
        path = newpath

def _get_hg_repo(path, prefs):
    p = _find_parent_dir_with(path, '.hg')
    return Hg(p) if p else None

def _get_mtn_repo(path, prefs):
    p = _find_parent_dir_with(path, '_MTN')
    return Mtn(p) if p else None

def _get_rcs_repo(path, prefs):
    if os.path.isdir(os.path.join(path, 'RCS')):
        return Rcs(path)

    # [rfailliot] this code doesn't seem to work, but was in 0.4.8 too.
    # I'm letting it here until further tests are done, but it is possible
    # this code never actually worked.
    try:
        for s in os.listdir(path):
            if s.endswith(',v') and os.path.isfile(os.path.join(path, s)):
                return Rcs(path)
    except OSError:
        # the user specified an invalid folder name
        pass
    return None

def _get_svn_repo(path, prefs):
    p = _find_parent_dir_with(path, '.svn')
    return Svn(p) if p else None

def _get_svk_repo(path, prefs):
    name = path
    # parse the ~/.svk/config file to discover which directories are part of
    # SVK repositories
    if utils.isWindows():
        name = name.upper()
    svkroot = os.environ.get('SVKROOT', None)
    if svkroot is None:
        svkroot = os.path.expanduser('~/.svk')
    svkconfig = os.path.join(svkroot, 'config')
    if os.path.isfile(svkconfig):
        try:
            # find working copies by parsing the config file
            with open(svkconfig, 'r', encoding='utf-8') as f:
                ss = utils.readlines(f)
            projs, sep = [], os.sep
            # find the separator character
            for s in ss:
                if s.startswith('  sep: ') and len(s) > 7:
                    sep = s[7]
            # find the project directories
            i = 0
            while i < len(ss):
                s = ss[i]
                i += 1
                if s.startswith('  hash: '):
                    while i < len(ss) and ss[i].startswith('    '):
                        s = ss[i]
                        i += 1
                        if (
                            s.endswith(': ') and
                            i < len(ss) and
                            ss[i].startswith('      depotpath: ')
                        ):
                            key = s[4:-2].replace(sep, os.sep)
                            # parse directory path
                            j, n, tt = 0, len(key), []
                            while j < n:
                                if key[j] == '"':
                                    # quoted string
                                    j += 1
                                    while j < n:
                                        if key[j] == '"':
                                            j += 1
                                            break
                                        if key[j] == '\\':
                                            # escaped character
                                            j += 1
                                        if j < n:
                                            tt.append(key[j])
                                            j += 1
                                else:
                                    tt.append(key[j])
                                    j += 1
                            key = ''.join(tt).replace(sep, os.sep)
                            if utils.isWindows():
                                key = key.upper()
                            projs.append(key)
                    break
            # check if the file belongs to one of the project directories
            if FolderSet(projs).contains(name):
                return Svk(path)
        except IOError:
            utils.logError(_('Error parsing %s.') % (svkconfig, ))
    return None
