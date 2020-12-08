project('diffuse',
    version: '0.6.0',
    meson_version: '>= 0.50',
    license: 'GPL-2.0-or-later')

i18n = import('i18n')
python = import('python')

py_installation = python.find_installation('python3')

find_program('gtk-update-icon-cache', required: false)

prefix = get_option('prefix')

bindir = prefix / get_option('bindir')
datadir = prefix / get_option('datadir')
localedir = prefix / get_option('localedir')
libexecdir = prefix / get_option('libexecdir')
sysconfdir = prefix / get_option('sysconfdir')
pythondir = py_installation.get_path('purelib')

pkgdatadir = join_paths(datadir, meson.project_name())
podir = join_paths(meson.source_root(), 'po')

subdir('po')
subdir('data')
subdir('src')

meson.add_install_script('build-scripts/meson-postinstall.py')
