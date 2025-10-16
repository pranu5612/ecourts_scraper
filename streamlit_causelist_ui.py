# streamlit_causelist_ui.py

import streamlit as st
from fpdf import FPDF
from bs4 import BeautifulSoup
import os

st.set_page_config(page_title="eCourts Cause List Parser", layout="wide")
st.title("🏛️ eCourts Cause List Parser")

# Function to parse HTML and generate PDF
def parse_html_to_pdf(html_file_path):
    # Read HTML
    with open(html_file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # Example: Extract all cases (modify as per your HTML structure)
    cases = []
    for idx, row in enumerate(soup.find_all("tr")[1:], start=1):
        cols = row.find_all("td")
        if len(cols) >= 2:
            case_name = cols[0].get_text(strip=True)
            case_date = cols[1].get_text(strip=True)
            cases.append(f"Case {idx}: {case_name} ({case_date})")

    # Generate PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "eCourts Cause List", ln=True, align="C")
    pdf.ln(10)

    for case in cases:
        pdf.multi_cell(0, 10, case)

    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, "cause_list_parsed.pdf")
    pdf.output(pdf_path)
    return pdf_path

# File uploader
uploaded_file = st.file_uploader("Upload HTML Cause List", type=["html", "htm"])

if uploaded_file:
    temp_path = "temp_causelist.html"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.info("Parsing HTML and generating PDF...")
    pdf_file_path = parse_html_to_pdf(temp_path)
    st.success(f"✅ PDF generated at `{pdf_file_path}`")

    # Download button
    with open(pdf_file_path, "rb") as pdf_file:
        st.download_button(
            label="📥 Download PDF",
            data=pdf_file,
            file_name="cause_list_parsed.pdf",
            mime="application/pdf"
        )
