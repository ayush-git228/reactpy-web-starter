from reactpy import component, html, hooks

@component
def Modal(children, is_open=False, on_close=None, title=None, **props):
    if not is_open:
        return None
    return html.div(
        {"class_name": "modal-overlay"},
        html.div(
            {"class_name": "modal"},
            html.div(
                {"class_name": "modal-header"},
                html.h3(title) if title else None,
                html.button({"on_click": on_close, "class_name": "modal-close"}, "x"),
            ),
            html.div({"class_name": "modal-body"}, children),
        )
    )
