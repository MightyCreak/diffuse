# Diffuse documentation

**Diffuse** is a small and simple text merge tool written in Python.  

With Diffuse, you can easily merge, edit, and review changes to your code.

- [Quick Start](#quick-start)
- [Users](users.md)
- [Translators](translators.md)
- Developers
    - [Developers setup](developers/developers-setup.md)
    - [Release process](developers/release-process.md)

## Installation

### Using Flatpak

```sh
flatpak install io.github.mightycreak.Diffuse
```

Flatpak is probably the easiest way to install Diffuse on any distribution and
get the latest and greatest as quickly as possible. The Flatpak package is
hosted on [Flathub](https://flathub.org).

_Note:_ If the Flathub repository is not installed yet, please follow
[these instructions](https://flatpak.org/setup/).

### Using the distribution package manager

The Diffuse package statuses for every distributions can been seen on
[repology](https://repology.org/project/diffuse/versions).

Huge thanks to [@bongochong](https://github.com/bongochong) for maintaining the
Diffuse package on Fedora.

## Integrate with Git

Diffuse is compatible with `git difftool` command-line. To use Diffuse as Git
diff tool, run:

```sh
git config --global diff.tool diffuse
```

## Quick Start
Compare a Set of Files
 <pre>$ diffuse <em>file1</em> <em>file2</em> <em>file3</em></pre>
Review Local Changes or Fix Merge Conflicts
 <pre>$ diffuse -m</pre>
Compare Specific Revisions
 <pre>$ diffuse -r <em>rev1</em> -r <em>rev2</em> <em>file</em></pre>
Inspect a Revision
 <pre>$ diffuse -c <em>rev</em></pre>

