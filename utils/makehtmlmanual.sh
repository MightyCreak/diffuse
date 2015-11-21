#!/bin/bash

xsltproc --nonet /usr/share/sgml/docbook/stylesheet/xsl/nwalsh/html/docbook.xsl ../src/usr/share/gnome/help/diffuse/C/diffuse.xml | sed 's/<\/head>/<link rel="stylesheet" href="style.css" type="text\/css"\/><\/head>/;s/<code class="email">.*<\/code>//' > diffuse.html
