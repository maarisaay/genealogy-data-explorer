import streamlit as st

from src.gedcom_parser import parse_gedcom


st.set_page_config(
    page_title="Genealogy Data Explorer",
    page_icon="🌳",
    layout="wide",
)

st.title("Genealogy Data Explorer")
st.write("Upload a GEDCOM file to explore its contents.")

uploaded_file = st.file_uploader(
    "Upload GEDCOM file",
    type=["ged"],
)

encoding_options = {
    "Auto detect": None,
    "UTF-8": "utf-8",
    "Windows-1250 (Central European)": "cp1250",
    "Windows-1252 (Western European)": "cp1252",
    "ISO-8859-2 (Central European)": "iso-8859-2",
    "UTF-16": "utf-16",
}

selected_encoding = st.selectbox(
    "File encoding",
    options=encoding_options.keys(),
)

if uploaded_file is not None:
    people = parse_gedcom(
        uploaded_file,
        encoding=encoding_options[selected_encoding],
    )

    st.success(f"Loaded {len(people)} people.")