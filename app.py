import streamlit as st
from PIL import Image
from io import BytesIO
import pdf2image
from pypdf import PdfReader


def extract_text_from_pdf(pdf_file_path):
    reader = PdfReader(pdf_file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


def convert_pdf_to_images(pdf_data):
    images = pdf2image.convert_from_bytes(pdf_data)
    return images


def show_preview_image(images, page_no):
    st.image(images[page_no], use_column_width=True)


def main():
    st.title("PDF Previewer")
    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
    if uploaded_file is not None:
        if st.session_state.get("file_just_uploaded", True):
            st.toast("PDF uploaded successfully !")
            st.session_state.file_just_uploaded = False
        pdf_data = uploaded_file.read()
        st.session_state.page_no = st.session_state.get("page_no", 0)
        images = convert_pdf_to_images(pdf_data)
        text = extract_text_from_pdf(uploaded_file)
        col1, col2 = st.columns(2)
        with col1:
            st.write("Preview of PDF:")
            st.number_input(
                "Page No",
                min_value=0,
                max_value=len(images) - 1,
                value=st.session_state.page_no,
                key="page_no",
            )
            show_preview_image(images, st.session_state.page_no)
        with col2:
            st.write("Text extracted from PDF:")
            st.text_area("", text, height=500)


if __name__ == "__main__":
    main()
