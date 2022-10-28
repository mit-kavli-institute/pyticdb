import typing

import sqlalchemy as sa

from pyticdb.conn import TicDB
from pyticdb.models import TICEntry

INT_SCALAR_OR_LIST = typing.Union[int, typing.List[int]]


def query_by_id(
    id: INT_SCALAR_OR_LIST, *fields: str
) -> typing.List[typing.Tuple]:
    q = TICEntry.select_from_fields(*fields)

    if isinstance(id, list):
        q = q.where(TICEntry.id.in_(id))
    else:
        q = q.where(TICEntry.id == id)

    with TicDB() as db:
        return list(db.execute(q).fetchall())


def query_by_loc(
    ra: float, dec: float, radius: float, *fields: str
) -> typing.List[typing.Tuple]:
    q = TICEntry.select_from_fields(*fields)

    q = q.where(
        sa.func.q3c_radial_query(TICEntry.ra, TICEntry.dec, ra, dec, radius)
    )

    with TicDB() as db:
        return db.execute(q).fetchall()


def query_raw(sql) -> typing.List[typing.Tuple]:
    q = sa.text(sql)

    with TicDB() as db:
        return db.execute(q).fetchall()
