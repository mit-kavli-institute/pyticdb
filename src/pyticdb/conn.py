import os
import pathlib
import typing

import configurables as conf
import sqlalchemy as sa
from loguru import logger
from sqlalchemy import MetaData, orm
from sqlalchemy.pool import NullPool

CONFIG_DIR = pathlib.Path.home() / ".config" / "tic"
CONFIG_NAME = "db.conf"
CONFIG_PATH = CONFIG_DIR / CONFIG_NAME


class TableReflectionCache:
    """
    This class attempts to minimize cost of reflecting remote schemas.
    Reflected schemas are served by request and then cached within a simple
    dictionary.

    If more control is needed then this class may be modified or switched
    to dedicated caching libraries.
    """

    def __init__(self, configuration_path: typing.Optional[pathlib.Path] = CONFIG_PATH):
        self.configuration_path = configuration_path
        self._cache: dict[str, tuple[sa.MetaData, orm.sessionmaker]] = {}

    def __setitem__(self, key: str, value: tuple[sa.MetaData, orm.sessionmaker]):
        self._cache[key] = value

    def __getitem__(self, key: str):
        try:
            return self._cache[key]
        except KeyError:
            metadata, sessionmaker = reflected_session(
                _filepath=self.configuration_path,
                _section=key,
            )
            self[key] = metadata, sessionmaker
            return metadata, sessionmaker


Databases = TableReflectionCache()


def _connect(dbapi_connection, connection_record):
    """
    A quick function that sets the connection pid context to the current
    process. This function is invoked upon SQLAlchemy engines establishing
    a remote connection.
    """
    connection_record.info["pid"] = os.getpid()


def _checkout(dbapi_connection, connection_record, connection_proxy):
    """
    A quick function that will force SQLAlchemy to destroy the current engine
    if the current process pid does not match that within the connection
    context. If there is a disconnect, the connection will be destroyed and
    another will be created (with the current pid populated within the
    connection context).
    """
    pid = os.getpid()
    if connection_record.info["pid"] != pid:
        connection_record.dbapi_connection = None
        connection_proxy.dbapi_connection = None
        raise sa.exc.DisconnectionError(
            f"Connection record belongs to pid {connection_record.info['pid']}"
            f" attempting to check out in pid {pid}"
        )


def register_engine_guards(engine: sa.Engine) -> sa.Engine:
    """
    This function will wrap the provided engine within custom
    'multiprocess guards'. This ensures that resources expected to be unique
    per process are not shared across memory space.
    """
    logger.trace("Registering engine {engine} with multiprocessing guards")
    sa.event.listens_for(engine, "connect")(_connect)
    sa.event.listens_for(engine, "checkout")(_checkout)
    return engine


@conf.configurable()
@conf.param("username")
@conf.param("password")
@conf.param("database")
@conf.option("host", default="localhost")
@conf.option("port", type=int, default=5432)
@conf.option("dialect", default="postgresql+psycopg")
def reflected_session(**configuration) -> tuple[sa.MetaData, orm.sessionmaker]:
    """
    Reflect the specified database. The configuration header has been left
    unspecified to allow to runtime changes to whatever configuration file and
    whatever section to use.

    This function also allows non-postgresql dialects to be used.

    Returns
    -------
    tuple[MetaData, sessionmaker]
        Returns both the reflect metadata (such as tables, sequences, schemas,
        etc) as well as a sessionmaker to the specified database. It is up to
        the callee to know the schema they will be interacting with.

    Examples
    --------
    >>> from pyticdb.conn import reflected_session
    >>> meta, session = reflected_session(
    >>>     "./somedb.ini",
    >>>     _section="db_credentials"
    >>> )
    >>> with session() as db:
    >>>     table = meta.tables["some_table"]
    >>>     print(db.query(table.c.some_column).all())
    """
    url = "{dialect}://{username}:{password}@{host}:{port}/{database}"
    url = url.format(**configuration)
    engine = register_engine_guards(sa.create_engine(url, poolclass=NullPool))
    reflected_metadata = MetaData()
    reflected_metadata.reflect(bind=engine)  # Load the remote schema

    return reflected_metadata, orm.sessionmaker(bind=engine)
