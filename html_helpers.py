def build_html_table(df):
    """Generate an HTML table from a pandas DataFrame."""
    html = '<table border="1" cellspacing="0" cellpadding="4" style="border-collapse: collapse;">'
    html += "<tr>" + "".join(f"<th>{col}</th>" for col in df.columns) + "</tr>"
    for _, row in df.iterrows():
        html += "<tr>" + "".join(f"<td>{val}</td>" for val in row) + "</tr>"
    html += "</table>"
    return html


def build_html_list(df, text_format, tag="ul"):
    """Generate UL/OL lists dynamically from dataframe rows."""
    items = []
    for _, row in df.iterrows():
        text = text_format.format(**row.to_dict())
        items.append(f"<li>{text}</li>")
    return f"<{tag}>" + "".join(items) + f"</{tag}>"