pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, meson.project_name())
sysconfdir = join_paths(get_option('prefix'), get_option('sysconfdir'))

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)
conf.set('sysconfigdir', sysconfdir)
conf.set('log_print_output', get_option('log_print_output'))
conf.set('log_print_stack', get_option('log_print_stack'))
conf.set('use_flatpak', get_option('use_flatpak'))

configure_file(
  input: 'diffuse.in',
  output: 'diffuse',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

configure_file(
  input: 'constants.py.in',
  output: 'constants.py',
  configuration: conf,
  install: true,
  install_dir: moduledir
)

diffuse_sources = [
  '__init__.py',
  'dialogs.py',
  'main.py',
  'preferences.py',
  'resources.py',
  'utils.py',
]

install_data(diffuse_sources, install_dir: moduledir)
install_subdir('vcs', install_dir: moduledir, strip_directory: false)
