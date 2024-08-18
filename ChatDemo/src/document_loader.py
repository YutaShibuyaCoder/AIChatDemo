import PyPDF2
import docx2txt

def load_document(file):
    if file.name.endswith('.pdf'):
        return load_pdf(file)
    elif file.name.endswith('.docx'):
        return load_docx(file)
    else:
        raise ValueError("サポートされていないファイル形式です。PDFまたはDOCXファイルをアップロードしてください。")

def load_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def load_docx(file):
    return docx2txt.process(file)