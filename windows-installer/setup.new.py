import codecs
import glob
import os
import site
import subprocess
import sys

from cx_Freeze import setup, Executable

siteDir = site.getsitepackages()[1]
gnomeSiteDir = os.path.join(siteDir, "gnome")

# This is the list of dll which are required by PyGI.
# I get this list of DLL using http://technet.microsoft.com/en-us/sysinternals/bb896656.aspx
#   Procedure:
#    1) Run your from from your IDE
#    2) Command for using listdlls.exe
#        c:/path/to/listdlls.exe python.exe > output.txt
#    3) This would return lists of all dll required by you program
#       in my case most of dll file were located in c:\python27\Lib\site-packages\gnome
#       (I am using PyGI (all in one) installer)
#    4) Below is the list of gnome dll I received from listdlls.exe result.

# If you prefer you can import all dlls from c:\python27\Lib\site-packages\gnome folder
# missingDll = glob.glob(gnomeSiteDir + "\\" + '*.dll')
# missingDll = [ dll[len(gnomeSiteDir) + 1:] for dll in missingDll ]

missingDll = [
    # 'libaspell-15.dll',
    'libatk-1.0-0.dll',
    # 'libavcodec-56.dll',
    # 'libavformat-56.dll',
    # 'libavutil-54.dll',
    'libcairo-gobject-2.dll',
    # 'libdb-5.3.dll',
    'libdbus-1-3.dll',
    'libdbus-glib-1-2.dll',
    # 'libdb_sql-5.3.dll',
    # 'libdevhelp-3-2.dll',
    # 'libenchant-1.dll',
    'libepoxy-0.dll',
    'libffi-6.dll',
    'libfontconfig-1.dll',
    'libfreetype-6.dll',
    # 'libgailutil-3-0.dll',
    'libgconf-2-4.dll',
    # 'libgcrypt-11.dll',
    # 'libgda-5.0-4.dll',
    # 'libgda-ui-5.0-4.dll',
    # 'libgdict-1.0-9.dll',
    'libgdk-3-0.dll',
    'libgdk_pixbuf-2.0-0.dll',
    # 'libgdl-3-5.dll',
    # 'libgedit.dll',
    # 'libgee-0.8-2.dll',
    # 'libgeoclue-0.dll',
    # 'libgettextlib-0-18-3.dll',
    # 'libgettextsrc-0-18-3.dll',
    'libgio-2.0-0.dll',
    'libgirepository-1.0-1.dll',
    # 'libgit2-glib-1.0-0.dll',
    # 'libgladeui-2-6.dll',
    'libglib-2.0-0.dll',
    'libgmodule-2.0-0.dll',
    'libgnutls-28.dll',
    'libgobject-2.0-0.dll',
    # 'libgoocanvas-2.0-9.dll',
    # 'libgsf-1-114.dll',
    # 'libgsf-win32-1-114.dll',
    # 'libgspell-1-0.dll',
    # 'libgssapi-3.dll',
    # 'libgstallocators-1.0-0.dll',
    # 'libgstapp-1.0-0.dll',
    # 'libgstaudio-1.0-0.dll',
    # 'libgstbase-1.0-0.dll',
    # 'libgstcheck-1.0-0.dll',
    # 'libgstcontroller-1.0-0.dll',
    # 'libgstfft-1.0-0.dll',
    # 'libgstnet-1.0-0.dll',
    # 'libgstpbutils-1.0-0.dll',
    # 'libgstreamer-1.0-0.dll',
    # 'libgstriff-1.0-0.dll',
    # 'libgstrtp-1.0-0.dll',
    # 'libgstrtsp-1.0-0.dll',
    # 'libgstrtspserver-1.0-0.dll',
    # 'libgstsdp-1.0-0.dll',
    # 'libgsttag-1.0-0.dll',
    # 'libgstvideo-1.0-0.dll',
    # 'libgthread-2.0-0.dll',
    'libgtk-3-0.dll',
    # 'libgtkhex-3-0.dll',
    # 'libgtksourceview-3.0-1.dll',
    # 'libgtkspell3-3-0.dll',
    # 'libgtranslator.dll',
    # 'libgucharmap_2_90-7.dll',
    # 'libgxml-0.10-10.dll',
    'libharfbuzz-0.dll',
    # 'libharfbuzz-gobject-0.dll',
    # 'libharfbuzz-icu-0.dll',
    # 'libicu52.dll',
    'libintl-8.dll',
    # 'libisocodes-0.dll',
    'libjasper-1.dll',
    # 'libjavascriptcoregtk-3.0-0.dll',
    'libjpeg-8.dll',
    # 'libjson-glib-1.0-0.dll',
    # 'liblua51.dll',
    # 'libopenssl.dll',
    # 'liborc-0.4-0.dll',
    # 'liborc-test-0.4-0.dll',
    'libp11-kit-0.dll',
    'libpango-1.0-0.dll',
    'libpangocairo-1.0-0.dll',
    'libpangoft2-1.0-0.dll',
    'libpangowin32-1.0-0.dll',
    # 'libpeas-1.0-0.dll',
    # 'libpeas-gtk-1.0-0.dll',
    'libpng16-16.dll',
    'libproxy.dll',
    'librsvg-2-2.dll',
    # 'libsasl2.dll',
    # 'libsecret-1-0.dll',
    # 'libsoup-2.4-1.dll',
    # 'libsqlite3-0.dll',
    'libstdc++.dll',
    # 'libswresample-1.dll',
    'libtiff-5.dll',
    # 'libvisual-0.4-0.dll',
    # 'libwebkitgtk-3.0-0.dll',
    'libwebp-5.dll',
    'libwinpthread-1.dll',
    'libxmlxpat.dll',
    # 'libxslt-1.dll',
    'libzzz.dll',
]

print("missingDll = [")
for dll in missingDll:
    print("    '" + dll + "',")
print("]")

includeFiles = []
for dll in missingDll:
    includeFiles.append((os.path.join(gnomeSiteDir, dll), dll))
    # includeFiles.append(dll)

# You can import all Gtk Runtime data from gtk folder
# gnomeLibs= ['etc','lib','share']

# You can import only important Gtk Runtime data from gtk folder
gnomeLibs = [
    'lib\\gdk-pixbuf-2.0',
    'lib\\girepository-1.0',
    'lib\\gtk-3.0',
    'share\\glib-2.0'
]

for lib in gnomeLibs:
    includeFiles.append((os.path.join(gnomeSiteDir, lib), lib))

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="diffuse",
    version="0.5",
    description="Diffuse",
    options={'build_exe': {
        'compressed': True,
        'includes': ["gi", "cairo"],
        'excludes': ['wx', 'email', 'pydoc_data', 'curses'],
        'packages': ["gi", "cairo"],
        'include_files': includeFiles
    }},
    executables=[
        Executable(
            "..\\src\\usr\\bin\\diffuse",
            icon="diffuse.ico",
            base=base
        )
    ]
)


# makes a directory without complaining if it already exists
def mkdir(s):
    if not os.path.isdir(s):
        os.mkdir(s)


# copies a file to 'dest'
def copyFile(src, dest, use_text_mode=False, enc=None):
    print('copying "%s" to "%s"' % (src, dest))
    if use_text_mode:
        r, w = 'r', 'w'
    else:
        r, w = 'rb', 'wb'
    f = open(src, r)
    s = f.read()
    f.close()
    if enc is not None:
        s = codecs.encode(str(s, encoding='utf_8'), enc)
    f = open(dest, w)
    f.write(s)
    f.close()


# recursively copies a directory to 'dest'
def copyDir(src, dest):
    print('copying "%s" to "%s"' % (src, dest))
    mkdir(dest)
    for f in os.listdir(src):
        s = os.path.join(src, f)
        d = os.path.join(dest, f)
        if os.path.isfile(s):
            copyFile(s, d)
        elif os.path.isdir(s):
            copyDir(s, d)


# include GTK dependencies
build_dir = "build\\exe.win-amd64-3.4"

gnomeCopyDirs = [
    'etc',
    # 'lib',
    # 'lib\\GConf',
    'lib\\gdk-pixbuf-2.0',
    'lib\\gio',
    'lib\\girepository-1.0',
    'lib\\gtk-3.0',
    'share\\icons',
    'share\\themes'
]

for gnomeDir in gnomeCopyDirs:
    buildGnomeDir = os.path.join(build_dir, gnomeDir)
    if not os.path.isdir(buildGnomeDir):
        os.makedirs(buildGnomeDir)
    copyDir(os.path.join(gnomeSiteDir, gnomeDir), buildGnomeDir)

#
# Add all support files.
#

# syntax highlighting support
mkdir(os.path.join(build_dir, 'syntax'))
for p in glob.glob('..\\src\\usr\\share\\diffuse\\syntax\\*.syntax'):
    copyFile(p, os.path.join(build_dir, 'syntax', os.path.basename(p)), True)
copyFile('diffuserc', os.path.join(build_dir, 'diffuserc'))

# application icon
copyDir('..\\src\\usr\\share\\icons', os.path.join(build_dir, 'share\\icons'))

# translations
mkdir(os.path.join(build_dir, 'share\\locale'))
locale_dir = os.path.join(gnomeSiteDir, 'share\\locale')
for s in glob.glob('..\\po\\*.po'):
    lang = s[16:-3]
    # Diffuse localisations
    print('Compiling %s translation' % (lang, ))
    lang_dir = ''
    for p in ['locale', lang, 'LC_MESSAGES']:
        lang_dir = os.path.join(build_dir, p)
        mkdir(lang_dir)
    lang_dir = os.path.join(lang_dir, 'diffuse.mo')
    if subprocess.Popen(['msgfmt', '-o', lang_dir, s]).wait() != 0:
        raise OSError('Failed to compile "%s" into "%s".' % (s, lang_dir))
    # GTK localisations
    lang_dir = os.path.join(locale_dir, lang)
    if os.path.isdir(lang_dir):
        copyDir(lang_dir, os.path.join(build_dir, 'share\\locale', lang))
