# Developers setup

## Requirements

Diffuse depends on these projects:

* Python 3.8+
* PyPi
* Cairo and GObject Introspection development headers
* Meson
* Flatpak and Flatpak builder (Linux only)

### Install the distribution dependencies

It's a bit difficult to get the command lines for all the distributions and
their releases, but it should be enough to find the packages on other
distributions.

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

_Note: Tested on Fedora 34_
</details>

<details>
    <summary>Mac OS</summary>

On Mac, all deps can be fetched using [Homebrew](https://docs.brew.sh/).

```sh
brew install meson python3 py3cairo pygobject3 gtk+3
```

_Note: Tested on macOS 12.5 (Monterey)_

You don't need to use `pip` because the above `brew` command installs all dependencies.
</details>

### Install the project dependencies

To install the requirements just to execute the binary, run:

```sh
pip install -r requirements.txt
```

For developer tools, run this one instead (it includes requirements.txt):

```sh
pip install -r requirements.dev.txt
```

## Setup on Linux

### Build, test and install using Flatpak

To install Diffuse locally:

```sh
flatpak install runtime/org.gnome.Sdk/$(uname -p)/42
flatpak-builder --user --install build-flatpak io.github.mightycreak.Diffuse.yml
```

To run Diffuse through Flatpak:

```sh
flatpak run io.github.mightycreak.Diffuse
```

To uninstall Diffuse:

```sh
flatpak remove io.github.mightycreak.Diffuse
```

## Build, test and install using Meson on Linux and Mac OS

Diffuse build system is meson.

To compile and test Diffuse:

```sh
meson setup build
cd build
meson compile
meson test
```

To install Diffuse on your system (e.g. `/usr/local/`):

```sh
meson install # requires admin privileges

# Run Diffuse
diffuse
```

To install Diffuse on a custom directory (e.g. `~/bin/diffuse`):

```sh
meson install --destdir ~/bin/diffuse

# Run Diffuse
cd ~/bin/diffuse/usr/local/bin
PYTHONPATH=$HOME/bin/diffuse/usr/local/share/diffuse ./diffuse
```

To uninstall diffuse afterwards:

```sh
sudo ninja uninstall -C build
sudo rm -v /usr/local/share/locale/*/LC_MESSAGES/diffuse.mo
```

Meson allows to change the default installation directories, see
[command-line documentation](https://mesonbuild.com/Commands.html#configure).

## Setup on Mac OS

Building on Mac OS is similar to building on Linux. To recap, these are
the steps needed to build and install Diffuse manually:

```brew install meson python3 py3cairo pygobject3 gtk+3
  meson setup build
  cd build
  meson compile
  meson test
  meson install
```

After `meson install`, the `diffuse` command can be used to launch Diffuse
as a native Mac app that is installed into `/Applications/Diffuse.app`.

The `diffuse` command is compatible with git. To use Diffuse as git's
`git difftool` run `git config --global diff.tool diffuse`

## Setup on Windows

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
