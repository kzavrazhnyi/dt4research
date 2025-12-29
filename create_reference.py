from pathlib import Path
import zipfile
from datetime import datetime

base = Path("research/00_setup")
base.mkdir(parents=True, exist_ok=True)

doc_path = base / "reference.docx"
created = datetime(2025, 11, 8, 0, 0, 0)
content_types = """<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n<Types xmlns=\"http://schemas.openxmlformats.org/package/2006/content-types\">\n    <Default Extension=\"rels\" ContentType=\"application/vnd.openxmlformats-package.relationships+xml\"/>\n    <Default Extension=\"xml\" ContentType=\"application/xml\"/>\n    <Override PartName=\"/word/document.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml\"/>\n    <Override PartName=\"/docProps/core.xml\" ContentType=\"application/vnd.openxmlformats-package.core-properties+xml\"/>\n    <Override PartName=\"/docProps/app.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.extended-properties+xml\"/>\n    <Override PartName=\"/word/styles.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml\"/>\n</Types>\n"""
rels = """<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n<Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\">\n    <Relationship Id=\"rId1\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument\" Target=\"word/document.xml\"/>\n    <Relationship Id=\"rId2\" Type=\"http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties\" Target=\"docProps/core.xml\"/>\n    <Relationship Id=\"rId3\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties\" Target=\"docProps/app.xml\"/>\n</Relationships>\n"""
core = f"""<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n<cp:coreProperties xmlns:cp=\"http://schemas.openxmlformats.org/package/2006/metadata/core-properties\"\n    xmlns:dc=\"http://purl.org/dc/elements/1.1/\"\n    xmlns:dcterms=\"http://purl.org/dc/terms/\"\n    xmlns:dcmitype=\"http://purl.org/dc/dcmitype/\"\n    xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">\n    <dc:title>Research Reference Template</dc:title>\n    <dc:creator>dt4research</dc:creator>\n    <cp:lastModifiedBy>dt4research</cp:lastModifiedBy>\n    <dcterms:created xsi:type=\"dcterms:W3CDTF\">{created.isoformat()}Z</dcterms:created>\n    <dcterms:modified xsi:type=\"dcterms:W3CDTF\">{created.isoformat()}Z</dcterms:modified>\n</cp:coreProperties>\n"""
app = """<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n<Properties xmlns=\"http://schemas.openxmlformats.org/officeDocument/2006/extended-properties\"\n    xmlns:vt=\"http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes\">\n    <Application>dt4research</Application>\n</Properties>\n"""
doc_xml = """<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n<w:document xmlns:w=\"http://schemas.openxmlformats.org/wordprocessingml/2006/main\"\n    xmlns:r=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships\">\n  <w:body>\n    <w:p>\n      <w:r>\n        <w:t>Research reference template (Шаблон стилів)</w:t>\n      </w:r>\n    </w:p>\n    <w:sectPr>\n      <w:pgSz w:w=\"12240\" w:h=\"15840\"/>\n      <w:pgMar w:top=\"1440\" w:right=\"1440\" w:bottom=\"1440\" w:left=\"1440\" w:header=\"720\" w:footer=\"720\" w:gutter=\"0\"/>\n    </w:sectPr>\n  </w:body>\n</w:document>\n"""
styles = """<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n<w:styles xmlns:w=\"http://schemas.openxmlformats.org/wordprocessingml/2006/main\">\n  <w:style w:type=\"paragraph\" w:default=\"1\" w:styleId=\"Normal\">\n    <w:name w:val=\"Normal\"/>\n    <w:rPr/>\n  </w:style>\n  <w:style w:type=\"character\" w:default=\"1\" w:styleId=\"DefaultParagraphFont\">\n    <w:name w:val=\"Default Paragraph Font\"/>\n  </w:style>\n  <w:style w:type=\"table\" w:default=\"1\" w:styleId=\"TableNormal\">\n    <w:name w:val=\"Normal Table\"/>\n  </w:style>\n  <w:style w:type=\"numbering\" w:default=\"1\" w:styleId=\"NoList\">\n    <w:name w:val=\"No List\"/>\n  </w:style>\n</w:styles>\n"""
doc_rels = """<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n<Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\"/>\n"""

with zipfile.ZipFile(doc_path, "w") as doc:
    doc.writestr("[Content_Types].xml", content_types)
    doc.writestr("_rels/.rels", rels)
    doc.writestr("docProps/core.xml", core)
    doc.writestr("docProps/app.xml", app)
    doc.writestr("word/document.xml", doc_xml)
    doc.writestr("word/_rels/document.xml.rels", doc_rels)
    doc.writestr("word/styles.xml", styles)

print(f"Created {doc_path}")
