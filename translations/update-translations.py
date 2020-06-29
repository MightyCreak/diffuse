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

import glob
import os
import subprocess
import shutil
import tempfile

def generate_pot_file():
    subprocess.run(["xgettext", "-s", "-o", "diffuse.pot", "-L", "Python", "../src/usr/bin/diffuse"])

def update_translation(filename):
    print(f"Updating translation file '{filename}'...")

    # Get language
    lang = os.path.splitext(filename)[0]

    # Move existing .po file to working directory
    tmpfile = os.path.join(tmpdir, filename)
    shutil.move(filename, tmpfile)

    # Create a new .po file for this language
    emptypofile = os.path.join(tmpdir, f"{lang}.empty.po")
    subprocess.run(["msginit", "--no-wrap", "--no-translator", "-l", lang, "-o", emptypofile, "-i", "diffuse.pot"])

    # Merge with the old translation
    subprocess.run(["msgmerge", "-q", "--no-wrap", tmpfile, emptypofile, "-o", filename])

    # Validate translation
    print(f"Validation:")
    subprocess.run(["msgfmt", "-c", "-v", filename])

    print(f"Update done.")

# Generate diffuse.pot file
generate_pot_file()

# Create temporary working directory
tmpdir = tempfile.mkdtemp()

try:
    # Update PO files
    po_files = glob.glob("*.po", recursive=False)
    po_files.sort()
    for file in po_files:
        update_translation(file)
finally:
    # Remove working directory
    shutil.rmtree(tmpdir)
