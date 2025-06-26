from reactpy import component, html

@component
def Card(children, title=None, footer=None, **props):
    return html.div(
        {"class_name": "card", **props},
        html.div({"class_name": "card-header"}, title) if title else None,
        html.div({"class_name": "card-body"}, children),
        html.div({"class_name": "card-footer"}, footer) if footer else None,
    )
