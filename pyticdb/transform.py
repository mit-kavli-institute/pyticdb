import datetime
import typing

from sqlalchemy.engine import CursorResult, Row

INTERNAL_DATA = typing.List[Row]
FUNCTYPE = typing.Callable[[INTERNAL_DATA, ...], typing.Any]


class RemoteReturn:
    """
    This class wraps returns from `pyticdb.query`. It allows transparent access
    to the resulting remote SQL fetch while providing convenient data
    transforms.
    """

    def __init__(self, cursor: CursorResult):
        self.query_time_start = datetime.datetime.now()
        self._data = list(cursor.fetchall())
        self.query_time_end = datetime.datetime.now()

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self):
        yield from self._data

    def __getitem__(self, idx):
        return self._data[idx]

    def __repr__(self):
        return repr(self._data)

    def shape(self) -> typing.Union[int, typing.Tuple[int, int]]:
        if len(self._data) > 0:
            return (len(self._data), len(self._data[0]))
        else:
            return 0

    @property
    def time_elapsed(self) -> datetime.timedelta:
        return self.query_time_end - self.query_time_start

    def to(self, transform_func: FUNCTYPE, *args, **kwargs) -> typing.Any:
        """
        Call the provided function with the SQL result as the first
        positional parameter. Additional parameters and keyword arguments can
        be passed to the callee.

        Parameters
        ----------
        transform_func: typing.Callable

        *args: typing.Any
            Any positional parameters to pass to the transform function. Will
            be provided in order specified.
        **kwargs: typing.Any
            Any keyword parameters to pass to the transform function.

        Return
        ------
        typing.Any
            The return type of ``transform_func``.

        Example
        -------
        >>> result = query.query_by_loc(30, 30, 5, "id", "tmag", "ra", "dec")
        >>> result.to(pd.DataFrame, columns=["id", "tmag", "ra", "dec"])
                       id     tmag         ra        dec
        0       620522458  19.5013  26.517966  26.067170
        1        26854028  16.9362  26.554431  26.058153
        2       238602786  13.7684  25.831204  26.607332
        3        26780500  16.6801  25.749914  26.705586
        4        26780499  17.3535  25.751117  26.706271
        ...           ...      ...        ...        ...
        465131   63673024  15.4218  33.113164  34.242920
        465132  620976192  18.9674  33.113467  34.242985
        465133  620976196  19.3668  33.100306  34.253915
        465134  620976198  19.5535  33.082656  34.263246
        465135  620976186  19.2301  33.122409  34.237523
        \
        [465136 rows x 4 columns]
        """
        return transform_func(self._data, *args, **kwargs)

    def to_mapping(
        self,
        map_class: typing.Mapping = dict,
        ident: typing.Union[None, str] = None,
    ) -> typing.Mapping:
        """
        Convert the flat SQL return into a keyable mapping.

        map_class: typing.Mapping
            The mapping type to create.
        ident: str, optional
            The column name to use as an identifier. If None assume "id". This
            ident key must exist as part of the SQL return columns.

        Returns
        -------
        typing.Mapping
            An instance of the provided mapping class.

        Notes
        -----
        The user is expected to provide a column which contains unique values.
        If the provided ident column is not unique, then collisions will occur
        and the duplicate key will have the last value of the "group".
        """
        result = map_class()
        ident = "id" if ident is None else ident
        for row in self:
            result[getattr(row, ident)] = row
        return result

    def apply(
        self, function: typing.Callable[[Row], typing.Any]
    ) -> typing.Iterator[typing.Any]:
        """
        Apply the given function to each SQL alchemy row. Essentially an alias
        to ``map(function, query_func(*foo))``.

        Parameters
        ----------
        function: typing.Callable[[Row], typing.Any]
            The function to apply. Must take a ``sqlalchemy.engine.Row``
            object.

        Returns
        -------
        typing.Iterator[typing.Any]
            A generator yielding returns from the provided function.
        """
        return map(function, self._data)
