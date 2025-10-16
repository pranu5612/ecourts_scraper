import streamlit as st
from fpdf import FPDF
from datetime import date
import os

uploaded_file = st.file_uploader("Upload HTML Cause List", type="html")

# --- Create outputs folder if it doesn't exist ---
os.makedirs("outputs", exist_ok=True)

# --- Streamlit Page Config ---
st.set_page_config(page_title="eCourts Cause List Downloader", page_icon="🏛️")

st.title("🏛️ eCourts Cause List Downloader")
st.write("Fetch and download cause lists directly from eCourts websites.")

# --- User Input Section ---
st.subheader("📋 Court Selection")

state = st.text_input("Enter State Name (e.g., Delhi, Maharashtra)")
district = st.text_input("Enter District Name (e.g., New Delhi, Mumbai)")
court_complex = st.text_input("Enter Court Complex Name")
court_name = st.text_input("Enter Court Name")

selected_date = st.date_input("Select Date", value=date.today())

# --- Action Button ---
if st.button("Download Cause List"):
    if not all([state, district, court_complex, court_name]):
        st.error("⚠️ Please fill in all details before proceeding.")
    else:
        st.info(f"Generating PDF for **{court_name}**, {district}, {state} ({selected_date})...")

        # --- Dummy cause list ---
        cause_list_text = f"""
Cause List - {selected_date}
State: {state}
District: {district}
Court Complex: {court_complex}
Court: {court_name}

Case 1: State vs. Ramesh
Case 2: Anita vs. Rohan
Case 3: Rajesh vs. Municipal Corporation
"""

        # --- Save as PDF ---
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
        pdf.set_font("DejaVu", size=12)
        pdf.set_auto_page_break(auto=True, margin=15)

        for line in cause_list_text.strip().split("\n"):
            pdf.multi_cell(0, 10, txt=line)

        pdf_output_path = "outputs/cause_list_ui.pdf"
        pdf.output(pdf_output_path)

        st.success("✅ PDF generated successfully!")
        with open(pdf_output_path, "rb") as f:
            st.download_button(
                "📥 Download PDF",
                data=f,
                file_name="cause_list_ui.pdf"
            )
