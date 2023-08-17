import operator
import typing
from functools import wraps
from itertools import chain

import sqlalchemy as sa
from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import BinaryExpression

from pyticdb.conn import Databases
from pyticdb.transform import RemoteReturn

INT_SCALAR_OR_LIST = typing.Union[int, typing.List[int]]
FILTER_TYPE = typing.Union[
    None, BinaryExpression, typing.List[BinaryExpression]
]


def _is_iterable(obj: typing.Any) -> bool:
    """
    Quickly determine if an object is iterable. Returns True if the object
    can be iterated on.
    """
    try:
        iter(obj)
    except TypeError:
        return False
    return True


def resolve_database(func):
    @wraps(func)
    def wrapper(*args, database=None, table=None, **kwargs):
        if database is None:
            database = "tic_82"
        if table is None:
            table = "ticentries"
        meta, sessionmaker = Databases[database]
        table = meta.tables[table]
        kwargs["database"] = sessionmaker()
        kwargs["table"] = table
        return func(*args, **kwargs)

    return wrapper


def expression_from_kwarg(
    table: sa.Table, kwarg: str, rhs: typing.Any
) -> BinaryExpression:
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
    lhs = getattr(table.c, col_name)
    op = getattr(operator, op_name)

    expression = op(lhs, rhs)

    return expression


def apply_filters(
    q,
    table: sa.Table,
    expressions: typing.List[BinaryExpression],
    keyword_filters: typing.Dict[str, typing.Any],
):
    parsed_filters = []
    for kwarg, value in keyword_filters.items():
        parsed_filters.append(expression_from_kwarg(table, kwarg, value))

    for expression in chain(expressions, parsed_filters):
        q = q.where(expression)

    return q


@resolve_database
def query_by_id(
    id: INT_SCALAR_OR_LIST,
    *fields: str,
    database: Session,
    table: sa.Table,
    expression_filters: FILTER_TYPE = None,
    **keyword_filters,
) -> RemoteReturn:
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
    columns = [getattr(table.c, field) for field in fields]
    q = sa.select(*columns)

    filters = []

    pk_columns = list(table.primary_key)
    depth = len(pk_columns)
    if depth == 0:
        # Attempt to recover by using a field called 'id'
        try:
            pk_columns = [table.c.id]
            depth = 1
        except AttributeError:
            raise RuntimeError(
                f"No primary key is specified on {database}: {table}. Attempts"
                " to use a field called 'id' failed as well."
            )

    if depth == 1:
        if _is_iterable(id) and not isinstance(id, str):
            filters.append(pk_columns[0].in_(id))
        else:
            filters.append(pk_columns[0] == id)
    else:
        # Handle composite primary key
        print(f"Cannot handle composite key of lenth {depth}: {pk_columns}")
        raise NotImplementedError

    if expression_filters is not None:
        filters.extend(expression_filters)

    q = apply_filters(q, table, filters, keyword_filters)

    with database as db:
        return RemoteReturn(db.execute(q))


@resolve_database
def query_by_loc(
    ra: float,
    dec: float,
    radius: float,
    *fields: str,
    database: Session,
    table: sa.Table,
    expression_filters: FILTER_TYPE = None,
    **keyword_filters,
) -> RemoteReturn:
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
    columns = [getattr(table.c, field) for field in fields]
    q = sa.select(*columns)

    filters = [
        sa.func.q3c_radial_query(table.c.ra, table.c.dec, ra, dec, radius)
    ]

    if expression_filters is not None:
        filters.extend(expression_filters)

    q = apply_filters(q, table, filters, keyword_filters)

    with database as db:
        return RemoteReturn(db.execute(q))


@resolve_database
def query_raw(sql, database: Session, table: sa.Table) -> RemoteReturn:
    """
    Pass a raw sql string to interpret. The provided text is assumed to be safe
    and no sanitization is performed! Use with caution!
    """
    q = sa.text(sql)

    with database as db:
        return RemoteReturn(db.execute(q))


@resolve_database
def inspect_schema(database: Session, table: sa.Table):
    print(table)
    print(table.columns)
