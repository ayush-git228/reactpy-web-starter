from reactpy import hooks

def use_theme():
    theme, set_theme = hooks.use_state("light")
    return theme, set_theme
