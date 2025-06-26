from reactpy import component, html
from .components.AuthUI import AuthUI

@component
def AuthApp(on_login_success=None):
    return html.div(
        html.link({"rel": "stylesheet", "href": "/static/styles.css"}),
        AuthUI(on_login_success=on_login_success)
    )
