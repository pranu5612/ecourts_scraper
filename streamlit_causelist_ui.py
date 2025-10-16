import streamlit as st
from fpdf import FPDF
from bs4 import BeautifulSoup
import re
import io
import os

st.title("🏛️ eCourts Cause List Parser")

uploaded_file = st.file_uploader("Upload HTML Cause List", type=["html", "htm"])

if uploaded_file:
    # Read HTML
    soup = BeautifulSoup(uploaded_file, "html.parser")

    # Collect all rows from table
    rows = soup.find_all('tr')
    cases = []

    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 2:
            case_text = cols[0].text.strip()
            parties = cols[1].text.strip() if cols[1].text.strip() else "N/A"
            next_date = "N/A"

            match = re.search(r"Next hearing date[:-]?\s*(\d{2}-\d{2}-\d{4})", case_text)
            if match:
                next_date = match.group(1)

            match2 = re.match(r"(\d+)\s*\(?([A-Za-z./0-9-]*)", case_text)
            case_no = match2.group(1) if match2 else "N/A"
            case_id = match2.group(2) if match2 else "N/A"

            cases.append({
                "Case No": case_no,
                "Parties": parties,
                "Case ID": case_id,
                "Next Hearing": next_date
            })

    if cases:
        st.success(f"✅ Parsed {len(cases)} cases!")

        # Display in Streamlit
        for c in cases:
            st.write(f"Case {c['Case No']}: {c['Parties']}")
            st.write(f"Case ID: {c['Case ID']}, Next Hearing: {c['Next Hearing']}")
            st.markdown("---")

        # Generate PDF in memory
        pdf = FPDF()
        pdf.add_page()
        # Use built-in font "Arial" instead of DejaVu
        pdf.set_font("Arial", "B", 12)

        for c in cases:
            pdf.cell(0, 8, f"Case {c['Case No']}: {c['Parties']}", ln=True)
            pdf.cell(0, 8, f"Case ID: {c['Case ID']}, Next Hearing: {c['Next Hearing']}", ln=True)
            pdf.ln(2)

        pdf_buffer = io.BytesIO()
        pdf.output(pdf_buffer)
        pdf_buffer.seek(0)

        # Provide download button
        st.download_button(
            label="📥 Download Parsed Cause List PDF",
            data=pdf_buffer,
            file_name="cause_list_parsed.pdf",
            mime="application/pdf"
        )
