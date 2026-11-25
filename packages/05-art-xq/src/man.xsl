<?xml version="1.0" encoding="UTF-8"?>
<!-- Преобразование простого XML-описания в страницу man (troff) -->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="text" encoding="UTF-8"/>
  <xsl:strip-space elements="*"/>

  <xsl:template match="/manpage">
    <xsl:text>.TH </xsl:text>
    <xsl:value-of select="translate(@name, 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')"/>
    <xsl:text> </xsl:text><xsl:value-of select="@section"/>
    <xsl:text> "</xsl:text><xsl:value-of select="@date"/><xsl:text>"&#10;</xsl:text>
    <xsl:text>.SH NAME&#10;</xsl:text>
    <xsl:value-of select="@name"/><xsl:text> \- </xsl:text>
    <xsl:value-of select="normalize-space(purpose)"/><xsl:text>&#10;</xsl:text>
    <xsl:text>.SH SYNOPSIS&#10;.B </xsl:text>
    <xsl:value-of select="normalize-space(synopsis)"/><xsl:text>&#10;</xsl:text>
    <xsl:text>.SH DESCRIPTION&#10;</xsl:text>
    <xsl:for-each select="description/para">
      <xsl:if test="position() &gt; 1"><xsl:text>.PP&#10;</xsl:text></xsl:if>
      <xsl:value-of select="normalize-space(.)"/><xsl:text>&#10;</xsl:text>
    </xsl:for-each>
    <xsl:text>.SH EXAMPLE&#10;.nf&#10;</xsl:text>
    <xsl:value-of select="normalize-space(example)"/>
    <xsl:text>&#10;.fi&#10;</xsl:text>
  </xsl:template>
</xsl:stylesheet>
