pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'diffuse')

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('PKGDATADIR', pkgdatadir)
conf.set('LOCALEDIR', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('SYSCONFIGDIR', join_paths(get_option('prefix'), get_option('sysconfdir')))
conf.set('BINDIR', join_paths(get_option('prefix'), get_option('bindir')))

configure_file(
  input: 'diffuse.in',
  output: build_machine.system() == 'darwin' ? 'diffuse_impl' : 'diffuse',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

if build_machine.system() == 'darwin'
  configure_file(
    input: 'mac-os-app/diffuse-mac.in',
    output: 'diffuse',
    configuration: conf,
    install: true,
    install_dir: get_option('bindir')
  )
  configure_file(
    input: 'mac-os-app/mac_launcher.sh.in',
    output: 'mac_launcher.sh',
    configuration: conf,
    install: true,
    install_dir: '/Applications/Diffuse.app/Contents/MacOS'
  )
  configure_file(
    input: 'mac-os-app/Info.plist.in',
    output: 'Info.plist',
    configuration: conf,
    install: true,
    install_dir: '/Applications/Diffuse.app/Contents'
  )
endif

diffuse_sources = [
  '__init__.py',
  'constants.py',
  'dialogs.py',
  'main.py',
  'preferences.py',
  'resources.py',
  'utils.py',
  'widgets.py',
  'window.py',
]

install_data(diffuse_sources, install_dir: moduledir)
install_subdir('vcs', install_dir: moduledir, strip_directory: false)
