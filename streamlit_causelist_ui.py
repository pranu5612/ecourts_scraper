import streamlit as st
from fpdf import FPDF
from bs4 import BeautifulSoup
import re
import pandas as pd
import io
from datetime import datetime

st.set_page_config(page_title="eCourts Cause List Parser", layout="wide")

st.title("🏛️ eCourts Cause List Parser")

# Upload HTML file
uploaded_file = st.file_uploader("Upload HTML Cause List", type=["html", "htm"])

if uploaded_file:
    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(uploaded_file, "html.parser")

    # Collect all table rows
    rows = soup.find_all('tr')
    cases = []

    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 2:
            case_text = cols[0].text.strip()
            parties = cols[1].text.strip() if cols[1].text.strip() else "N/A"
            next_date = "N/A"

            # Extract next hearing date from text if present
            match = re.search(r"Next hearing date[:-]?\s*(\d{2}-\d{2}-\d{4})", case_text)
            if match:
                next_date = match.group(1)

            # Extract case number and ID
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

        # Display cases in table
        df_cases = pd.DataFrame(cases)
        st.dataframe(df_cases)

        # Generate PDF in memory
        pdf = FPDF()
        pdf.add_page()

        # Add Unicode-friendly font (DejaVu)
        pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
        pdf.set_font("DejaVu", "B", 16)
        pdf.cell(0, 10, "eCourts Cause List", ln=True, align="C")
        pdf.set_font("DejaVu", size=12)
        pdf.cell(0, 8, f"Generated on: {datetime.now().strftime('%d-%m-%Y %H:%M')}", ln=True)
        pdf.ln(5)

        # Table headers
        pdf.set_font("DejaVu", "B", 12)
        pdf.cell(25, 8, "Case No", border=1)
        pdf.cell(90, 8, "Parties", border=1)
        pdf.cell(40, 8, "Next Hearing", border=1)
        pdf.cell(35, 8, "Case ID", border=1)
        pdf.ln()

        # Table rows
        pdf.set_font("DejaVu", size=12)
        for c in cases:
            pdf.cell(25, 8, c["Case No"], border=1)
            pdf.cell(90, 8, c["Parties"][:50], border=1)  # Truncate long text
            pdf.cell(40, 8, c["Next Hearing"], border=1)
            pdf.cell(35, 8, c["Case ID"], border=1)
            pdf.ln()

        # Save PDF in memory
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
