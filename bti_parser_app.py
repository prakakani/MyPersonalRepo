
import streamlit as st
import pandas as pd
import json

# EBCDIC to ASCII map (simplified for demo)
EBCDIC_MAP = {
    'C2': 'B', 'C1': 'A', 'C3': 'C', 'C4': 'D', 'C5': 'E', 'C6': 'F',
    'C7': 'G', 'C8': 'H', 'C9': 'I', 'D1': 'J', 'D2': 'K', 'D3': 'L',
    'D4': 'M', 'D5': 'N', 'D6': 'O', 'D7': 'P', 'D8': 'Q', 'D9': 'R',
    'E2': 'S', 'E3': 'T', 'E4': 'U', 'E5': 'V', 'E6': 'W', 'E7': 'X',
    'E8': 'Y', 'E9': 'Z', 'F0': '0', 'F1': '1', 'F2': '2', 'F3': '3',
    'F4': '4', 'F5': '5', 'F6': '6', 'F7': '7', 'F8': '8', 'F9': '9',
    '40': ' ', '4B': '.', '6B': ',', '5A': '$', '7A': '#'
}

def decode_ebcdic(hex_str):
    chars = []
    for i in range(0, len(hex_str), 2):
        byte = hex_str[i:i+2].upper()
        chars.append(EBCDIC_MAP.get(byte, '.'))
    return ''.join(chars)

def parse_bti_record(raw_data):
    lines = raw_data.strip().splitlines()
    parsed = []
    for line in lines:
        if '**' in line:
            parts = line.split('**')
            hex_part = parts[0].strip().replace(' ', '')
            ascii_part = decode_ebcdic(hex_part)
            comment = parts[1].strip()
            parsed.append({
                'Hex': hex_part,
                'ASCII': ascii_part,
                'Comment': comment
            })
    return parsed

st.title("BTI D5FD Record Parser")

raw_input = st.text_area("Paste BTI D5FD Record Data Here", height=300)

if st.button("Parse Record"):
    if raw_input.strip():
        parsed_data = parse_bti_record(raw_input)
        df = pd.DataFrame(parsed_data)
        st.dataframe(df)

        json_data = json.dumps(parsed_data, indent=2)
        csv_data = df.to_csv(index=False)

        st.download_button("Download JSON", json_data, file_name="parsed_bti.json")
        st.download_button("Download CSV", csv_data, file_name="parsed_bti.csv")
    else:
        st.warning("Please paste some BTI record data.")
