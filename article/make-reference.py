#!/usr/bin/python3
"""Шаблон оформления для pandoc: Times New Roman 14 пт, интервал 1,5,
абзацный отступ 1,25 см, поля 30/15/20/20 мм, A4.

usage: make-reference.py DEFAULT.docx OUT.docx
(DEFAULT.docx: pandoc -o DEFAULT.docx --print-default-data-file reference.docx)
"""
import re
import sys
import zipfile

src, dst = sys.argv[1], sys.argv[2]
FONT = ('<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" '
        'w:eastAsia="Times New Roman" w:cs="Times New Roman"/>')


def style(sid, name, ppr, rpr, kind="paragraph", based="Normal", extra=""):
    b = f'<w:basedOn w:val="{based}"/>' if based else ""
    return (f'<w:style w:type="{kind}" w:customStyle="1" w:styleId="{sid}">'
            f'<w:name w:val="{name}"/>{b}{extra}<w:qFormat/>'
            f'<w:pPr>{ppr}</w:pPr><w:rPr>{FONT}{rpr}</w:rPr></w:style>')


BODY = '<w:spacing w:before="0" w:after="0" w:line="360" w:lineRule="auto"/><w:ind w:firstLine="709"/><w:jc w:val="both"/>'
CENTER = '<w:spacing w:before="0" w:after="0" w:line="360" w:lineRule="auto"/><w:ind w:firstLine="0"/><w:jc w:val="center"/>'
BLACK = '<w:color w:val="000000"/>'
STYLES = {
    "Normal": style("Normal", "Normal", BODY, BLACK + '<w:sz w:val="28"/><w:szCs w:val="28"/><w:lang w:val="ru-RU"/>', based=None),
    "BodyText": style("BodyText", "Body Text", BODY, ""),
    "FirstParagraph": style("FirstParagraph", "First Paragraph", BODY, "", based="BodyText"),
    "Compact": style("Compact", "Compact",
                     '<w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/><w:ind w:firstLine="0"/><w:jc w:val="left"/>',
                     '<w:sz w:val="24"/><w:szCs w:val="24"/>', based="BodyText"),
    "Title": style("Title", "Title",
                   '<w:keepNext/><w:spacing w:before="240" w:after="240" w:line="276" w:lineRule="auto"/><w:ind w:firstLine="0"/><w:jc w:val="center"/>',
                   '<w:b/><w:bCs/>' + BLACK + '<w:sz w:val="32"/><w:szCs w:val="32"/>', extra='<w:next w:val="BodyText"/>'),
    "Heading1": style("Heading1", "heading 1",
                      '<w:keepNext/><w:keepLines/><w:spacing w:before="360" w:after="120" w:line="360" w:lineRule="auto"/><w:ind w:firstLine="709"/><w:jc w:val="left"/><w:outlineLvl w:val="0"/>',
                      '<w:b/><w:bCs/>' + BLACK + '<w:sz w:val="28"/><w:szCs w:val="28"/>', extra='<w:next w:val="BodyText"/>'),
    "Heading2": style("Heading2", "heading 2",
                      '<w:keepNext/><w:keepLines/><w:spacing w:before="240" w:after="60" w:line="360" w:lineRule="auto"/><w:ind w:firstLine="709"/><w:jc w:val="left"/><w:outlineLvl w:val="1"/>',
                      '<w:b/><w:bCs/><w:i/>' + BLACK + '<w:sz w:val="28"/><w:szCs w:val="28"/>', extra='<w:next w:val="BodyText"/>'),
    "Figure": style("Figure", "Figure", '<w:keepNext/>' + CENTER, ""),
    "CaptionedFigure": style("CaptionedFigure", "Captioned Figure", '<w:keepNext/>' + CENTER, "", based="Figure"),
    "ImageCaption": style("ImageCaption", "Image Caption",
                          '<w:spacing w:before="60" w:after="240" w:line="276" w:lineRule="auto"/><w:ind w:firstLine="0"/><w:jc w:val="center"/>',
                          '<w:sz w:val="24"/><w:szCs w:val="24"/>'),
    "TableCaption": style("TableCaption", "Table Caption",
                          '<w:keepNext/><w:spacing w:before="120" w:after="60"/><w:ind w:firstLine="0"/><w:jc w:val="left"/>',
                          '<w:sz w:val="24"/><w:szCs w:val="24"/>'),
    "Udc": style("Udc", "UDC", '<w:spacing w:before="0" w:after="0" w:line="360" w:lineRule="auto"/><w:ind w:firstLine="0"/><w:jc w:val="left"/>', ""),
    "Author": style("Author", "Author", CENTER, ""),
}
MONO = ('<w:rFonts w:ascii="Courier New" w:hAnsi="Courier New" w:eastAsia="Courier New" w:cs="Courier New"/>')
STYLES["VerbatimChar"] = ('<w:style w:type="character" w:customStyle="1" w:styleId="VerbatimChar">'
                          '<w:name w:val="Verbatim Char"/><w:qFormat/><w:rPr>' + MONO +
                          '<w:sz w:val="24"/><w:szCs w:val="24"/><w:lang w:val="en-US"/></w:rPr></w:style>')

zin = zipfile.ZipFile(src)
zout = zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED)
for item in zin.infolist():
    data = zin.read(item.filename)
    if item.filename == "word/styles.xml":
        xml = data.decode()
        # шрифт и размер по умолчанию, без тем оформления
        xml = re.sub(r"<w:rFonts [^>]*/>", FONT, xml)
        xml = re.sub(r'<w:color w:val="[0-9A-Fa-f]{6}"[^>]*/>', BLACK, xml)
        for sid, new in STYLES.items():
            pat = rf'<w:style [^>]*w:styleId="{sid}"[^>]*>.*?</w:style>'
            xml, n = re.subn(pat, lambda _m: new, xml, flags=re.S)
            if not n:
                xml = xml.replace("</w:styles>", new + "</w:styles>")
        # таблицы: рамка по всем ячейкам
        borders = ('<w:tblBorders>' + ''.join(
            f'<w:{e} w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
            for e in ("top", "left", "bottom", "right", "insideH", "insideV")) + '</w:tblBorders>')
        m = re.search(r'<w:style w:type="table"[^>]*w:styleId="Table".*?</w:style>', xml, re.S)
        tbl = m.group(0)
        tbl = re.sub(r"<w:tblBorders>.*?</w:tblBorders>", "", tbl, flags=re.S)
        tbl = tbl.replace("<w:tblPr>", "<w:tblPr>" + borders, 1)
        xml = xml.replace(m.group(0), tbl)
        data = xml.encode()
    elif item.filename == "word/document.xml":
        xml = data.decode()
        sect = ('<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
                '<w:pgMar w:top="1134" w:right="851" w:bottom="1134" w:left="1701" '
                'w:header="709" w:footer="709" w:gutter="0"/></w:sectPr>')
        xml = re.sub(r"<w:sectPr.*?</w:sectPr>|<w:sectPr[^>]*/>", sect, xml, flags=re.S)
        data = xml.encode()
    zout.writestr(item, data)
zout.close()
