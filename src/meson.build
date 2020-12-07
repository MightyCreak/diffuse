# Diffuse binary file
diffuse_conf = configuration_data()
diffuse_conf.set('SYSCONFIGDIR', sysconfdir)

configure_file(
  input: 'usr/bin/diffuse.py.in',
  output: 'diffuse',
  configuration: diffuse_conf,
  install: true,
  install_dir: bindir
)

# Diffuse config file
diffuserc_conf = configuration_data()
diffuserc_conf.set('PKGDATADIR', pkgdatadir)

configure_file(
  input: 'etc/diffuserc.py.in',
  output: 'diffuserc',
  configuration: diffuserc_conf,
  install: true,
  install_dir: sysconfdir
)

# Validate MetaInfo file
metainfo_file = join_paths(meson.source_root(), 'src/usr/share/metainfo/io.github.mightycreak.Diffuse.metainfo.xml')
ascli_exe = find_program('appstreamcli', required: false)
if ascli_exe.found()
  test('validate metainfo file',
        ascli_exe,
        args: ['validate',
               '--no-net',
               '--pedantic',
               metainfo_file]
  )
endif

# Data files
install_subdir('usr/share', install_dir: datadir, strip_directory: true)
