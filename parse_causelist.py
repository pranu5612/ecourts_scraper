from bs4 import BeautifulSoup
from fpdf import FPDF
import os

# Open and read the HTML file
with open("sample_causelist.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Parse HTML with BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# Find the table
table = soup.find("table", {"id": "cause-list"})

# Extract rows
rows = table.find_all("tr")[1:]  # skip header row

# Store cause list
cause_list = []
for row in rows:
    cols = row.find_all("td")
    case_no = cols[0].text.strip()
    petitioner = cols[1].text.strip()
    respondent = cols[2].text.strip()
    date = cols[3].text.strip()
    cause_list.append(f"Case {case_no}: {petitioner} vs. {respondent} ({date})")

# Print to check
for case in cause_list:
    print(case)

# --- Create outputs folder if not exist ---
os.makedirs("outputs", exist_ok=True)

# Create PDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

# Add each case to PDF
for case in cause_list:
    pdf.multi_cell(0, 10, case)

pdf_output_path = "outputs/cause_list_parsed.pdf"
pdf.output(pdf_output_path)
print(f"✅ PDF saved at {pdf_output_path}")
