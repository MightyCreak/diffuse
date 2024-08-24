# Developers setup

## Requirements

Diffuse depends on these projects:

* Python 3.8+
* PyPi
* Cairo and GObject Introspection development headers
* Meson
* Flatpak and Flatpak builder (Linux only)

### Install the system dependencies

It's a bit difficult to get the command lines for all the systems, but these
examples should be enough to find the packages on most systems.

<details>
    <summary>Debian/Ubuntu</summary>

```sh
sudo apt install python3-pip libcairo2-dev libgirepository1.0-dev meson flatpak flatpak-builder
```

_Note: Tested on Debian 11 (Buster) and Ubuntu 20.04 (Focal)_
</details>
<details>
    <summary>Fedora</summary>

```sh
sudo dnf install python-pip cairo-devel cairo-gobject-devel meson flatpak flatpak-builder
```

_Note: Tested on Fedora 36_
</details>

<details>
    <summary>macOS</summary>

On Mac, all dependencies can be installed using [Homebrew](https://docs.brew.sh/):

```sh
brew install meson python3 py3cairo pygobject3 gtk+3 librsvg
```

_Note: Tested on macOS 12.5 (Monterey)_
</details>

### Install the project dependencies

To install the requirements just to execute the binary, run:

```sh
pip3 install -r requirements.txt
```

For developer tools, run this one instead (it includes requirements.txt):

```sh
pip3 install -r requirements.dev.txt
```

### Install git hooks (optional)

There is a pre-commit git hook that runs some linters on the source code before committing.

To install the git hooks (for the repository only), run this command:

```sh
git config --local core.hooksPath ./.githooks
```

## Setup

### Setup on Linux using Flatpak

#### Build, test and install

To build, test and install Diffuse locally:

```sh
flatpak install runtime/org.gnome.Sdk/$(uname -p)/44
flatpak-builder --user --install build-flatpak io.github.mightycreak.Diffuse.yml
```

#### Run

To run Diffuse through Flatpak:

```sh
flatpak run --user io.github.mightycreak.Diffuse
```

#### Uninstall

To uninstall Diffuse:

```sh
flatpak remove --user io.github.mightycreak.Diffuse
```

### Setup on Linux using Meson

#### Build and test

Diffuse is using Meson as its build system.

To build and test Diffuse:

```sh
meson setup build
meson compile -C build
meson test -C build
```

#### Install on system and run

To install Diffuse on your system (e.g. `/usr/local/`):

```sh
meson install -C build  # requires admin privileges
```

To run Diffuse:

```sh
diffuse
```

#### Install in a custom directory and run

Meson allows to change the default installation directories, see
[command-line documentation](https://mesonbuild.com/Commands.html#configure).

To install Diffuse in a custom directory (e.g. `~/bin/diffuse`):

```sh
meson install -C build --destdir ~/bin/diffuse
```

To run Diffuse:

```sh
export PYTHONPATH=$HOME/bin/diffuse/usr/local/share/diffuse
cd ~/bin/diffuse/usr/local/bin
./diffuse
```

#### Uninstall

To uninstall Diffuse afterwards:

```sh
sudo ninja uninstall -C build
sudo rm -v /usr/local/share/locale/*/LC_MESSAGES/diffuse.mo
```

### Setup on macOS

#### Build and test

Diffuse is using Meson as its build system, this is the only supported system
on macOS.

To build and test Diffuse:

```sh
meson setup build
meson compile -C build
meson test -C build
```

#### Install on system and run

To install Diffuse on your system (e.g. `/Applications/` and `/opt/homebrew/`
or `/usr/local/`):

```sh
meson install -C build  # requires admin privileges
```

To run Diffuse:

```sh
diffuse
```

_Note: The `diffuse` command can be used to launch Diffuse as a native Mac app_
_that is installed into `/Applications/Diffuse.app`._

### Setup on Windows (deprecated)

_Note:_ The Windows port is not maintained and would need some love.
Contributions are very welcome! 😉

The `windows-installer` directory contains scripts for building an installable
package for Windows that includes all dependencies.

Diffuse can be packaged as a portable application by copying the installation
directory to a pen drive and creating a front end that sets the
`XDG_CONFIG_HOME` and `XDG_DATA_DIR` environment variables prior to launching
Diffuse.  The `XDG_CONFIG_HOME` and `XDG_DATA_DIR` environment variables
indicate where Diffuse should store persistent settings (eg. the path to a
writable directory on the pen drive).
