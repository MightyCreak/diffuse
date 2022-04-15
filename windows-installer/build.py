# Copyright (C) 2006-2014 Derrick Moser <derrick_moser@yahoo.com>
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

# This program builds a Windows installer for Diffuse.

import codecs
import glob
import os
import platform
import subprocess
import sys

VERSION = '0.7.5'
PACKAGE = '1'
PLATFORM = 'win' + ''.join([c for c in platform.architecture()[0] if c.isdigit()])
INSTALLER = 'diffuse-%s-%s.%s' % (VERSION, PACKAGE, PLATFORM)


# makes a directory without complaining if it already exists
def mkdir(s):
    if not os.path.isdir(s):
        os.mkdir(s)


# copies a file to 'dest'
def copyFile(src, dest, use_text_mode=False, enc=None):
    print('copying "%s" to "%s"' % (src, dest))
    if use_text_mode:
        r, w = 'r', 'w'
    else:
        r, w = 'rb', 'wb'
    f = open(src, r)
    s = f.read()
    f.close()
    if enc is not None:
        s = codecs.encode(str(s, encoding='utf_8'), enc)
    f = open(dest, w)
    f.write(s)
    f.close()


# recursively copies a directory to 'dest'
def copyDir(src, dest):
    print('copying "%s" to "%s"' % (src, dest))
    mkdir(dest)
    for f in os.listdir(src):
        s = os.path.join(src, f)
        d = os.path.join(dest, f)
        if os.path.isfile(s):
            copyFile(s, d)
        elif os.path.isdir(s):
            copyDir(s, d)


# helper to clean up the resulting HTML
def extract_tag(s, start, end):
    i = s.find(start)
    if i >= 0:
        pre = s[:i]
        i += len(start)
        j = s.find(end, i)
        if j >= 0:
            return pre, start, s[i:j], end, s[j+len(end):]


#
# Make sure we are in the correct directory.
#

path = os.path.dirname(sys.argv[0])
if path != '':
    os.chdir(path)

#
# Build EXE versions of the Diffuse Python script.
#

# make a temp directory
mkdir('temp')
# copy script into temp directory under two names
for p in 'temp\\diffuse.py', 'temp\\diffusew.pyw':
    copyFile('..\\src\\usr\\bin\\diffuse', p, True)

# build executable in 'dist' from diffuse.py and diffusew.pyw
args = [sys.executable, 'setup.py', 'py2exe']
if os.spawnv(os.P_WAIT, args[0], args) != 0:
    raise OSError('Could not run setup.py')

# include Microsoft redistributables needed by Python 2.6 and above
for f in 'msvcm90.dll', 'msvcp90.dll', 'msvcr90.dll':
    copyFile(
        os.path.join(
            os.environ['SYSTEMROOT'],
            'WinSxS\\x86_Microsoft.VC90.CRT_1fc8b3b9a1e18e3b_9.0.21022.8_x-ww_d08d0375\\' + f
        ),
        'dist\\' + f
    )
copyFile(
    os.path.join(
        os.environ['SYSTEMROOT'],
        'WinSxS\\Manifests\\x86_Microsoft.VC90.CRT_1fc8b3b9a1e18e3b_9.0.21022.8_x-ww_d08d0375.manifest'  # noqa: E501
    ),
    'dist\\Microsoft.VC90.CRT.manifest'
)

# include GTK dependencies
gtk_dir = os.environ['GTK_BASEPATH']
copyDir(os.path.join(gtk_dir, 'etc'), 'dist\\etc')
copyDir(os.path.join(gtk_dir, 'lib'), 'dist\\lib')
mkdir('dist\\share')
copyDir(os.path.join(gtk_dir, 'share\\icons'), 'dist\\share\\icons')
copyDir(os.path.join(gtk_dir, 'share\\themes'), 'dist\\share\\themes')

#
# Add all support files.
#

# syntax highlighting support
mkdir('dist\\syntax')
for p in glob.glob('..\\src\\usr\\share\\diffuse\\syntax\\*.syntax'):
    copyFile(p, os.path.join('dist\\syntax', os.path.basename(p)), True)
copyFile('diffuserc', 'dist\\diffuserc')

# application icon
copyDir('..\\src\\usr\\share\\icons', 'dist\\share\\icons')

# translations
mkdir('dist\\share\\locale')
locale_dir = os.path.join(gtk_dir, 'share\\locale')
for s in glob.glob('..\\po\\*.po'):
    lang = s[16:-3]
    # Diffuse localisations
    print('Compiling %s translation' % (lang, ))
    d = 'dist'
    for p in ['locale', lang, 'LC_MESSAGES']:
        d = os.path.join(d, p)
        mkdir(d)
    d = os.path.join(d, 'diffuse.mo')
    if subprocess.Popen(['msgfmt', '-o', d, s]).wait() != 0:
        raise OSError('Failed to compile "%s" into "%s".' % (s, d))
    # GTK localisations
    d = os.path.join(locale_dir, lang)
    if os.path.isdir(d):
        copyDir(d, os.path.join('dist\\share\\locale', lang))

#
# Add all documentation.
#

# license and other documentation
for p in 'AUTHORS', 'ChangeLog', 'COPYING', 'README':
    copyFile(os.path.join('..', p), os.path.join('dist', p + '.txt'), True)
for p, enc in [('ChangeLog_ru', 'cp1251'), ('README_ru', 'cp1251')]:
    copyFile(os.path.join('..', p), os.path.join('dist', p + '.txt'), True, enc)

# fetch translations for English text hard coded in the stylesheets
translations = {}
f = open('translations.txt', 'rb')
for v in f.read().split('\n'):
    v = v.split(':')
    if len(v) == 3:
        lang = v[0]
        if lang not in translations:
            translations[lang] = []
        translations[lang].append(v[1:])
f.close()

# convert the manual from DocBook to HTML
d = '..\\src\\usr\\share\\gnome\\help\\diffuse'
for lang in os.listdir(d):
    p = os.path.join(os.path.join(d, lang), 'diffuse.xml')
    if os.path.isfile(p):
        cmd = ['xsltproc', '/usr/share/sgml/docbook/xsl-stylesheets/html/docbook.xsl', p]
        info = subprocess.STARTUPINFO()
        info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        info.wShowWindow = subprocess.SW_HIDE
        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            startupinfo=info)
        proc.stdin.close()
        proc.stderr.close()
        fd = proc.stdout
        s = fd.read()
        fd.close()
        if proc.wait() != 0:
            raise OSError('Could not run xsltproc')
        # add link to style sheet
        s = s.replace(
            '</head>',
            '<link rel="stylesheet" href="style.css" type="text/css"/></head>'
        )
        s = s.replace('<p>\n        </p>', '')
        s = s.replace('<p>\n      </p>', '')
        # cleanup HTML to simpler UTF-8 form
        s = s.replace(
            '<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">',
            '<meta http-equiv="Content-Type" content="text/html; charset=utf-8">'
        )
        a, idx = [], 0
        while True:
            i = s.find('&#', idx)
            if i < 0:
                a.append(str(s[idx:], encoding='latin_1'))
                break
            a.append(str(s[idx:i], encoding='latin_1'))
            i += 2
            j = s.find(';', i)
            a.append(chr(int(s[i:j])))
            idx = j + 1
        s = ''.join(a)
        s = codecs.encode(s, 'utf-8')
        # clean up translator credit portion
        div = extract_tag(s, '<div class="othercredit">', '</div>')
        if div is not None:
            firstname = extract_tag(div[2], '<span class="firstname">', '</span>')
            surname = extract_tag(div[2], '<span class="surname">', '</span>')
            contrib = extract_tag(div[2], '<span class="contrib">', '</span>')
            email = extract_tag(div[2], '<code class="email">', '</code>')
            copyright = extract_tag(div[4], '<p class="copyright">', '</p>')
            if (
                firstname is not None and
                surname is not None and
                contrib is not None and
                email is not None and
                copyright is not None
            ):
                s = (
                    '%s%s<p><span class="contrib">%s:</span> '
                    '<span class="firstname">%s</span> '
                    '<span class="surname">%s</span> '
                    '<code class="email">%s</code></p>%s'
                ) % (
                    div[0],
                    ''.join(copyright[:4]),
                    contrib[2],
                    firstname[2],
                    surname[2],
                    email[2],
                    copyright[4]
                )
        # translate extra text
        for k, v in translations.get(lang, []):
            s = s.replace(k, v)
        # save HTML version of the manual
        fn = 'manual'
        if lang != 'C':
            fn += '_' + lang
            # update the document language
            s = s.replace(' lang="en" ', ' lang="%s" ' % (lang,))
        f = open(os.path.join('dist', fn + '.html'), 'w')
        f.write(s)
        f.close()
copyFile('style.css', 'dist\\style.css')

#
# Package everything into a single EXE installer.
#

# build binary installer
copyFile(os.path.join(os.environ['ADD_PATH_HOME'], 'add_path.exe'), 'dist\\add_path.exe')
if os.system('iscc diffuse.iss /F%s' % (INSTALLER, )) != 0:
    raise OSError('Could not run iscc')

#
# Declare success.
#

print('Successfully created "%s".' % (INSTALLER, ))
