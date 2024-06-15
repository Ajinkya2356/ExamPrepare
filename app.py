import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
from PyPDF2 import PdfReader


def extract_text_from_pdf(pdf_file_path):
    reader = PdfReader(pdf_file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


def main():
    st.title("PDF Viewer")

    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

    if uploaded_file is not None:

        col1, col2 = st.columns(2)
        with col1:
            st.write("PDF preview")
            pdf_document = fitz.open("pdf", uploaded_file.read())
            num_pages = pdf_document.page_count

            page_number = st.number_input(
                "Enter page number", min_value=1, max_value=num_pages, value=1
            )
            page = pdf_document.load_page(page_number - 1)
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            st.image(img, use_column_width=True)
        with col2:
            text = extract_text_from_pdf(uploaded_file)
            st.write("Text extracted from PDF:")
            st.text_area("", text, height=500)


if __name__ == "__main__":
    main()
