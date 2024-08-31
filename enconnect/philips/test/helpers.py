"""
Functions and routines associated with Enasis Network Remote Connect.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



import asyncio
from json import dumps
from json import loads
from typing import AsyncIterator
from typing import Iterator

from encommon.types import DictStrAny

from httpx import AsyncByteStream
from httpx import SyncByteStream



class ByteStreamBlock(SyncByteStream):
    """
    Class used for gaining coverage in dependency projects.

    :param source: JSON encoded source string for iteration.
    """

    source: list[DictStrAny]

    def __init__(
        self,
        source: str,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.source = loads(source)

    def __iter__(
        self,
    ) -> Iterator[bytes]:
        """
        Return the iterator for enumerating the provided events.
        """

        source = self.source

        chunks = [
            (f'data: {dumps(x)}\n'
             .encode('utf-8'))
            for x in source]

        chunks.insert(0, b': hi\n')

        yield from chunks



class ByteStreamAsync(AsyncByteStream):
    """
    Class used for gaining coverage in dependency projects.

    :param source: JSON encoded source string for iteration.
    """

    source: list[DictStrAny]

    def __init__(
        self,
        source: str,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.source = loads(source)


    async def __aiter__(
        self,
    ) -> AsyncIterator[bytes]:
        """
        Return the iterator for enumerating the provided events.
        """

        source = self.source

        chunks = [
            (f'data: {dumps(x)}\n'
             .encode('utf-8'))
            for x in source]

        chunks.insert(0, b': hi\n')

        await asyncio.sleep(0)

        for chunk in chunks:

            yield chunk

            await asyncio.sleep(0)

        await asyncio.sleep(0)
