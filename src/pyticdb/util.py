from itertools import islice
from typing import Generator, Iterable, TypeVar

RT = TypeVar("RT")


def chunkify(
    iterable: Iterable[RT], chunk_size: int
) -> Generator[list[RT], None, None]:
    """
    A pre python 3.12 chunkify function.
    Yields chunks of the iterable with the specified size.
    """
    iterator = iter(iterable)
    while True:
        chunk = list(islice(iterator, chunk_size))
        if not chunk:
            break
        yield chunk
