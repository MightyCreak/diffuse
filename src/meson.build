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

configure_file(
  input: 'diffuse.in',
  output: 'diffuse',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

diffuse_sources = [
  '__init__.py',
  'main.py',
  'utils.py',
]

install_data(diffuse_sources, install_dir: moduledir)
