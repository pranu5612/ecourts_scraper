import streamlit as st
from fpdf import FPDF
from bs4 import BeautifulSoup
import os

# --- Create outputs folder if it doesn't exist ---
os.makedirs("outputs", exist_ok=True)

# --- Streamlit Page Config ---
st.set_page_config(page_title="eCourts Cause List Downloader", page_icon="🏛️")

st.title("🏛️ eCourts Cause List Downloader")
st.write("Upload an HTML cause list or fetch from eCourts and download as PDF.")

# --- File Uploader ---
uploaded_file = st.file_uploader("Upload HTML Cause List", type="html")

# --- User Input Section ---
st.subheader("📋 Court Selection")
state = st.text_input("Enter State Name (e.g., Delhi, Maharashtra)")
district = st.text_input("Enter District Name (e.g., New Delhi, Mumbai)")
court_complex = st.text_input("Enter Court Complex Name")
court_name = st.text_input("Enter Court Name")

# --- Action Button ---
if st.button("Generate PDF"):
    if not all([state, district, court_complex, court_name]):
        st.error("⚠️ Please fill in all details before proceeding.")
    elif uploaded_file is None:
        st.error("⚠️ Please upload an HTML cause list file.")
    else:
        st.info(f"Generating PDF for **{court_name}**, {district}, {state}...")

        # --- Parse HTML ---
        html_content = uploaded_file.read()
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Try to find table with id 'cause-list', fallback to first table
        table = soup.find("table", {"id": "cause-list"}) or soup.find("table")
        cause_list = []
        if table:
            rows = table.find_all("tr")[1:]  # skip header
            for row in rows:
                cols = row.find_all("td")
                if len(cols) >= 4:
                    case_no = cols[0].text.strip()
                    petitioner = cols[1].text.strip()
                    respondent = cols[2].text.strip()
                    date = cols[3].text.strip()
                    cause_list.append(f"Case {case_no}: {petitioner} vs. {respondent} ({date})")
        else:
            st.error("⚠️ No table found in the uploaded HTML.")
        
        # --- Add header info ---
        cause_list.insert(0, f"Court: {court_name}")
        cause_list.insert(0, f"Court Complex: {court_complex}")
        cause_list.insert(0, f"District: {district}")
        cause_list.insert(0, f"State: {state}")
        cause_list.insert(0, "Cause List")

        # --- Save as PDF ---
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
        pdf.set_font("DejaVu", size=12)
        pdf.set_auto_page_break(auto=True, margin=15)

        for line in cause_list:
            pdf.multi_cell(0, 10, line)

        pdf_output_path = "outputs/cause_list_uploaded.pdf"
        pdf.output(pdf_output_path)

        st.success("✅ PDF generated successfully!")
        with open(pdf_output_path, "rb") as f:
            st.download_button(
                "📥 Download PDF",
                data=f,
                file_name="cause_list_uploaded.pdf"
            )
