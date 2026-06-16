import zipfile
import xml.etree.ElementTree as ET
import os

def read_docx(file_path):
    # docx is a zip file, we can extract word/document.xml
    namespaces = {
        'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    }
    
    texts = []
    with zipfile.ZipFile(file_path) as docx:
        tree = ET.fromstring(docx.read('word/document.xml'))
        for paragraph in tree.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
            p_text = []
            for run in paragraph.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'):
                if run.text:
                    p_text.append(run.text)
            if p_text:
                texts.append("".join(p_text))
            else:
                texts.append("")
    return "\n".join(texts)

if __name__ == "__main__":
    prd_path = r"c:\Users\saikr\.gemini\antigravity\scratch\upi-merchant-category-pulse-dashboard\UPI_Pulse_Dashboard_PRD.docx"
    content = read_docx(prd_path)
    output_path = r"c:\Users\saikr\.gemini\antigravity\scratch\upi-merchant-category-pulse-dashboard\prd_content.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Successfully extracted PRD text to prd_content.txt")
