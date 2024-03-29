#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2021 Romain Failliot <romain.failliot@foolstep.com>
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
import tempfile


def check_translation(filename):
    print(f'Validate file "{filename}":')
    subprocess.run(['msgfmt', '-c', '-v', filename])


def remove_obsolete_messages(filename):
    print(f'Removing obsolete messages in file "{filename}"...')
    subprocess.run(['msgattrib', '--no-obsolete', '-o', filename, filename])


def update_translation(filename):
    print(f'Updating translation file "{filename}"...')

    # Get language
    lang = os.path.splitext(filename)[0]

    with tempfile.NamedTemporaryFile() as ftmp:
        # Create temporary .po file for this language
        subprocess.run([
            'msginit',
            '--no-translator',
            '--width=84',
            f'--locale={lang}',
            f'--output-file={ftmp.name}',
            '--input=diffuse.pot'])

        # Merge with the previous translation
        subprocess.run([
            'msgmerge',
            '--quiet',
            '--width=84',
            f'--output-file={filename}',
            filename,
            ftmp.name])

    # Validate translation
    check_translation(filename)

    print('Update done.')


if __name__ == '__main__':
    # Setup argument parser
    parser = argparse.ArgumentParser(description='Update translation files (.po).')
    parser.add_argument('po_files', metavar='filename.po', nargs='+',
                        help='the translation file')
    parser.add_argument('--remove-obsolete', action='store_true',
                        help='remove obsolete (#~) messages')
    parser.add_argument('--check-only', action='store_true',
                        help='check the PO files')

    # Parse command-line arguments
    args = parser.parse_args()

    # Get PO files from command-line
    po_files = args.po_files
    po_files.sort()

    if args.check_only:
        # Validate PO files
        for file in po_files:
            check_translation(file)
        exit(0)

    if args.remove_obsolete:
        # Remove obsolete messages
        for file in po_files:
            remove_obsolete_messages(file)
        exit(0)

    # Update PO files
    for file in po_files:
        update_translation(file)
