#!/usr/bin/env python

# Copyright (C) 2010 Derrick Moser <derrick_moser@yahoo.com>
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

# This program translates Diffuse's DocBook help into a manual page using the
# book2manual.xsl template.

import os
import subprocess

# fetch translations for English text hard coded in the stylesheets
translations = {}
f = open('translations.txt', 'rb')
for v in f.read().split('\n'):
    v = v.split(':')
    if len(v) == 3:
        lang = v[0]
        if not translations.has_key(lang):
            translations[lang] = []
        translations[lang].append(v[1:])
f.close()

# find all localised versions of the DocBook manual
d = '../src/usr/share/gnome/help/diffuse'
for lang in os.listdir(d):
    # skip over any .svn files
    if lang.startswith('.'):
        continue

    # convert regular DocBook manual into a form suitable for man pages
    cmd = [ 'xsltproc', 'book2manual.xsl', os.path.join(os.path.join(d, lang), 'diffuse.xml') ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.stdin.close()
    proc.stderr.close()
    fd = proc.stdout
    s = fd.read()
    fd.close()
    if proc.wait() != 0:
        raise OSError('Could not run xsltproc')
 
    # save man page suitable DocBook file
    a = 'diffuse.xml'
    f = open(a, 'wb')
    f.write(s)
    f.close()

    # convert to man page
    cmd = [ 'xsltproc', '/usr/share/sgml/docbook/stylesheet/xsl/nwalsh/manpages/docbook.xsl', a ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.stdin.close()
    proc.stderr.close()
    fd = proc.stdout
    s = fd.read()
    fd.close()
    if proc.wait() != 0:
        raise OSError('Could not run xsltproc')
    os.unlink(a)

    # read resulting man page
    f = open('diffuse.1', 'rb')
    s = f.read()
    f.close()
    os.unlink('diffuse.1')
    # remove comments
    s = '\n'.join([ c for c in s.split('\n') if not c.startswith('.\\"') ])
    # fix arrow
    s = s.replace('\xe2\x86\x92', '\\(->')
    # translate extra text
    for k, v in translations.get(lang, []):
        s = s.replace(k, v)

    # figure out where to save the new man page
    # make subdirectories if necessary
    dd = '../src/usr/share/man'
    if lang != 'C':
        dd = os.path.join(dd, lang)
    if not os.path.exists(dd):
        os.mkdir(dd)
    dd = os.path.join(dd, 'man1')
    if not os.path.exists(dd):
        os.mkdir(dd)

    # finally save the man page
    f = open(os.path.join(dd, 'diffuse.1'), 'wb')
    f.write(s)
    f.close()
