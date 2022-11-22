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
    """
    A quick implementation of a Django like interface allowing keyword names
    to be interpreted as sql column expressions.

    Parameters
    ----------
    kwarg: str
        The kwarg string. Should be in the format of ``column__operator``.

    rhs: typing.Any
        The value used as the operation right hand side.

    Returns
    -------
    The interpreted sqlalchemy BinaryExpression.

    Example
    -------
    >>> expression_from_kwarg(tmag__ge=13.5)
    >>> # Equivalent to (TicEntry.tmag <= 13.5)
    """
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
    """
    Get TIC parameters by querying from primary key(s).

    Parameters
    ----------
    id: integer or iterable of integers
        The primary key values to restrict the query to.
    *fields: str
        Names of columns to return.
    expression_filters: BinaryExpression or list of BinaryExpressions
        Additional filters to use.
    keyword_filters:
        Django like keywords to provide easy filtering without imports of
        TicEntry. Usage is such: ``column__operator=value`` which is
        interpreted like ``column operator value``. Where `operator` is the
        property within the standard library ``operator`` module.
    """
    q = TICEntry.select_from_fields(*fields)

    filters = []
    if isinstance(id, int):
        filters.append(TICEntry.id == id)
    else:
        filters.append(TICEntry.id.in_(id))

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
    """
    Get TIC parameters by a radial query.

    Parameters
    ----------
    ra: float
        The right ascension center of the radial query.
    dec: float
        The declination center of the radia query.
    radius: float
        The maximum radial distance to consider in units of degrees.
    *fields: str
        Names of columns to return.
    expression_filters: BinaryExpression or list of BinaryExpressions
        Additional filters to use.
    keyword_filters:
        Django like keywords to provide easy filtering without imports of
        TicEntry. Usage is such: ``column__operator=value`` which is
        interpreted like ``column operator value``. Where `operator` is the
        property within the standard library ``operator`` module.
    """
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
    """
    Pass a raw sql string to interpret. The provided text is assumed to be safe
    and no sanitization is performed! Use with caution!
    """
    q = sa.text(sql)

    with TicDB() as db:
        return db.execute(q).fetchall()
