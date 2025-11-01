import re

import yaml


class TemplateRenderer:
    def __init__(self, email_template, template_config, ):
        with open(email_template, "r", encoding="utf-8") as f:
            self.email_template = f.read()
        with open(template_config, "r", encoding="utf-8") as f:
            self.template_config = yaml.safe_load(f)

    def render(self, df):
        html = self.email_template

        placeholders = re.findall(r"{{(.*?)}}", html)
        for ph in placeholders:
            ph = ph.strip()
            conf = self.template_config.get("placeholders", {}).get(ph)

            content = ""
            if not conf:
                print(ph)
                content = str(df[ph].iloc[0])
                # series to join to list.
                # content = ", ".join(df[ph].dropna().astype(str).unique())
            elif ph in self.template_config["placeholders"]:
                content = self._generate_content(df, conf)
            else:
                print(f"⚠️ No config found for placeholder: {ph}")


            print(content)
            html = html.replace(f"{{{{{ph}}}}}", content)

        return html

    def _generate_content(self, df, conf):
        group_by = conf.get("group_by", [])
        agg = conf.get("agg", {})
        ptype = conf.get("type", "table")

        grouped_df = df
        if group_by and agg:
            grouped_df = df.groupby(group_by).agg(agg).reset_index()

        if ptype == "table":
            cols = conf.get("columns", list(grouped_df.columns))
            return self._build_html_table(grouped_df[cols])

        elif ptype == "list":
            text_fmt = conf.get("text_format", "")
            tag = conf.get("format", "ul")
            return self._build_html_list(grouped_df, text_fmt, tag)

        else:
            return f"<p>Unknown placeholder type: {ptype}</p>"

    def _build_html_table(self, df):
        """Generate an HTML table from a pandas DataFrame."""
        html = '<table border="1" cellspacing="0" cellpadding="4" style="border-collapse: collapse;">'
        html += "<tr>" + "".join(f"<th>{col}</th>" for col in df.columns) + "</tr>"
        for _, row in df.iterrows():
            html += "<tr>" + "".join(f"<td>{val}</td>" for val in row) + "</tr>"
        html += "</table>"
        return html

    def _build_html_list(self, df, text_format, tag="ul"):
        """Generate UL/OL lists dynamically from dataframe rows."""
        items = []
        for _, row in df.iterrows():
            text = text_format.format(**row.to_dict())
            items.append(f"<li>{text}</li>")
        return f"<{tag}>" + "".join(items) + f"</{tag}>"