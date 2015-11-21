Below are instructions for building a Windows installer for Diffuse.

Prerequisites:

1) Python >= 2.4
   http://www.python.org/

   Python 3.0 has not been tested as no official PyGTK package for Python 3.0
   has been released at the time of writing.

2) PyGTK >= 2.10
   http://www.pygtk.org/

   PyGTK has its own set of dependencies.  GTK+ runtime, PyCairo, and PyGObject
   should be installed in that order prior to installing PyGTK.  If the GTK+
   runtime installer did not set the GTK_BASEPATH environment variable,
   manually set it to the installation path.  Also, add the 'bin' and 'lib'
   directories to the PATH environment variable.

3) py2exe
   http://www.py2exe.org/

4) xsltproc (use Cygwin installer)

5) docbook-xsl (use Cygwin installer)

6) ADD_PATH
   http://blog.barisione.org/projects/#add_path

   Unzip the package and set the environment variable ADD_PATH_HOME to the full
   path of the root directory.

7) GNU gettext (use Cygwin installer; install the development package)

8) Inno Setup
   http://jrsoftware.org/isinfo.php

   You may need to manually update the PATH environment variable to run
   ISCC.exe from the command line.

Building the installer:

After all of the prerequisites are installed, run the build.py Python script to
create a Windows installer for Diffuse.  If successful, an installer will be
created in the current directory named diffuse-{version}.{platform}.exe.
