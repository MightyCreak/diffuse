# Diffuse

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

Diffuse is implemented entirely in Python and should run on any platform with
Python and PyGObject.

* Python >= 3.4
* PyGObject >= 3.18

## Users

### Installing using Flatpak

This is the easiest way to install Diffuse:

```sh
flatpak install io.github.mightycreak.Diffuse
```

## Developers

### Setup

#### Run Diffuse from source

To run Diffuse from the source code, type this:
```sh
python main.py
```

To debug with VS Code, open the directory in VS Code, place your breakpoints and hit F5.

#### Build Diffuse

To build Diffuse, type this:
```sh
python setup.py build
```

To run from the build, type this:
```sh
PYTHONPATH=build/lib ./build/scripts-3.7/diffuse
```

#### Install Diffuse locally

Diffuse build system is meson.

To install diffuse locally:

```sh
meson setup build
cd build
meson compile
meson install # requires admin privileges
```

To uninstall diffuse afterwards:

```sh
sudo ninja uninstall -C build
sudo rm -v /usr/local/share/locale/*/LC_MESSAGES/diffuse.mo
```

Meson allows to change the default installation directories, see
[command-line documentation](https://mesonbuild.com/Commands.html#configure).

### Installing on Windows

The `windows-installer` directory contains scripts for building an installable
package for Windows that includes all dependencies.

Diffuse can be packaged as a portable application by copying the installation
directory to a pen drive and creating a front end that sets the
`XDG_CONFIG_HOME` and `XDG_DATA_DIR` environment variables prior to launching
Diffuse.  The `XDG_CONFIG_HOME` and `XDG_DATA_DIR` environment variables
indicate where Diffuse should store persistent settings (eg. the path to a
writable directory on the pen drive).

## Building and testing the Flatpak package

To install Diffuse locally:

```sh
flatpak install runtime/org.gnome.Sdk/$(uname -p)/3.38
flatpak-builder build-flatpak --user --install io.github.mightycreak.Diffuse.yml
```

To run Diffuse through Flatpak:

```sh
flatpak run io.github.mightycreak.Diffuse
```

To uninstall Diffuse:

```sh
flatpak remove io.github.mightycreak.Diffuse
```

## Help Documentation

Diffuse's help documentation is written in the DocBook format and can be easily
converted into other formats using XSLT stylesheets.  If the local help
documentation or its browser are unavailable, Diffuse will attempt to display
the on-line help documentation using a web browser.

## Licenses

Diffuse is under the [GPLv2](COPYING).

The file [io.github.mightycreak.Diffuse.appdata.xml.in](data/io.github.mightycreak.Diffuse.appdata.xml.in)
is licensed under the [FSF-AP](https://www.gnu.org/prep/maintain/html_node/License-Notices-for-Other-Files.html)
license.

Copyright (C) 2006-2019 Derrick Moser <derrick_moser@yahoo.com>  
Copyright (C) 2015-2021 Romain Failliot <romain.failliot@foolstep.com>

Icon made by [@jimmac](https://github.com/jimmac).
