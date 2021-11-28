# Copyright (C) 2006-2013 Derrick Moser <derrick_moser@yahoo.com>
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

# This program creates EXE versions of diffuse and diffusew using py2exe.

from distutils.core import setup

setup(
    name='diffuse',
    description='Diffuse',
    version='1.0',

    console=[{'script': 'temp/diffuse.py', 'icon_resources': [(1, 'diffuse.ico')]}],
    windows=[{'script': 'temp/diffusew.pyw', 'icon_resources': [(1, 'diffuse.ico')]}],
    options={'py2exe': {
        'packages': 'encodings, gtk',
        'includes': 'cairo, pango, pangocairo, atk, gobject',
        'excludes': [
            '_ssl',
            'pyreadline',
            'doctest',
            'pickle',
            'calendar',
            'unittest',
            'inspect',
            'pdb'
        ],
        'dll_excludes': ['libglade-2.0-0.dll']
    }}
 )
