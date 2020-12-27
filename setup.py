import os
import setuptools

setup_path = os.path.dirname(os.path.realpath(__file__))

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

required_packages = []
required_packages_path = os.path.join(setup_path, "requirements.txt")
if os.path.isfile(required_packages_path):
    with open(required_packages_path, "r") as fh:
        required_packages = [entry.strip() for entry in fh.readlines()]

setuptools.setup(
    name="html_form_parser", # Replace with your own username
    version="0.0.1",
    author="Garrett Kunde",
    author_email="null",
    description="Static HTML Form Parser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gkunde/py_html_form_parser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=required_packages
)