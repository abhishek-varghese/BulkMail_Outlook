import yaml
import re
from html_helpers import build_html_table, build_html_list


class TemplateRenderer:
    def __init__(self, template_path, config_path):
        with open(template_path, "r", encoding="utf-8") as f:
            self.template = f.read()
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)

    def render(self, df):
        html = self.template
        placeholders = re.findall(r"{{(.*?)}}", html)

        for ph in placeholders:
            ph = ph.strip()
            conf = self.config.get("placeholders", {}).get(ph)
            if not conf:
                print(f"⚠️ No config found for placeholder: {ph}")
                continue

            content = self._generate_content(df, conf)
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
            return build_html_table(grouped_df[cols])

        elif ptype == "list":
            text_fmt = conf.get("text_format", "")
            tag = conf.get("format", "ul")
            return build_html_list(grouped_df, text_fmt, tag)

        else:
            return f"<p>Unknown placeholder type: {ptype}</p>"