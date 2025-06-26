from reactpy import component, html

@component
def JsComponent(script, container_id="js-component-container"):
    return html.div(
        html.script(script),
        html.div({"id": container_id})
    )
