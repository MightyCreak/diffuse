# Users documentation

## Installation

### Using Flatpak

Flatpak is probably the easiest way to install Diffuse on any distribution and
get the latest and greatest as quickly as possible. The Flatpak package is
hosted on [Flathub](https://flathub.org).

_Note:_ If the Flathub repository is not installed yet, please follow
[these instructions](https://flatpak.org/setup/).

Install diffuse using

```sh
flatpak install io.github.mightycreak.Diffuse
```

then run it either from you application menu or via command line

```sh
flatpak run io.github.mightycreak.Diffuse
```

To open files for comparison from your shell run

```sh
flatpak run --file-forwarding io.github.mightycreak.Diffuse file1 file2
```

### Using the distribution package manager

The Diffuse package statuses for every distributions can been seen on
[repology](https://repology.org/project/diffuse/versions).

Huge thanks to [@bongochong](https://github.com/bongochong) for maintaining the
Diffuse package on Fedora.

## Integrate with Git

Diffuse is compatible with `git difftool` and `git mergetool` command-line. To use Diffuse as Git
diff/merge tool, run:

```sh
git config --global difftool.diffuse_flatpak.cmd 'flatpak run --file-forwarding --filesystem=/tmp io.github.mightycreak.Diffuse $LOCAL $REMOTE'
git config --global diff.tool diffuse_flatpak
```
```sh
git config --global mergetool.diffuse_flatpak.cmd 'flatpak run --file-forwarding --filesystem=/tmp io.github.mightycreak.Diffuse $BASE $LOCAL $MERGED $REMOTE'
git config --global merge.tool diffuse_flatpak
```
