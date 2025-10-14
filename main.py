import json
import os
from datetime import datetime, timedelta

print("🔍 Welcome to eCourts Case Checker")
print("-----------------------------------")

# Step 1: Take CNR Number from user
cnr_number = input("Enter your CNR Number (Example: MHAU010123452018): ").strip()

# Step 2: Ask if user wants to check today or tomorrow
choice = input("Check listing for (1) Today or (2) Tomorrow? Enter 1 or 2: ").strip()

if choice == "1":
    listed_when = "Today"
elif choice == "2":
    listed_when = "Tomorrow"
else:
    listed_when = "Unknown"

# Step 3: Simulate sample data
sample_case_data = {
    "CNR": cnr_number,
    "Court Name": "District Civil Court, Mumbai",
    "Serial Number": "12",
    "Listed Date": listed_when,
    "PDF Available": "Yes (sample.pdf)"
}

# Step 4: Show result on console
print(f"\n✅ Case found! (Sample Data Used for {listed_when})")
for k, v in sample_case_data.items():
    print(f"{k}: {v}")

# Step 5: Save JSON & TXT
output_dir = "outputs"
os.makedirs(output_dir, exist_ok=True)

json_file = os.path.join(output_dir, f"case_{cnr_number}.json")
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(sample_case_data, f, indent=4)
print(f"\n💾 JSON saved at: {json_file}")

txt_file = os.path.join(output_dir, f"case_{cnr_number}.txt")
with open(txt_file, "w", encoding="utf-8") as f:
    for k, v in sample_case_data.items():
        f.write(f"{k}: {v}\n")
print(f"💾 TXT saved at: {txt_file}")
# Step 6: Ask if user wants to download today's cause list
cause_list_choice = input("\nDo you want to download today's cause list? (y/n): ").strip().lower()

if cause_list_choice == "y":
    # Sample cause list data
    cause_list = [
        {"Serial": 1, "CNR": "MHAU010123452018", "Court": "District Civil Court, Mumbai"},
        {"Serial": 2, "CNR": "MHAU010123452019", "Court": "District Civil Court, Mumbai"},
        {"Serial": 3, "CNR": "MHAU010123452020", "Court": "District Civil Court, Mumbai"},
    ]

    # Save as JSON
    cause_json_file = os.path.join(output_dir, f"cause_list_today.json")
    with open(cause_json_file, "w", encoding="utf-8") as f:
        json.dump(cause_list, f, indent=4)
    
    # Save as TXT
    cause_txt_file = os.path.join(output_dir, f"cause_list_today.txt")
    with open(cause_txt_file, "w", encoding="utf-8") as f:
        for item in cause_list:
            f.write(f"Serial: {item['Serial']}, CNR: {item['CNR']}, Court: {item['Court']}\n")
    
    print(f"\n💾 Cause list saved as JSON: {cause_json_file}")
    print(f"💾 Cause list saved as TXT: {cause_txt_file}")
else:
    print("\nSkipped downloading cause list.")

