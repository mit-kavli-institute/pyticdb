import nox


@nox.session
def tests(session: nox.Session):
    session.install(
        ".[dev]",
        "--extra-index-url",
        "https://mit-kavli-institute.github.io/MIT-Kavli-PyPi/",
    )
    session.run("pytest")


@nox.session
def docs(session: nox.Session):
    # Install docs requirements
    session.install("sphinx", "myst-parser")

    # You can also install your package in editable mode if you want autodoc
    # to see the up-to-date version:
    session.install(
        "-e",
        ".",
        "--extra-index-url",
        "https://mit-kavli-institute.github.io/MIT-Kavli-PyPi/",
    )

    # Invoke Sphinx to build HTML
    session.run(
        "sphinx-build",
        "-b",
        "html",  # Builder: html
        "docs",  # Source directory
        "docs/_build",  # Output directory
    )
