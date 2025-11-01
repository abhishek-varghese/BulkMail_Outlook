import pandas as pd
import yaml

from mail_manager import MailManager
from template_renderer import TemplateRenderer
from email_sender import EmailSender


def main():
    # Load main config
    with open("config/app_config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    data_path = config["data"]["path"]
    email_template = config["email_template"]["path"]
    template_config = "config/template_config.yaml"
    mail_config = config["mail"]

    # Step 1: Load Excel or CSV data
    if data_path.endswith(".xlsx"):
        df = pd.read_excel(data_path)
    else:
        df = pd.read_csv(data_path)


    # Step 2: Render email body (with placeholder tables/lists)
    renderer = TemplateRenderer(email_template, template_config)

    # Step 3: Create email sender
    sender = EmailSender(
        from_address=mail_config["from"],
        subject=mail_config["subject"],
        attachments_path=mail_config.get("attachments_path", "")
    )

    mail_manager = MailManager(
        email_sender=sender,
        template_renderer=renderer,
        template_config=template_config
    )

    mail_manager.start(df)

if __name__ == "__main__":
    main()