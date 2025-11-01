import os
import win32com.client as win32

class OutlookMailer:
    def __init__(self, sender_email):
        self.outlook = win32.Dispatch("Outlook.Application")
        self.namespace = self.outlook.GetNamespace("MAPI")
        self.account = next((a for a in self.namespace.Accounts if a.SmtpAddress == sender_email), None)
        if not self.account:
            raise ValueError(f"Outlook account '{sender_email}' not found.")
        self.sender_email = sender_email
        print(f"Using Outlook account: {self.account.DisplayName}")

    def send_mail(self, to, cc, subject, html_body, attachments_path=None):
        mail = self.outlook.CreateItem(0)
        mail.To = to
        mail.CC = cc
        mail.Subject = subject
        mail.HTMLBody = html_body
        mail.SentOnBehalfOfName = self.sender_email
        mail.SendUsingAccount = self.account

        if attachments_path and os.path.exists(attachments_path):
            for file in os.listdir(attachments_path):
                if file.lower().endswith((".jpg", ".png", ".gif")):
                    attachment = mail.Attachments.Add(os.path.join(attachments_path, file))
                    attachment.PropertyAccessor.SetProperty(
                        "http://schemas.microsoft.com/mapi/proptag/0x3712001F",
                        file
                    )

        mail.Display()  # change to mail.Send() after testing
        print(f"Mail displayed for: {to}")