import streamlit as st
from pdfminer.high_level import extract_text
from pdf2image import convert_from_bytes
import pandas as pd
from io import StringIO
def read_pdf(file):
    text = extract_text(file)
    return text

def convert_pdf_to_images(pdf_data):
    poppler_path=r"C:\Users\Dell\Downloads\Release-24.02.0-0\poppler-24.02.0\Library\bin"
    images = convert_from_bytes(pdf_data, size=(500, None),poppler_path=poppler_path)
    return images

def show_pdf_preview(images,page_no=0):
    return st.image(images[page_no],use_column_width=True)

def main():
    st.title("PDF Previewer")
    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
    if uploaded_file is not None:
        st.toast('PDF uploaded successfully !')
        pdf_data = uploaded_file.read()
        st.session_state.page_no=st.session_state.get("page_no",0)
        images = convert_pdf_to_images(pdf_data)
        text = read_pdf(uploaded_file)
        col1,col2=st.columns(2)
        with col1:
            st.write("Preview of PDF:")
            st.number_input("Page No", min_value=0, max_value=len(images)-1, value=st.session_state.page_no, key="page_no")
            show_pdf_preview(images,st.session_state.page_no)
        with col2:
            st.write("Text extracted from PDF:")
            st.text_area("", text, height=500)

if __name__ == "__main__":
    main()
