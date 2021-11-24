# Developers documentation

## Requirements

Diffuse is implemented in Python and should run on any platform with Python and
PyGObject.

* Python >= 3.4
* PyGObject >= 3.18

## Setup on Linux

### Build, test and install using Flatpak

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
