from pathlib import Path
from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from reactpy import component, html, hooks
from reactpy.backend.fastapi import configure
import importlib

from ..shared.components.button import Button

TEMPLATES = {
    "auth": ("templates.auth.main", "AuthApp"),
    "dashboard": ("templates.dashboard.main", "Dashboard"),
    "landing": ("templates.landing.main", "Landing"),
    "theming": ("templates.theming.main", "ThemingApp"),
}

app = FastAPI()
app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.parent.parent / "static"),
    name="static"
)

# Define upload directory
UPLOAD_DIR = Path(__file__).parent.parent.parent / "uploads"
#UPLOAD_DIR = Path(__file__).parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if file.filename is None:
        return JSONResponse({"error": "No file selected"}, status_code=400)
    contents = await file.read()
    file_path = UPLOAD_DIR / file.filename
    print("Saving file to:", file_path)  
    with open(file_path, "wb") as f:
        f.write(contents)
    return JSONResponse({"success": True, "filename": file.filename})

@component
def FullApp():
    current_template, set_current_template = hooks.use_state("auth")
    logged_in, set_logged_in = hooks.use_state(False) 

    def switch_to_dashboard():
        set_current_template("dashboard")
        set_logged_in(True)

    def handle_logout(e):
        set_logged_in(False)
        set_current_template("auth") 

    def load_template(template_name):
        try:
            module_name, component_name = TEMPLATES[template_name]
            module = importlib.import_module(module_name)
            return getattr(module, component_name)
        except Exception as e:
            print(f"Error loading template {template_name}: {e}")
            return None

    TemplateComponent = load_template(current_template)

    if not TemplateComponent:
        return html.div("Error loading template")

    # Get file and error from query params (if you want to pass them to Dashboard)
    # NOTE: In ReactPy, you cannot access the request object directly.
    # For now, we'll just pass empty strings.
    # In a real app, you would need to get these from the URL or use client-side JS.
    file = ""
    error = ""

    return html.div(
        {"class_name": "container"},
        html.link({"rel": "stylesheet", "href": "/static/styles.css"}),
        Button("Logout", on_click=handle_logout, variant="danger") if logged_in else None,
        html.div(
            {"class_name": "flex gap-2 mb-4"},
            *[
                Button(
                    name.capitalize(),
                    on_click=lambda e, name=name: set_current_template(name),
                    variant="primary"
                )
                for name in TEMPLATES
                if logged_in or name == "auth"
            ]
        ),
        TemplateComponent(on_login_success=switch_to_dashboard) if current_template == "auth" else
        TemplateComponent(file=file, error=error) if current_template == "dashboard" else
        TemplateComponent()
    )

configure(app, FullApp)
