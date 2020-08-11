# Diffuse

Version 0.5.0

Copyright (C) 2006-2019 Derrick Moser <derrick_moser@yahoo.com>  
Copyright (C) 2015-2020 Romain Failliot <romain.failliot@foolstep.com>

----

Diffuse is a graphical tool for merging and comparing text files.  Diffuse is
able to compare an arbitrary number of files side-by-side and gives users the
ability to manually adjust line matching and directly edit files.  Diffuse can
also retrieve revisions of files from Bazaar, CVS, Darcs, Git, Mercurial,
Monotone, RCS, Subversion, and SVK repositories for comparison and merging.

Some key features of Diffuse:

* Ability to compare and merge an arbitrary number of files side-by-side (n-way
  merges)
* Line matching can be manually corrected by the user
* Ability to directly edit files
* Syntax highlighting
* Bazaar, CVS, Darcs, Git, Mercurial, Monotone, RCS, Subversion, and SVK support
* Unicode support
* Unlimited undo
* Easy keyboard navigation

## Requirements

* Python >= 3.4
* PyGObject >= 3.18

Diffuse is implemented entirely in Python and should run on any platform with
Python and PyGTK.  If you need to manually install PyGTK, please be aware its
dependencies should be installed prior to installing PyGTK.

Diffuse can be run directly from an untared source distribution on any POSIX
system or installed with the instructions described in the next section.

The location of the personal preferences, state, and initialisation files have
changed in the 0.4.1 release.  Old settings may be migrated using the following
commands:

    $ mkdir -p ~/.config/diffuse
    $ mv ~/.diffuse/config ~/.config/diffuse/state
    $ mv ~/.diffuse/* ~/.config/diffuse
    $ rmdir ~/.diffuse

The rules for parsing files in `~/.diffuse` changed in the 0.3.0 release.
Non-fatal errors may be reported when parsing old files.  These errors can be
fixed by removing the offending lines (or the entire file) from
`~/.config/diffuse/diffuserc`.

## Installing on POSIX systems

Diffuse build system is meson.

To install diffuse locally:

    meson builddir
    meson install -C builddir

To uninstall diffuse afterwards:

    sudo ninja uninstall -C builddir
    sudo rm -v /usr/local/share/locale/*/LC_MESSAGES/diffuse.mo

Meson allows to change the default installation directories, see
[command-line documentation](https://mesonbuild.com/Commands.html#configure).

## Installing on Windows

The `windows-installer` directory contains scripts for building an installable
package for Windows that includes all dependencies.

Diffuse can be packaged as a portable application by copying the installation
directory to a pen drive and creating a front end that sets the
`XDG_CONFIG_HOME` and `XDG_DATA_DIR` environment variables prior to launching
Diffuse.  The `XDG_CONFIG_HOME` and `XDG_DATA_DIR` environment variables
indicate where Diffuse should store persistent settings (eg. the path to a
writable directory on the pen drive).

## Help Documentation

Diffuse's help documentation is written in the DocBook format and can be easily
converted into other formats using XSLT stylesheets.  If the local help
documentation or its browser are unavailable, Diffuse will attempt to display
the on-line help documentation using a web browser.
