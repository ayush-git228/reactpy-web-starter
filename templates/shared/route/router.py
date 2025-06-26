# router.py
from reactpy import component, html, hooks

routes = {
    "/": "Home",
    "/dashboard": "Dashboard",
}

@component
def Router():
    path, set_path = hooks.use_state("/")
    current_page = routes.get(path, "404")
    return html.div(
        html.nav(
            [html.a({"href": route, "on_click": lambda e, r=route: set_path(r)}, name)
             for route, name in routes.items()]
        ),
        html.div(current_page)
    )
