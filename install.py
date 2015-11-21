#!/usr/bin/env python
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
    sys.stderr.write('%s: %s\n' % (app_path, s))

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
    print """Usage: %s [OPTION...]

Install or remove Diffuse.

Options:
  --help
     print this help text and quit

  --remove
     remove the program

  --destdir=PATH
     path to the installation's root directory
     default: %s

  --prefix=PATH
     common installation prefix for files
     default: %s

  --sysconfdir=PATH
     directory for installing read-only single-machine data
     default: %s

  --examplesdir=PATH
     directory for example configuration files
     default: %s

  --mandir=PATH
     directory for man pages
     default: %s

  --pythonbin=PATH
     command for python interpreter
     default: %s

  --files-only
     only install/remove files; skip the post install/removal tasks""" % (app_path, options['destdir'], options['prefix'], options['sysconfdir'], options['examplesdir'], options['mandir'], options['pythonbin'])
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
        logError('Error removing "%s".' % (f, ))

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
                print 'Installing %s' % (d, )
                f = open(d, 'wb')
                f.write(c)
                f.close()
                if k == 'bin/diffuse':
                    # turn on the execute bits
                    os.chmod(d, 0755)
            else:
                # remove file
                removeFile(d)

# compile .po files and install
def processTranslations(install, dst):
    for s in glob.glob('translations/*.po'):
        lang = s[13:-3]
        d = os.path.join(dst, 'share/locale/%s/LC_MESSAGES/diffuse.mo' % (lang, ))
        if install:
            # install file
            try:
                print 'Installing %s' % (d, )
                createDirs(os.path.dirname(d))
                if subprocess.Popen(['msgfmt', '-o', d, s]).wait() != 0:
                    raise OSError()
            except OSError:
                logError('WARNING: Failed to compile "%s" localisation.' % (lang, ))
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
            key = '--%s=' % (opt, )
            if arg.startswith(key):
                options[opt] = arg[len(key):]
                break
        else:
            logError('Unknown option "%s".' % (arg, ))
            sys.exit(1)

# expand variables
for s in 'sysconfdir', 'examplesdir', 'mandir':
    for k in 'prefix', 'sysconfdir':
        if s != k:
            options[s] = options[s].replace('${%s}' % (k, ), options[k])

# validate inputs
if options['destdir'] == '':
    options['destdir'] = '/'
for opt in 'prefix', 'sysconfdir', 'examplesdir', 'mandir':
    p = options[opt]
    c = components(p)
    if os.pardir in c or os.curdir in c:
        logError('Bad value for option "%s".' % (opt, ))
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
print '''Performing %s with:
    destdir=%s
    prefix=%s
    sysconfdir=%s
    examplesdir=%s
    mandir=%s
    pythonbin=%s''' % (stage, destdir, prefix, sysconfdir, examplesdir, mandir, pythonbin)

# install files to prefix
processFiles(install, os.path.join(destdir, prefix[1:]), 'src/usr/', {
        'bin/diffuse': [ ("'../../etc/diffuserc'", repr(relpath(os.path.join(prefix, 'bin'), os.path.join(sysconfdir, 'diffuserc')))), ('/usr/bin/env python', pythonbin) ],
        'share/applications/diffuse.desktop': None,
        'share/diffuse/syntax/*.syntax': None,
        'share/gnome/help/diffuse/*/diffuse.xml': [ ('/usr/', prefix), ('/etc/', sysconfdir) ],
        'share/omf/diffuse/diffuse-*.omf': [ ('/usr/', prefix) ],
        'share/icons/hicolor/*/apps/diffuse.png': None
    })

# install manual
processFiles(install, os.path.join(destdir, mandir[1:]), 'src/usr/share/man/', {
        'man1/diffuse.1': [ ('/usr/', prefix), ('/etc/', sysconfdir) ],
        '*/man1/diffuse.1': [ ('/usr/', prefix), ('/etc/', sysconfdir) ]
    })

# install files to sysconfdir
processFiles(install, os.path.join(destdir, examplesdir[1:]), 'src/etc/', { 'diffuserc': [ ('/etc/', sysconfdir), ('../usr', relpath(sysconfdir, prefix)) ] })

# install translations
processTranslations(install, os.path.join(destdir, prefix[1:]))

if not install:
    # remove directories we own
    for s in 'share/omf/diffuse', 'share/gnome/help/diffuse/C', 'share/gnome/help/diffuse/ru', 'share/gnome/help/diffuse', 'share/diffuse/syntax', 'share/diffuse':
        d = os.path.join(destdir, os.path.join(prefix, s)[1:])
        try:
            os.rmdir(d)
        except OSError:
            logError('Error removing "%s".' % (d, ))

# do post install/removal tasks
if not files_only:
    print 'Performing post %s tasks.' % (stage, )

    cmds = [ [ 'update-desktop-database' ],
             [ 'gtk-update-icon-cache', os.path.join(destdir, os.path.join(prefix, 'icons/hicolor')[1:]) ] ]
    if install:
        cmds.append([ 'scrollkeeper-update', '-q', '-o', os.path.join(destdir, os.path.join(prefix, 'share/omf/diffuse')[1:]) ])
    else:
        cmds.append([ 'scrollkeeper-update', '-q' ])
    for c in cmds:
        for p in os.environ['PATH'].split(os.pathsep):
            if os.path.exists(os.path.join(p, c[0])):
                print ' '.join(c)
                try:
                    if subprocess.Popen(c).wait() != 0:
                        raise OSError()
                except OSError:
                    logError('WARNING: Failed to update documentation database with %s.' % (c[0], ))
                break
        else:
            print 'WARNING: %s is not installed' % (c[0], )
