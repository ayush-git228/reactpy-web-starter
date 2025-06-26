from pathlib import Path
from reactpy import component, html, hooks
from typing import Optional, cast

# Use the provided use_store hook
def use_store(initial_state):
    state, set_state = hooks.use_state(initial_state)
    def dispatch(action):
        if action["type"] == "toggle_modal":
            set_state({**state, "show_modal": action["show_modal"]})
        # Add more actions as needed
    return state, dispatch

from ..shared.components.button import Button
from ..shared.components.card import Card
from ..shared.components.loader import Loader
from ..shared.components.modal import Modal
from ..shared.components.table import Table
from ..shared.error.error_boundary import ErrorBoundary
from ..shared.devtools.devtools import DevToolsPanel
from ..shared.js_integration.js_integration import JsComponent

import os
import pandas as pd
import plotly.express as px
import base64

#UPLOAD_DIR = Path(__file__).parent / "uploads"
UPLOAD_DIR = Path(__file__).parent.parent.parent / "uploads"

UPLOAD_DIR.mkdir(exist_ok=True)

@component
def FileUpload(on_upload):
    def upload_file(e):
        js = """
        const input = document.querySelector('input[type="file"]');
        const file = input.files[0];
        if (!file) return;
        const formData = new FormData();
        formData.append('file', file);
        fetch('/upload', {
            method: 'POST',
            body: formData,
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                alert("Upload complete! Click 'Refresh' to see the file.");
            }
        });
        """
        return JsComponent(js)

    return html.div(
        html.input({"type": "file", "name": "file", "accept": ".csv,.xlsx,.pdf,.docx,.jpg,.png"}),
        Button("Upload", on_click=upload_file, variant="primary"),
    )

@component
def DataPreview(file, df, chart_svg, error_message):
    if not file:
        return html.p("Upload a file and click 'Refresh' to see preview.")
    table_content = (
        Table(columns=df.columns.tolist(), data=df.head(5).values.tolist())
        if df is not None and not df.empty
        else None
    )
    return html.div(
        {"class_name": "space-y-4"},
        html.p(f"File: {file}"),
        html.p(f"Type: {file.split('.')[-1].upper()}"),
        html.p(f"Size: {os.path.getsize(UPLOAD_DIR / file)} bytes"),
        html.div({"dangerouslySetInnerHTML": {"__html__": chart_svg}}) if chart_svg else None,
        table_content,
        html.p({"class_name": "text-red-500"}, error_message) if error_message else None,
    )

@component
def Dashboard(file="", error=""):
    file, set_file = hooks.use_state(file)
    error, set_error = hooks.use_state("")
    df, set_df = hooks.use_state(cast(Optional[pd.DataFrame], None))
    chart_svg, set_chart_svg = hooks.use_state("")
    error_message, set_error_message = hooks.use_state("")
    
    # Use the provided use_store hook
    state, dispatch = use_store({
        "show_modal": False,
        "file_info": {"name": "", "size": 0, "type": ""}
    })

    def refresh_files(e):
        files = list(UPLOAD_DIR.glob("*"))
        print("Files in uploads dir:", files)  # Debug log
        if files:
            latest = max(files, key=lambda f: f.stat().st_mtime)
            print("Latest file:", latest.name)  # Debug log
            set_file(latest.name)
            
            # Update file info in store
            dispatch({
                "type": "update_file_info",
                "name": latest.name,
                "size": os.path.getsize(UPLOAD_DIR / latest.name),
                "type": latest.name.split('.')[-1].upper()
            })
        else:
            set_file("")
            set_error_message("No files found. Upload a file first.")
            # Reset file info in store
            dispatch({"type": "reset_file_info"})

    def handle_file_change(f):
        if not f:
            set_df(None)
            set_chart_svg("")
            set_error_message("")
            return
        try:
            file_path = UPLOAD_DIR / f
            print("Handling file change:", file_path)  # Debug log
            if f.lower().endswith(".csv"):
                new_df = pd.read_csv(file_path)
                print("CSV data loaded:", new_df.head())  # Debug log
                if not new_df.empty and len(new_df.select_dtypes(include=["number"]).columns) >= 2:
                    x_col = new_df.select_dtypes(include=["number"]).columns[0]
                    y_col = new_df.select_dtypes(include=["number"]).columns[1]
                    fig = px.scatter(new_df, x=x_col, y=y_col, title=f"{x_col} vs {y_col}")
                    svg_bytes = fig.to_image(format="svg")
                    set_chart_svg(svg_bytes.decode("utf-8"))
                else:
                    set_chart_svg("")
                set_df(new_df)
            elif f.lower().endswith(".xlsx"):
                new_df = pd.read_excel(file_path)
                print("Excel data loaded:", new_df.head())  # Debug log
                if not new_df.empty and len(new_df.select_dtypes(include=["number"]).columns) >= 2:
                    x_col = new_df.select_dtypes(include=["number"]).columns[0]
                    y_col = new_df.select_dtypes(include=["number"]).columns[1]
                    fig = px.scatter(new_df, x=x_col, y=y_col, title=f"{x_col} vs {y_col}")
                    svg_bytes = fig.to_image(format="svg")
                    set_chart_svg(svg_bytes.decode("utf-8"))
                else:
                    set_chart_svg("")
                set_df(new_df)
            elif f.lower().endswith((".jpg", ".png", ".jpeg")):
                with open(file_path, "rb") as img_file:
                    image_data = img_file.read()
                set_chart_svg(
                    f'<img src="data:image/{f.split(".")[-1]};base64,{base64.b64encode(image_data).decode("utf-8")}" width="300" alt="Uploaded Image">'
                )
                set_df(None)
            else:
                set_error_message(f"File type not supported for preview: {f.split('.')[-1]}")
                set_df(None)
                set_chart_svg("")
        except Exception as e:
            print("Error handling file:", e)  # Debug log
            set_error_message(str(e))
            set_df(None)
            set_chart_svg("")

    hooks.use_effect(lambda: handle_file_change(file), [file])

    return ErrorBoundary(
        lambda e: Card(html.div({"class_name": "text-red-500"}, f"Error: {e}")),
        html.div(
            {"class_name": "container"},
            html.link({"rel": "stylesheet", "href": "/static/styles.css"}),
            html.h1("📊 Interactive Data Dashboard"),
            FileUpload(on_upload=lambda: None),
            Button("Refresh", on_click=refresh_files, variant="primary"),
            Card(
                DataPreview(file, df, chart_svg, error_message)
            ),
            Button(
                "Show Modal",
                on_click=lambda e: dispatch({"type": "toggle_modal", "show_modal": not state["show_modal"]}),
                variant="secondary"
            ),
            Modal(
                html.div(
                    {"class_name": "space-y-4"},
                    html.p("This is a modal! You can put anything here."),
                    html.p(f"File: {file}") if file else None,
                    html.div({"dangerouslySetInnerHTML": {"__html__": chart_svg}}) if chart_svg else None,
                ),
                is_open=state["show_modal"],
                on_close=lambda e: dispatch({"type": "toggle_modal", "show_modal": False}),
                title="Dashboard Modal"
            ),
            DevToolsPanel(state)
        )
    )
