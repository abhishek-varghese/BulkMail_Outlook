import pandas as pd
import yaml
from template_renderer import TemplateRenderer
from email_sender import EmailSender


def main():
    # Load main config
    with open("config/app_config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    data_path = config["data"]["path"]
    template_path = config["template"]["path"]
    template_config = "config/template_config.yaml"
    mail_config = config["mail"]

    # Step 1: Load Excel or CSV data
    if data_path.endswith(".xlsx"):
        df = pd.read_excel(data_path)
    else:
        df = pd.read_csv(data_path)


    # Step 2: Render email body (with placeholder tables/lists)
    renderer = TemplateRenderer(template_path, template_config)

    # Step 3: Create email sender
    sender = EmailSender(
        from_address=mail_config["from"],
        subject=mail_config["subject"],
        attachments_path=mail_config.get("attachments_path", "")
    )

    # Step 4: Loop through data and send mails
    for _, row in df.iterrows():
        html_body = renderer.render(df)  # render once from grouped data
        # sender.send_mail(to=row["Email"], cc=row.get("CCemail", ""), body=html_body)
        sender.send_mail(to="abhishek.varghese@syndigo.com", cc="", body=html_body)

    print("✅ All emails processed successfully.")


if __name__ == "__main__":
    main()