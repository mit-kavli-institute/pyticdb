import os
import pathlib

import configurables as conf
import sqlalchemy as sa
from loguru import logger
from sqlalchemy import orm

CONFIG_DIR = pathlib.Path.home() / ".config" / "tic"
CONFIG_NAME = "db.conf"
CONFIG_PATH = CONFIG_DIR / CONFIG_NAME


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


@conf.configurable("Credentials")
@conf.param("username")
@conf.param("password")
@conf.option("database", type=str, default="tic_82")
@conf.option("host", type=str, default="localhost")
@conf.option("port", type=int, default=5432)
def create_engine_from_config(username, password, database, host, port):
    url = f"postgresql://{username}:{password}@{host}:{port}/{database}"
    engine = sa.create_engine(url)

    return register_engine_guards(engine)


@conf.configurable("Credentials")
@conf.param("username")
@conf.param("password")
@conf.option("database", type=str, default="tic_82")
@conf.option("host", type=str, default="localhost")
@conf.option("port", type=int, default=5432)
def session_from_config(username, password, database, host, port):
    url = f"postgresql://{username}:{password}@{host}:{port}/{database}"
    engine = sa.create_engine(url)
    return orm.sessionmaker(bind=engine)


try:
    TicDB = session_from_config(CONFIG_PATH)
except FileNotFoundError:
    logger.error(f"Could not find a configuration file at '{CONFIG_PATH}'")
