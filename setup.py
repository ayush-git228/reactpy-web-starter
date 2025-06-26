# from setuptools import setup, find_packages
# from pathlib import Path

# # Read the contents of your README file
# this_directory = Path(__file__).parent
# long_description = (this_directory / "README.md").read_text()

# # Function to read requirements from a requirements.txt file
# def read_requirements(path):
#     return [
#         line.strip()
#         for line in Path(path).read_text().splitlines()
#         if not line.startswith('#') and line.strip()
#     ]

# # Dynamically collect all requirements from template requirements.txt files
# all_requirements = set()
# for template_dir in Path(__file__).parent.glob("templates/*/"):
#     req_file = template_dir / "requirements.txt"
#     if req_file.exists():
#         all_requirements.update(read_requirements(req_file))

# # Add core dependencies for the CLI itself
# core_requirements = read_requirements(Path(__file__).parent / "core_requirements.txt")
# all_requirements.update(core_requirements)


# setup(
#     name="reactpy-web-starter",
#     version="0.1.0", 
#     author="Ayush Gupta", 
#     author_email="ayushgupta228@gmail.com",
#     description="A powerful and opinionated web starter toolkit for building full-stack applications with ReactPy in Python.",
#     long_description=long_description,
#     long_description_content_type="text/markdown",
#     url="https://github.com/ayush-git228/reactpy-web-starter",
#     packages=find_packages(),
#     include_package_data=True, # Important to include non-Python files like templates
#     package_data={
#         "reactpy_web_starter": [ # This should match the base package name if find_packages is used without a specific folder
#             "templates/**/*",
#             "assets/*",
#             "templates/*/backend/*",
#             "templates/*/components/*",
#             "templates/*/data/*",
#             "*.md", # Include README
#             "*.toml", # Include pyproject.toml
#             "LICENSE", # Include LICENSE file
#             "core_requirements.txt" # Include the core requirements file
#         ]
#     },
#     install_requires=list(all_requirements), # All collected requirements
#     entry_points={
#         "console_scripts": [
#             "reactpy-web-starter=cli:main"
#         ]
#     },
#     classifiers=[
#         "Development Status :: 3 - Alpha",
#         "Intended Audience :: Developers",
#         "Intended Audience :: Science/Research",
#         "License :: OSI Approved :: MIT License",
#         "Programming Language :: Python :: 3",
#         "Programming Language :: Python :: 3.8",
#         "Programming Language :: Python :: 3.9",
#         "Programming Language :: Python :: 3.10",
#         "Programming Language :: Python :: 3.11",
#         "Programming Language :: Python :: 3.12",
#         "Framework :: ReactPy",
#         "Topic :: Software Development :: Libraries :: Application Frameworks",
#         "Topic :: Scientific/Engineering :: Visualization",
#         "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
#     ],
#     python_requires=">=3.8",
#     keywords=["reactpy", "python", "web", "starter", "boilerplate", "dashboard", "fullstack", "data science"],
# )


from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

def read_requirements(path):
    return [
        line.strip()
        for line in Path(path).read_text().splitlines()
        if not line.startswith('#') and line.strip()
    ]

all_requirements = set()
for template_dir in Path(__file__).parent.glob("templates/*/"):
    req_file = template_dir / "requirements.txt"
    if req_file.exists():
        all_requirements.update(read_requirements(req_file))

core_requirements = read_requirements(Path(__file__).parent / "reactpy_web_starter/core_requirements.txt")
all_requirements.update(core_requirements)

setup(
    name="reactpy-web-starter",
    version="0.1.0",
    author="Ayush Gupta",
    author_email="ayushgupta228@gmail.com",
    description="A powerful and opinionated web starter toolkit for building full-stack applications with ReactPy in Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ayush-git228/reactpy-web-starter",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "reactpy_web_starter": [
            "templates/**/*",
            "static/*",
            "hooks/*",
            "context/*",
            "utils/*",
            "*.md",
            "*.toml",
            "LICENSE",
            "core_requirements.txt"
        ]
    },
    install_requires=list(all_requirements),
    entry_points={
        "console_scripts": [
            "reactpy-web-starter=reactpy_web_starter.cli:main"
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Framework :: ReactPy",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    python_requires=">=3.8",
    keywords=["reactpy", "python", "web", "starter", "boilerplate", "dashboard", "fullstack", "data science"],
)

