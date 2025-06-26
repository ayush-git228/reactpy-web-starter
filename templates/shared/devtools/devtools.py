from reactpy import component, html

@component
def DevToolsPanel(state):
    return html.div(
        {"style": {
            "position": "fixed", "bottom": "0", "right": "0",
            "background": "#fff", "padding": "10px", "border": "1px solid #ccc"
        }},
        html.pre(str(state))
    )
