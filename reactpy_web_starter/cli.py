import argparse
import os
import subprocess
import sys
from pathlib import Path
import shutil

# --- Define Project Root and Template Paths ---
CLI_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = CLI_DIR.parent.parent.resolve()
TEMPLATES_DIR = PROJECT_ROOT / "templates"
STATIC_DIR = PROJECT_ROOT / "static"

def read_requirements(file_path: Path):
    if not file_path.exists():
        return []
    with file_path.open("r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

def run_command(args):
    template_name = args.template
    template_main_py = TEMPLATES_DIR / template_name / "main.py"
    template_requirements_txt = TEMPLATES_DIR / template_name / "requirements.txt"

    print(f"✨ Running example for template '{template_name}'...")
    if template_requirements_txt.exists():
        try:
            print(f"Installing dependencies from {template_requirements_txt}...")
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(template_requirements_txt), "--no-warn-script-location"], check=True)
            print("Dependencies installed.")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error installing dependencies: {e}")
            sys.exit(1)
    else:
        print("No specific requirements.txt found for this example.")

    if not template_main_py.exists():
        print(f"❌ Error: Template '{template_name}' not found at {template_main_py}")
        sys.exit(1)

    print(f"Starting ReactPy app from {template_main_py}...")
    try:
        subprocess.run([sys.executable, str(template_main_py)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running example: Command '{e.cmd}' returned non-zero exit status {e.returncode}.")
        print("Ensure ReactPy is installed and the template's main.py is correct.")
        sys.exit(e.returncode)

def create_command(args):
    template_name = args.template
    project_name = args.project_name
    source_template_path = TEMPLATES_DIR / template_name
    destination_project_path = Path.cwd() / project_name

    if not source_template_path.is_dir():
        print(f"❌ Error: Template '{template_name}' not found at {source_template_path}")
        sys.exit(1)
    if destination_project_path.exists():
        print(f"❌ Error: Directory '{project_name}' already exists.")
        sys.exit(1)

    print(f"✨ Creating new project '{project_name}' from template '{template_name}'...")
    try:
        shutil.copytree(source_template_path, destination_project_path)
        print(f"✅ Project '{project_name}' created successfully at {destination_project_path}")
        print("\nNext steps:")
        print(f"1. cd {project_name}")
        print(f"2. pip install -r requirements.txt")
        print(f"3. python main.py")
    except Exception as e:
        print(f"❌ Error creating project: {e}")
        sys.exit(1)

def export_command(args):
    template_name = args.template
    output_dir = Path(args.output)
    source_template_path = TEMPLATES_DIR / template_name
    if not source_template_path.is_dir():
        print(f"❌ Error: Template '{template_name}' not found.")
        sys.exit(1)
    shutil.copytree(source_template_path, output_dir, dirs_exist_ok=True)
    print(f"✅ Template '{template_name}' exported to {output_dir}")

def main():
    parser = argparse.ArgumentParser(
        description="ReactPy Web Starter CLI: Scaffold and run ReactPy projects.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    run_parser = subparsers.add_parser(
        "run",
        help="Run an example template directly.",
        description="""\
Run an example template directly without creating a new project.
Example: reactpy-web-starter run dashboard"""
    )
    run_parser.add_argument("template", help="Name of the template to run (e.g., minimal, auth, dashboard).")
    run_parser.set_defaults(func=run_command)
    create_parser = subparsers.add_parser(
        "create",
        help="Create a new project from a template.",
        description="""\
Create a new project directory from a specified template.
Example: reactpy-web-starter create auth my_auth_app"""
    )
    create_parser.add_argument("template", help="Name of the template to use (e.g., minimal, auth, dashboard).")
    create_parser.add_argument("project_name", help="Name for your new project directory.")
    create_parser.set_defaults(func=create_command)
    export_parser = subparsers.add_parser(
        "export",
        help="Export a template as a static site.",
        description="""\
Export a template as a static site.
Example: reactpy-web-starter export auth --output dist"""
    )
    export_parser.add_argument("template", help="Template name")
    export_parser.add_argument("--output", default="dist", help="Output directory")
    export_parser.set_defaults(func=export_command)
    args = parser.parse_args()
    if args.command:
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
