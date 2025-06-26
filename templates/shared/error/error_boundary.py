from reactpy import component, html

@component
def ErrorBoundary(fallback, children):
    try:
        return children
    except Exception as e:
        return fallback(str(e))
