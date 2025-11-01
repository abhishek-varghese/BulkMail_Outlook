import pandas as pd
import win32com.client as win32
import re
import os

# --- CONFIG ---
SUBJECT = "[IMMEDIATE ACTION NEEDED] - Inaction will lead to locking of SAP IDs of your team"
SENDER_EMAIL = "UAR_Global@sanofi.com"
DATA_FILE = "data.xlsx"
HTML_TEMPLATE = "body.html"
ATTACHMENTS_DIR = "attachments"

# --- STEP 1: Load Template ---
with open(HTML_TEMPLATE, "r", encoding="utf-8") as f:
    template = f.read()

# --- STEP 2: Load Data ---
df = pd.read_excel(DATA_FILE)  # or pd.read_csv()

# --- STEP 3: Group by Email ---
grouped = df.groupby("Email")

records = []
for email, group in grouped:
    first = group.iloc[0]
    record = {
        "Email": email,
        "Name": first["Name"],
        "User": "; ".join(group["User"].unique()),
        "CCemail": ";".join(group["CCemail"].unique()),
        "reqnum": ", ".join(group["reqnum"].unique()),
        "approver": ", ".join(group["approver"].unique())
    }
    records.append(record)

print(f"Total records to send: {len(records)}")

# --- STEP 4: Setup Outlook ---
outlook = win32.Dispatch("Outlook.Application")
namespace = outlook.GetNamespace("MAPI")

# Find the sender account
account = None
for acc in namespace.Accounts:
    if acc.SmtpAddress.lower() == SENDER_EMAIL.lower():
        account = acc
        break

if not account:
    raise Exception(f"Outlook account '{SENDER_EMAIL}' not found")

# --- STEP 5: Send Mails ---
total_sent = 0
failed = []

for row in records:
    try:
        # Personalize HTML body
        body = template
        for key, value in row.items():
            pattern = r"\{\{" + re.escape(key) + r"\}\}"
            body = re.sub(pattern, str(value), body)

        mail = outlook.CreateItem(0)
        mail.Subject = SUBJECT
        mail.To = row["Email"]
        mail.CC = row["CCemail"]
        mail.HTMLBody = body
        mail.SentOnBehalfOfName = SENDER_EMAIL
        mail.SendUsingAccount = account

        # Attach inline images (CID)
        if os.path.exists(ATTACHMENTS_DIR):
            for filename in os.listdir(ATTACHMENTS_DIR):
                full_path = os.path.join(ATTACHMENTS_DIR, filename)
                attachment = mail.Attachments.Add(full_path)
                attachment.PropertyAccessor.SetProperty(
                    "http://schemas.microsoft.com/mapi/proptag/0x3712001F", filename
                )

        # mail.Send()  # Uncomment to actually send
        mail.Display()  # for manual review
        total_sent += 1
        print(f"✅ Sent: {row['Email']}")

    except Exception as e:
        print(f"❌ Failed: {row['Email']} → {e}")
        failed.append(row)

# --- STEP 6: Save Failed ---
if failed:
    pd.DataFrame(failed).to_csv("final-failures.csv", index=False)
    print(f"⚠️ {len(failed)} failed emails saved to final-failures.csv")

print(f"\nSummary: Sent={total_sent}, Failed={len(failed)}")