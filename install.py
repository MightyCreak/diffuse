#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2009-2010 Derrick Moser <derrick_moser@yahoo.com>
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the licence, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  You may also obtain a copy of the GNU General Public License
# from the Free Software Foundation by visiting their web site
# (http://www.fsf.org/) or by writing to the Free Software Foundation, Inc.,
# 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import glob
import os
import stat
import subprocess
import sys

app_path = sys.argv[0]

# print a message to stderr
def logError(s):
    sys.stderr.write(f'{app_path}: {s}\n')

# this install script should not be used on Windows
if os.name == 'nt':
    logError('Wrong platform.  Use scripts from the "windows-installer" directory instead.')
    sys.exit(1)

# reset the umask so files we create will have the expected permissions
os.umask(stat.S_IWGRP | stat.S_IWOTH)

# option defaults
options = { 'destdir': '/',
            'prefix': '/usr/local/',
            'sysconfdir': '/etc/',
            'examplesdir': '${sysconfdir}',
            'mandir': '${prefix}/share/man/',
            'pythonbin': '/usr/bin/env python' }
install = True
files_only = False

# process --help option
if len(sys.argv) == 2 and sys.argv[1] == '--help':
    print(f"""Usage: {app_path} [OPTION...]

Install or remove Diffuse.

Options:
  --help
     print this help text and quit

  --remove
     remove the program

  --destdir=PATH
     path to the installation's root directory
     default: {options['destdir']}

  --prefix=PATH
     common installation prefix for files
     default: {options['prefix']}

  --sysconfdir=PATH
     directory for installing read-only single-machine data
     default: {options['sysconfdir']}

  --examplesdir=PATH
     directory for example configuration files
     default: {options['examplesdir']}

  --mandir=PATH
     directory for man pages
     default: {options['mandir']}

  --pythonbin=PATH
     command for python interpreter
     default: {options['pythonbin']}

  --files-only
     only install/remove files; skip the post install/removal tasks""")
    sys.exit(0)
 
# returns the list of components used in a path
def components(s):
    return [ p for p in s.split(os.sep) if p != '' ]

# returns a relative path from 'src' to 'dst'
def relpath(src, dst):
    s1, s2, i = components(src), components(dst), 0
    while i < len(s1) and i < len(s2) and s1[i] == s2[i]:
        i += 1
    s = [ os.pardir ] * (len(s1) - i)
    s.extend(s2[i:])
    return os.sep.join(s)

# apply a set of text substitution rules on a string
def replace(s, rules, i=0):
    if i < len(rules):
        k, v = rules[i]
        a = s.split(k)
        for j in range(len(a)):
            a[j] = replace(a[j], rules, i + 1)
        s = v.join(a)
    return s

# create directories
def createDirs(d):
    p = os.sep
    for c in components(d):
        p = os.path.join(p, c)
        if not os.path.isdir(p):
            os.mkdir(p)

# remove a file
def removeFile(f):
    try:
        os.unlink(f)
    except OSError:
        logError(f'Error removing "{f}".')

# install/remove sets of files
def processFiles(install, dst, src, template):
    for k, v in template.items():
        for s in glob.glob(os.path.join(src, k)):
            d = s.replace(src, dst, 1)
            if install:
                createDirs(os.path.dirname(d))
                # install file
                f = open(s, 'rb')
                c = f.read()
                f.close()
                if v is not None:
                    c = replace(c, v)
                print(f'Installing {d}')
                f = open(d, 'wb')
                f.write(c)
                f.close()
                if k == 'bin/diffuse':
                    # turn on the execute bits
                    os.chmod(d, 0o755)
            else:
                # remove file
                removeFile(d)

# compile .po files and install
def processTranslations(install, dst):
    for s in glob.glob('translations/*.po'):
        lang = s[13:-3]
        d = os.path.join(dst, f'share/locale/{lang}/LC_MESSAGES/diffuse.mo')
        if install:
            # install file
            try:
                print(f'Installing {d}')
                createDirs(os.path.dirname(d))
                if subprocess.Popen(['msgfmt', '-o', d, s]).wait() != 0:
                    raise OSError()
            except OSError:
                logError(f'WARNING: Failed to compile "{lang}" localisation.')
        else:
            # remove file
            removeFile(d)

# parse command line arguments
for arg in sys.argv[1:]:
    if arg == '--remove':
        install = False
    elif arg == '--files-only':
        files_only = True
    else:
        for opt in options.keys():
            key = f'--{opt}='
            if arg.startswith(key):
                options[opt] = arg[len(key):]
                break
        else:
            logError(f'Unknown option "{arg}".')
            sys.exit(1)

# expand variables
for s in 'sysconfdir', 'examplesdir', 'mandir':
    for k in 'prefix', 'sysconfdir':
        if s != k:
            options[s] = options[s].replace(f'${{{k}}}', options[k])

# validate inputs
if options['destdir'] == '':
    options['destdir'] = '/'
for opt in 'prefix', 'sysconfdir', 'examplesdir', 'mandir':
    p = options[opt]
    c = components(p)
    if os.pardir in c or os.curdir in c:
        logError(f'Bad value for option "{opt}".')
        sys.exit(1)
    c.insert(0, '')
    c.append('')
    options[opt] = os.sep.join(c)

destdir = options['destdir']
prefix = options['prefix']
sysconfdir = options['sysconfdir']
examplesdir = options['examplesdir']
mandir = options['mandir']
pythonbin = options['pythonbin']

# tell the user what we are about to do
if install:
    stage = 'install'
else:
    stage = 'removal'
print(f'''Performing {stage} with:
    destdir={destdir}
    prefix={prefix}
    sysconfdir={sysconfdir}
    examplesdir={examplesdir}
    mandir={mandir}
    pythonbin={pythonbin}''')

# install files to prefix
processFiles(install, os.path.join(destdir, prefix[1:]), 'src/usr/', {
        'bin/diffuse': [ (b"'../../etc/diffuserc'", repr(relpath(os.path.join(prefix, 'bin'), os.path.join(sysconfdir, 'diffuserc'))).encode()),
            (b'/usr/bin/env python', pythonbin.encode()) ],
        'share/applications/diffuse.desktop': None,
        'share/diffuse/syntax/*.syntax': None,
        'share/gnome/help/diffuse/*/diffuse.xml': [ (b'/usr/', prefix.encode()), (b'/etc/', sysconfdir.encode()) ],
        'share/omf/diffuse/diffuse-*.omf': [ (b'/usr/', prefix.encode()) ],
        'share/icons/hicolor/*/apps/diffuse.png': None
    })

# install manual
processFiles(install, os.path.join(destdir, mandir[1:]), 'src/usr/share/man/', {
        'man1/diffuse.1': [ (b'/usr/', prefix.encode()), (b'/etc/', sysconfdir.encode()) ],
        '*/man1/diffuse.1': [ (b'/usr/', prefix.encode()), (b'/etc/', sysconfdir.encode()) ]
    })

# install files to sysconfdir
processFiles(install, os.path.join(destdir, examplesdir[1:]), 'src/etc/', { 'diffuserc': [ (b'/etc/', sysconfdir.encode()),
    (b'../usr', relpath(sysconfdir, prefix).encode()) ] })

# install translations
processTranslations(install, os.path.join(destdir, prefix[1:]))

if not install:
    # remove directories we own
    for s in 'share/omf/diffuse', 'share/gnome/help/diffuse/C', 'share/gnome/help/diffuse/ru', 'share/gnome/help/diffuse', 'share/diffuse/syntax', 'share/diffuse':
        d = os.path.join(destdir, os.path.join(prefix, s)[1:])
        try:
            os.rmdir(d)
        except OSError:
            logError(f'Error removing "{d}".')

# do post install/removal tasks
if not files_only:
    print(f'Performing post {stage} tasks.')

    cmds = [ [ 'update-desktop-database' ],
             [ 'gtk-update-icon-cache', os.path.join(destdir, os.path.join(prefix, 'icons/hicolor')[1:]) ] ]
    if install:
        cmds.append([ 'scrollkeeper-update', '-q', '-o', os.path.join(destdir, os.path.join(prefix, 'share/omf/diffuse')[1:]) ])
    else:
        cmds.append([ 'scrollkeeper-update', '-q' ])
    for c in cmds:
        for p in os.environ['PATH'].split(os.pathsep):
            if os.path.exists(os.path.join(p, c[0])):
                print(' '.join(c))
                try:
                    if subprocess.Popen(c).wait() != 0:
                        raise OSError()
                except OSError:
                    logError(f'WARNING: Failed to update documentation database with {c[0]}.')
                break
        else:
            print(f'WARNING: {c[0]} is not installed')
