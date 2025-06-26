from reactpy import component, html

@component
def Loader(size="md"):
    size_classes = {
        "sm": "h-4 w-4 border-t-2 border-b-2",
        "md": "h-8 w-8 border-t-2 border-b-2",
        "lg": "h-12 w-12 border-t-2 border-b-2",
    }
    return html.div(
        {"class_name": "flex justify-center items-center h-16"},
        html.div({"class_name": f"animate-spin rounded-full {size_classes.get(size, 'h-8 w-8 border-t-2 border-b-2')} border-blue-500"})
    )
