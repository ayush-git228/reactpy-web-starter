from reactpy import component, html, hooks

@component
def Lazy(loader, fallback=None):
    loaded, set_loaded = hooks.use_state(False)
    component, set_component = hooks.use_state(None)
    if not loaded:
        loader().then(lambda c: set_component(c) and set_loaded(True))
        return fallback or html.div("Loading...")
    return component
