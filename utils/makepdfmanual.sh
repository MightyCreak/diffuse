#!/bin/bash

xsltproc /usr/share/xml/docbook/stylesheet/docbook-xsl-ns/fo/docbook.xsl ../src/usr/share/gnome/help/diffuse/C/diffuse.xml | sed 's/→/<fo:inline font-family="Symbol">&<\/fo:inline>/g' > diffuse.fo
fop -fo diffuse.fo -pdf diffuse.pdf
rm diffuse.fo
