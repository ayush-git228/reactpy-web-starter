from reactpy import hooks, component, html

def create_theme_context():
    return hooks.create_context(("light", lambda: None))

ThemeContext = create_theme_context()

@component
def ThemeProvider(children):
    theme, set_theme = hooks.use_state("light")

    def toggle_theme():
        new_theme = "dark" if theme == "light" else "light"
        set_theme(new_theme)
        return new_theme

    hooks.use_effect(
        lambda: document.documentElement.setAttribute("data-theme", theme), # type: ignore
        [theme]
    )

    # return ThemeContext.Provider((theme, toggle_theme), children)
    return ThemeContext((theme, toggle_theme), children)
