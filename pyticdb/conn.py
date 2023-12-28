import os
import pathlib

import configurables as conf
import sqlalchemy as sa
from loguru import logger
from sqlalchemy import MetaData, orm
from sqlalchemy.pool import NullPool

CONFIG_DIR = pathlib.Path.home() / ".config" / "tic"
CONFIG_NAME = "db.conf"
CONFIG_PATH = CONFIG_DIR / CONFIG_NAME


class TableReflectionCache(dict):
    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except KeyError:
            metadata, sessionmaker = reflected_session(
                _filepath=CONFIG_PATH,
                _section=key,
            )
            self[key] = metadata, sessionmaker
            return metadata, sessionmaker


Databases = TableReflectionCache()


def _connect(dbapi_connection, connection_record):
    connection_record.info["pid"] = os.getpid()


def _checkout(dbapi_connection, connection_record, connection_proxy):
    pid = os.getpid()
    if connection_record.info["pid"] != pid:
        connection_record.dbapi_connection = None
        connection_proxy.dbapi_connection = None
        raise sa.exc.DisconnectionError(
            f"Connection record belongs to pid {connection_record.info['pid']}"
            f" attempting to check out in pid {pid}"
        )


def register_engine_guards(engine):
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
@conf.option("dialect", default="postgresql")
def reflected_session(**configuration):
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


try:
    _, TicDB = Databases["tic_82"]
except KeyError:
    TicDB = None
