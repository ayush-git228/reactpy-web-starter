from reactpy import component, html, hooks
from ..shared.components.card import Card
from ..shared.components.button import Button
from ..shared.components.modal import Modal
from ..shared.js_integration.js_integration import JsComponent

@component
def ThemingApp():
    theme, set_theme = hooks.use_state("light")
    show_help, set_show_help = hooks.use_state(False)

    def toggle_theme(e):
        set_theme("dark" if theme == "light" else "light")

    def open_docs(e):
        # Open documentation in a new tab
        js = "window.open('https://docs.example.com', '_blank');"
        return JsComponent(js)

    def show_help_modal(e):
        set_show_help(not show_help)

    theme_js = f"""
        document.documentElement.setAttribute("data-theme", "{theme}");
    """

    return html.div(
        {"class_name": "container"},
        html.link({"rel": "stylesheet", "href": "/static/styles.css"}),
        html.div(
            {"class_name": "flex gap-4 mb-4"},
            Button("Toggle Theme", on_click=toggle_theme, variant="primary"),
            Button("Open Docs", on_click=open_docs, variant="primary"),
            Button("Show Help", on_click=show_help_modal, variant="secondary"),
        ),
        JsComponent(theme_js),
        Card(
            html.div(
                {"class_name": "space-y-4"},
                html.h1("🎨 Theming ReactPy Apps"),
                html.p("This card's appearance changes with the theme."),
            )
        ),
        # Help modal (optional)
        Modal(
            html.p("Here is some helpful information about theming!"),
            is_open=show_help,
            on_close=lambda e: set_show_help(False),
            title="Theming Help"
        ) if show_help else None
    )
