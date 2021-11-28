pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'diffuse')

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('PKGDATADIR', pkgdatadir)
conf.set('LOCALEDIR', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('SYSCONFIGDIR', join_paths(get_option('prefix'), get_option('sysconfdir')))

configure_file(
  input: 'diffuse.in',
  output: 'diffuse',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

diffuse_sources = [
  '__init__.py',
  'constants.py',
  'dialogs.py',
  'main.py',
  'preferences.py',
  'resources.py',
  'utils.py',
  'widgets.py',
]

install_data(diffuse_sources, install_dir: moduledir)
install_subdir('vcs', install_dir: moduledir, strip_directory: false)
