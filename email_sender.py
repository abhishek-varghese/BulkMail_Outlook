import os
import win32com.client


class EmailSender:
    def __init__(self, from_address, subject, attachments_path=""):
        print("Initializing EmailSender")
        self.outlook = win32com.client.Dispatch("Outlook.Application")
        print("Outlook.Application is ready")
        self.from_address = from_address
        self.subject = subject
        self.attachments_path = attachments_path

    def send_mail(self, to, cc, body):
        mail = self.outlook.CreateItem(0)
        mail.To = to
        mail.CC = cc
        mail.Subject = self.subject
        mail.HTMLBody = body
        mail.SentOnBehalfOfName = self.from_address

        # Attach images if available
        if os.path.isdir(self.attachments_path):
            for file in os.listdir(self.attachments_path):
                full_path = os.path.join(self.attachments_path, file)
                if os.path.isfile(full_path):
                    attachment = mail.Attachments.Add(full_path)
                    attachment.PropertyAccessor.SetProperty(
                        "http://schemas.microsoft.com/mapi/proptag/0x3712001F", file
                    )

        mail.Display()  # change to mail.Send() to actually send
        print(f"📧 Displayed email to: {to}")