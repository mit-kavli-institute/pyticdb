import operator
import typing
from itertools import chain

import sqlalchemy as sa
from sqlalchemy.sql.elements import BinaryExpression

from pyticdb.conn import TicDB
from pyticdb.models import TICEntry

INT_SCALAR_OR_LIST = typing.Union[int, typing.List[int]]
FILTER_TYPE = typing.Union[
    None, BinaryExpression, typing.List[BinaryExpression]
]


def expression_from_kwarg(kwarg: str, rhs: typing.Any) -> BinaryExpression:
    col_name, op_name = kwarg.split("__")
    lhs = getattr(TICEntry, col_name)
    op = getattr(operator, op_name)

    expression = op(lhs, rhs)

    return expression


def apply_filters(
    q,
    expressions: typing.List[BinaryExpression],
    keyword_filters: typing.Dict[str, typing.Any],
):
    parsed_filters = []
    for kwarg, value in keyword_filters.items():
        parsed_filters.append(expression_from_kwarg(kwarg, value))

    for expression in chain(expressions, parsed_filters):
        q = q.where(expression)

    return q


def query_by_id(
    id: INT_SCALAR_OR_LIST,
    *fields: str,
    expression_filters: FILTER_TYPE = None,
    **keyword_filters
) -> typing.List[typing.Tuple]:
    q = TICEntry.select_from_fields(*fields)

    filters = []
    if isinstance(id, list):
        filters.append(TICEntry.id.in_(id))
    else:
        filters.append(TICEntry.id == id)

    if expression_filters is not None:
        filters.extend(expression_filters)

    q = apply_filters(q, filters, keyword_filters)

    with TicDB() as db:
        return list(db.execute(q).fetchall())


def query_by_loc(
    ra: float,
    dec: float,
    radius: float,
    *fields: str,
    expression_filters: FILTER_TYPE = None,
    **keyword_filters
) -> typing.List[typing.Tuple]:
    q = TICEntry.select_from_fields(*fields)

    filters = [
        sa.func.q3c_radial_query(TICEntry.ra, TICEntry.dec, ra, dec, radius)
    ]

    if expression_filters is not None:
        filters.extend(expression_filters)

    q = apply_filters(q, filters, keyword_filters)

    with TicDB() as db:
        return db.execute(q).fetchall()


def query_raw(sql) -> typing.List[typing.Tuple]:
    q = sa.text(sql)

    with TicDB() as db:
        return db.execute(q).fetchall()
