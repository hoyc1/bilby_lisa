# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
try:
    import importlib
    # The full version, including alpha/beta/rc tags.
    release = importlib.metadata.version(project.lower())
    # The short X.Y version.
    version = release.split('+', 1)[0]
except Exception:
    release = "unknown"

project = 'bilby LISA'
copyright = '2024, C.Hoy, L.K.Nuttall'
author = 'C.Hoy, L.K.Nuttall'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.ifconfig", "sphinx_immaterial", "sphinx_tabs.tabs"]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_immaterial'
html_theme_options = {
    # colouring and light/dark mode
    "palette": [
        {
            "media": "(prefers-color-scheme: light)",
            "scheme": "default",
            "primary": "blue-grey",
            "accent": "deep-orange",
        },
    ]
}
html_static_path = ['_static']
