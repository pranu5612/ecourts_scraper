import streamlit as st
from fpdf import FPDF
from bs4 import BeautifulSoup

st.title("🏛️ eCourts Cause List Parser - Full Details PDF")

# Upload HTML file
uploaded_file = st.file_uploader("Upload HTML Cause List", type=["html", "htm"])

if uploaded_file is not None:
    # Read uploaded HTML
    html_content = uploaded_file.read()
    
    # Parse HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Create PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    # Extract case information (customize according to your HTML structure)
    cases = soup.find_all("tr")  # Assuming each case is in a <tr> tag
    case_count = 0
    for case in cases:
        text = case.get_text(separator=" ", strip=True)
        if text:
            pdf.multi_cell(0, 8, text)
            pdf.ln(2)
            case_count += 1

    if case_count == 0:
        st.warning("⚠️ No cases found in the uploaded HTML!")
    else:
        # Save PDF with the same name as uploaded HTML
        pdf_name = uploaded_file.name.replace(".html", ".pdf").replace(".htm", ".pdf")
        pdf.output(pdf_name)
        st.success(f"✅ Parsed {case_count} cases! PDF saved as `{pdf_name}`")
        st.download_button("📥 Download PDF", data=open(pdf_name, "rb"), file_name=pdf_name)
