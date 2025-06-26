from reactpy import component, html
from ..shared.components.button import Button

@component
def Landing():
    def handle_learn_more(e):
        print("Learn More clicked!")
    def handle_get_started(e):
        print("Get Started clicked!")
    return html.div(
        {"class_name": "min-h-screen flex flex-col items-center justify-center gradient"},
        html.link({"rel": "stylesheet", "href": "/static/styles.css"}),
        html.h1(
            {"class_name": "text-5xl font-bold mb-4"},
            "🚀 Welcome to ReactPy Web Starter!"
        ),
        html.p(
            {"class_name": "text-xl text-center max-w-2xl mb-8"},
            "This is your landing page template. Start building amazing web apps with Python!"
        ),
        html.div(
            {"class_name": "flex space-x-4"},
            Button("Learn More", on_click=handle_learn_more, variant="primary"),
            Button("Get Started", on_click=handle_get_started, variant="secondary"),
        )
    )
