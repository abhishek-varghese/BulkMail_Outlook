import yaml
class MailManager:
    def __init__(self, email_sender, template_renderer, template_config):
        self.email_sender = email_sender
        self.template_renderer = template_renderer
        with open(template_config, "r", encoding="utf-8") as f:
            self.template_config = yaml.safe_load(f)

    def start(self, df):
        data_group_by = self.template_config["data_group_by"]
        grouped_df = df.groupby(data_group_by)
        print(grouped_df)

        # Step 4: Loop through data and send mails
        for group, row in grouped_df:
            print("printing html body")
            html_body = self.template_renderer.render(row)  # render once from grouped data
            print(html_body)

            mail_to = str(group)
            mail_cc = ",".join(row["CCemail"].dropna().astype(str).unique())
            self.email_sender.send_mail(to=mail_to, cc=mail_cc, body=html_body)
            # sender.send_mail(to="abhishek.varghese@syndigo.com", cc="", body=html_body)
