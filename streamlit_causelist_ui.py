import streamlit as st
from fpdf import FPDF
from bs4 import BeautifulSoup
import re
import io
import pandas as pd

st.title("🏛️ eCourts Cause List Parser")

# Upload HTML file
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
            # Extract text safely
            case_text = cols[0].text.strip()
            parties = cols[1].text.strip() if cols[1].text.strip() else "N/A"
            next_date = "N/A"

            # Extract next hearing date if present
            match_date = re.search(r"Next hearing date[:-]?\s*(\d{2}-\d{2}-\d{4})", case_text)
            if match_date:
                next_date = match_date.group(1)

            # Extract case number and ID
            match_case = re.match(r"(\d+)\s*\(?([A-Za-z./0-9-]*)", case_text)
            case_no = match_case.group(1) if match_case else "N/A"
            case_id = match_case.group(2) if match_case else "N/A"

            cases.append({
                "Case No": case_no,
                "Parties": parties,
                "Case ID": case_id,
                "Next Hearing": next_date
            })

    if cases:
        st.success(f"✅ Parsed {len(cases)} valid cases!")

        # Display in a table
        df = pd.DataFrame(cases)
        st.dataframe(df)

        # Generate PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for _, c in df.iterrows():
            pdf.cell(0, 8, f"Case {c['Case No']}: {c['Parties']}", ln=True)
            pdf.cell(0, 8, f"Case ID: {c['Case ID']}, Next Hearing: {c['Next Hearing']}", ln=True)
            pdf.ln(2)

        # PDF in memory
        pdf_buffer = io.BytesIO()
        pdf_bytes = pdf.output(dest='S').encode('latin1')
        pdf_buffer.write(pdf_bytes)
        pdf_buffer.seek(0)

        # Download button
        st.download_button(
            label="📥 Download Parsed Cause List PDF",
            data=pdf_buffer,
            file_name="cause_list_parsed.pdf",
            mime="application/pdf"
        )
