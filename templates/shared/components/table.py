from reactpy import component, html

@component
def Table(headers, rows, **props):
    return html.table(
        {"class_name": "table", **props},
        html.thead(
            html.tr([html.th(h) for h in headers])
        ),
        html.tbody(
            [html.tr([html.td(cell) for cell in row]) for row in rows]
        )
    )
