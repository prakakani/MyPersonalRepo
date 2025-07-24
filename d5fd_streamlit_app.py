import streamlit as st
from d5fd_file_parser import D5FDFileParser
import io

st.title("BTI D5FD Record Parser")

parser = D5FDFileParser()

input_method = st.radio("Choose input method:", ("Upload hex file", "Paste hex data"))

hex_data = ""

if input_method == "Upload hex file":
    uploaded_file = st.file_uploader("Upload a hex data file", type=["txt"])
    if uploaded_file is not None:
        hex_data = uploaded_file.read().decode("utf-8").strip()

elif input_method == "Paste hex data":
    hex_data = st.text_area("Paste your hex data here", height=300).strip()

if hex_data:
    output_buffer = io.StringIO()
    parser.parse_record_to_file(hex_data, output_buffer)
    parsed_output = output_buffer.getvalue()

    st.subheader("Parsed Output")
    st.text_area("Results", parsed_output, height=500)

    st.download_button("Download Parsed Output", parsed_output, file_name="parsed_output.txt", mime="text/plain")
