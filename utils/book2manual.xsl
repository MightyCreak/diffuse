<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE xsl:stylesheet [
 <!ENTITY app "Diffuse">
 <!ENTITY app-version "0.5.0">
 <!ENTITY app-cmd "diffuse">
 <!ENTITY date "2020-07-18">
]>
<!--
  template for translating Diffuse's help documentation to a manual page

  Copyright (C) 2010 Derrick Moser <derrick_moser@yahoo.com>
-->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

  <xsl:template match="book">
    <refentry>
      <refentryinfo>
        <date>&date;</date>
      </refentryinfo>

      <refmeta>
        <refentrytitle>&app;</refentrytitle>
        <manvolnum>1</manvolnum> <!-- 1 for commands -->
        <refmiscinfo class="version">&app-version;</refmiscinfo>
        <refmiscinfo class="software">&app-cmd;</refmiscinfo>
        <refmiscinfo class="sectdesc">&app; Manual</refmiscinfo>
      </refmeta>

      <refnamediv>
        <refname>&app-cmd;</refname>
        <refpurpose>graphical tool for merging and comparing text files</refpurpose>
      </refnamediv>

      <refsynopsisdiv>
        <cmdsynopsis>
          <command>&app-cmd;</command>
          <group>
            <arg choice="plain"><option>-h</option></arg>
            <arg choice="plain"><option>-?</option></arg>
            <arg choice="plain"><option>--help</option></arg>
            <arg choice="plain"><option>-v</option></arg>
            <arg choice="plain"><option>--version</option></arg>
          </group>
        </cmdsynopsis>
        <cmdsynopsis>
          <command>&app-cmd;</command>
          <group>
            <arg choice="plain"><option>--no-rcfile</option></arg>
            <arg choice="plain"><option>--rcfile <replaceable>file</replaceable></option></arg>
          </group>
          <group rep="repeat">
            <arg rep="repeat"><replaceable>option</replaceable></arg>
            <arg rep="repeat"><replaceable>file</replaceable></arg>
          </group>
        </cmdsynopsis>
      </refsynopsisdiv>

      <refsect1>
        <title>Description</title>
        <xsl:apply-templates select="id('introduction')/para"/>
      </refsect1>

      <refsect1>
        <title>Options</title>
        <xsl:for-each select="id('introduction-usage')">
          <xsl:for-each select="sect2">
            <refsect2>
              <xsl:apply-templates select="title"/>
              <xsl:apply-templates select="para"/>
              <xsl:apply-templates select="variablelist"/>
            </refsect2>
          </xsl:for-each>
        </xsl:for-each>
      </refsect1>

      <xsl:for-each select="chapter">
        <xsl:if test="@id != 'introduction'">
          <refsect1>
            <xsl:apply-templates select="title"/>
            <xsl:apply-templates select="para"/>
            <xsl:apply-templates select="variablelist"/>
            <xsl:for-each select="sect1">
              <refsect2>
                <xsl:apply-templates select="title"/>
                <xsl:apply-templates select="para"/>
                <xsl:apply-templates select="variablelist"/>
                <xsl:for-each select="sect2">
                  <refsect3>
                    <xsl:apply-templates select="title"/>
                    <xsl:apply-templates select="para"/>
                    <xsl:apply-templates select="variablelist"/>
                  </refsect3>
                </xsl:for-each>
              </refsect2>
            </xsl:for-each>
          </refsect1>
        </xsl:if> 
      </xsl:for-each>

      <refsect1>
        <title>Author</title>
        <xsl:apply-templates select="id('introduction-about')/para"/>
      </refsect1>

      <refsect1 id="introduction-licence">
        <title>Copying</title>
        <xsl:for-each select="id('introduction-licence')">
          <xsl:apply-templates select="para[1]"/>
        </xsl:for-each>
      </refsect1>

    </refentry>
  </xsl:template>

  <xsl:template match="node()|@*">
    <xsl:copy>
      <xsl:apply-templates select="node()|@*"/>
    </xsl:copy>
  </xsl:template>

</xsl:stylesheet>
