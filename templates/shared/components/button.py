from reactpy import component, html

@component
def Button(text, on_click=None, variant="primary", disabled=False, **props):
    variant_class = {
        "primary": "button-primary",
        "secondary": "button-secondary",
        "danger": "button-danger",
    }.get(variant, "button-primary")
    return html.button(
        {
            "on_click": on_click,
            "class_name": f"button {variant_class}",
            "disabled": disabled,
            **props
        },
        text
    )
