pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())

desktop_file = i18n.merge_file(
  input: 'io.github.mightycreak.Diffuse.desktop.in',
  output: 'io.github.mightycreak.Diffuse.desktop',
  type: 'desktop',
  po_dir: '../po',
  install: true,
  install_dir: join_paths(get_option('datadir'), 'applications')
)

desktop_utils = find_program('desktop-file-validate', required: false)
if desktop_utils.found()
  test('Validate desktop file', desktop_utils,
    args: [desktop_file]
  )
endif

appstream_file = i18n.merge_file(
  input: 'io.github.mightycreak.Diffuse.metainfo.xml.in',
  output: 'io.github.mightycreak.Diffuse.metainfo.xml',
  po_dir: '../po',
  install: true,
  install_dir: join_paths(get_option('datadir'), 'appdata')
)

appstream_util = find_program('appstream-util', required: false)
if appstream_util.found()
  test('Validate appstream file', appstream_util,
    args: ['validate', appstream_file]
  )
endif

# Diffuse config file
conf = configuration_data()
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'diffuserc.in',
  output: 'diffuserc',
  configuration: conf,
  install: true,
  install_dir: get_option('sysconfdir')
)

# Data files
install_subdir('usr/share', install_dir: get_option('datadir'), strip_directory: true)

subdir('icons')