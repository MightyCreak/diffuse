# Developers documentation

## Requirements

Diffuse depends on these projects:
* Python 3.8+
* PyPi
* Cairo and GObject Introspection development headers
* Meson
* Flatpak and Flatpak builder

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
sudo dnf install python-pip python3-cairo-devel python3-gobject-devel meson flatpak flatpak-builder
```

_Note: Tested on Fedora 34_
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
flatpak install runtime/org.gnome.Sdk/$(uname -p)/41
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

### Build, test and install using Meson

Diffuse build system is meson.

To install diffuse locally:

```sh
meson setup build
cd build
meson compile
meson test
meson install # requires admin privileges
```

To uninstall diffuse afterwards:

```sh
sudo ninja uninstall -C build
sudo rm -v /usr/local/share/locale/*/LC_MESSAGES/diffuse.mo
```

Meson allows to change the default installation directories, see
[command-line documentation](https://mesonbuild.com/Commands.html#configure).

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
