#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2020 Romain Failliot <romain.failliot@foolstep.com>
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the license, or (at your option) any later
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

import argparse
import os
import subprocess
import shutil
import tempfile


def check_translation(filename):
    subprocess.run(['msgfmt', '-c', '-v', filename])


def update_translation(filename):
    print(f'Updating translation file "{filename}"...')

    # Get language
    lang = os.path.splitext(filename)[0]

    # Move existing .po file to working directory
    tmpfile = os.path.join(tmpdir, filename)
    shutil.move(filename, tmpfile)

    # Create a new .po file for this language
    emptypofile = os.path.join(tmpdir, f'{lang}.empty.po')
    subprocess.run([
        'msginit',
        '--no-wrap',
        '--no-translator',
        '-l',
        lang,
        '-o',
        emptypofile,
        '-i',
        'diffuse.pot'])

    # Merge with the old translation
    subprocess.run([
        'msgmerge',
        '-q',
        '--no-wrap',
        tmpfile,
        emptypofile,
        '-o',
        filename])

    # Validate translation
    print(f'Validate "{filename}":')
    check_translation(filename)

    print('Update done.')


# Setup argument parser
parser = argparse.ArgumentParser(description='Update translation files (.po).')
parser.add_argument('po_files', metavar='filename.po', nargs='+',
                    help='the translation file')
parser.add_argument('-c', '--check-only', action='store_true',
                    help='check the PO files')

# Parse command-line arguments
args = parser.parse_args()

# Get PO files from command-line
po_files = args.po_files
po_files.sort()

if args.check_only:
    for file in po_files:
        print(f'Validate "{file}":')
        check_translation(file)
    exit(0)

# Create temporary working directory
tmpdir = tempfile.mkdtemp()
try:
    # Update PO files
    for file in po_files:
        update_translation(file)
finally:
    # Remove working directory
    shutil.rmtree(tmpdir)
