import nox


@nox.session
def tests(session: nox.Session):
    session.install(".[dev]")
    session.run("pytest")
