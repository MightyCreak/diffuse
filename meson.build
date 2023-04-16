project('diffuse',
    version: '0.8.2',
    meson_version: '>= 0.55',
    license: 'GPL-2.0-or-later',
    default_options: [ 'warning_level=2' ])

i18n = import('i18n')

subdir('data')
subdir('src')
subdir('po')

if build_machine.system() == 'linux'
  meson.add_install_script('build-aux/meson/postinstall.py')
endif
